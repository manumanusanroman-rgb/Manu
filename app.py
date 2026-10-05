import logging
import os
import re
import smtplib
from email.message import EmailMessage
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

import content

BASE_DIR = Path(__file__).resolve().parent
SITE_URL = "https://msanroman.com"
ASSET_VERSION = "20261004"
LANGS = ("es", "en")
LANG_COOKIE = "lang"

log = logging.getLogger("msanroman")

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Cada página existe en los dos idiomas, con su propia URL.
PAGES = {
    "home": {"es": "/", "en": "/en", "template": "index.html"},
    "about": {"es": "/sobre-mi", "en": "/en/about", "template": "sobre_mi.html"},
    "methodology": {"es": "/metodologia", "en": "/en/methodology", "template": "metodologia.html"},
    "projects": {"es": "/proyectos", "en": "/en/projects", "template": "proyectos.html"},
    "retos": {"es": "/proyectos/retos-de-habilidad", "en": "/en/projects/skills-challenge", "template": "retos.html"},
    "scouting": {"es": "/proyectos/rayados-scouting-lab", "en": "/en/projects/rayados-scouting-lab", "template": "scouting.html"},
    "contact": {"es": "/contacto", "en": "/en/contact", "template": "contacto.html"},
}
KNOWN_PATHS = {p[lang] for p in PAGES.values() for lang in LANGS}

# Match Center pausado (datos de menores). Se reactiva con ENABLE_MATCH_CENTER=1.
if os.getenv("ENABLE_MATCH_CENTER") == "1":
    from match_center import router as match_center_router

    app.include_router(match_center_router)


def cv_url(lang: str) -> str | None:
    """Devuelve el enlace al CV en PDF si el archivo existe."""
    name = f"Manu_Sanroman_CV_2026_{lang.upper()}.pdf"
    if (BASE_DIR / "static" / "docs" / name).exists():
        return f"/static/docs/{name}"
    return None


def page_context(request: Request, lang: str, page: str, **extra) -> dict:
    other = "en" if lang == "es" else "es"
    path = PAGES[page][lang]
    return {
        "request": request,
        "lang": lang,
        "other_lang": other,
        "t": content.TEXT[lang],
        "page": page,
        "urls": {key: p[lang] for key, p in PAGES.items()},
        "toggle_url": f"/lang/{other}?next={PAGES[page][other]}",
        "canonical": SITE_URL + path,
        "alternates": {code: SITE_URL + PAGES[page][code] for code in LANGS},
        "meta_title": content.TEXT[lang]["meta"][page][0],
        "meta_description": content.TEXT[lang]["meta"][page][1],
        "countries": content.COUNTRIES[lang],
        "email": content.EMAIL,
        "linkedin": content.LINKEDIN,
        "retos_app_url": content.RETOS_APP_URL,
        "retos_video": content.RETOS_VIDEO_EMBED,
        "scouting_repo_url": content.SCOUTING_REPO_URL,
        "cv_url": cv_url(lang),
        "asset_version": ASSET_VERSION,
        **extra,
    }


def make_page_route(page: str, lang: str):
    def route(request: Request):
        return templates.TemplateResponse(
            request, PAGES[page]["template"], page_context(request, lang, page, sent=request.query_params.get("sent") == "1")
        )

    return route


for _page, _cfg in PAGES.items():
    for _lang in LANGS:
        if _page == "home" and _lang == "es":
            continue  # "/" se resuelve abajo para recordar el idioma elegido
        app.add_api_route(_cfg[_lang], make_page_route(_page, _lang), methods=["GET"], response_class=HTMLResponse)


@app.get("/", response_class=HTMLResponse)
def home_es(request: Request):
    if request.cookies.get(LANG_COOKIE) == "en":
        return RedirectResponse(PAGES["home"]["en"], status_code=302)
    return templates.TemplateResponse(request, "index.html", page_context(request, "es", "home"))


@app.get("/lang/{code}")
def set_language(code: str, next: str = "/"):
    if code not in LANGS:
        code = "es"
    target = next if next in KNOWN_PATHS else PAGES["home"][code]
    response = RedirectResponse(target, status_code=303)
    response.set_cookie(LANG_COOKIE, code, max_age=60 * 60 * 24 * 365, samesite="lax")
    return response


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def send_contact_email(name: str, email: str, org: str, message: str) -> bool:
    """Envía el mensaje por SMTP (variables de entorno en Render). Sin configurar, solo lo registra."""
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    if not (host and user and password):
        log.warning("SMTP sin configurar; mensaje de %s <%s> no enviado", name, email)
        return False

    msg = EmailMessage()
    msg["Subject"] = f"msanroman.com · Mensaje de {name}"
    msg["From"] = user
    msg["To"] = os.getenv("CONTACT_TO", content.EMAIL)
    msg["Reply-To"] = email
    msg.set_content(f"Nombre: {name}\nEmail: {email}\nOrganización: {org or '-'}\n\n{message}")
    try:
        with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", "587")), timeout=15) as smtp:
            smtp.starttls()
            smtp.login(user, password)
            smtp.send_message(msg)
        return True
    except (smtplib.SMTPException, OSError):
        log.exception("Error enviando el formulario de contacto")
        return False


def make_contact_post(lang: str):
    def route(
        request: Request,
        name: str = Form(""),
        email: str = Form(""),
        org: str = Form(""),
        message: str = Form(""),
        website: str = Form(""),  # campo trampa para bots: los humanos no lo ven
    ):
        path = PAGES["contact"][lang]
        if website:
            return RedirectResponse(f"{path}?sent=1", status_code=303)

        name, email, org, message = name.strip(), email.strip(), org.strip(), message.strip()
        form = {"name": name, "email": email, "org": org, "message": message}
        if not name or len(name) > 120 or not EMAIL_RE.match(email) or len(email) > 200 \
                or not message or len(message) > 5000 or len(org) > 200:
            return templates.TemplateResponse(
                request, "contacto.html", page_context(request, lang, "contact", error="invalid", form=form), status_code=400
            )
        if not send_contact_email(name, email, org, message):
            return templates.TemplateResponse(
                request, "contacto.html", page_context(request, lang, "contact", error="send", form=form), status_code=502
            )
        return RedirectResponse(f"{path}?sent=1", status_code=303)

    return route


for _lang in LANGS:
    app.add_api_route(PAGES["contact"][_lang], make_contact_post(_lang), methods=["POST"], response_class=HTMLResponse)


@app.exception_handler(StarletteHTTPException)
async def not_found(request: Request, exc: StarletteHTTPException):
    if exc.status_code != 404:
        return HTMLResponse(str(exc.detail), status_code=exc.status_code)
    lang = "en" if request.url.path.startswith("/en") else "es"
    return templates.TemplateResponse(request, "404.html", page_context(request, lang, "home"), status_code=404)
