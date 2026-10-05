"""Genera el CV en PDF (español e inglés) con el estilo de la web.

Uso:  python tools/build_cv.py
Salida: static/docs/Manu_Sanroman_CV_2026_ES.pdf y _EN.pdf

Para cambiar el CV, edita CV más abajo y vuelve a ejecutarlo.
Necesita Microsoft Edge (lo usa para imprimir el HTML a PDF).
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

from jinja2 import Template

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "static" / "docs"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

# El PDF de la web es público: sin teléfono. Para aplicaciones directas, pon True.
INCLUDE_PHONE = False
PHONE = "+52 81 4010 1110"

CV = {
    "es": {
        "lang": "es",
        "title": "Entrenador de fútbol formativo · Desarrollo de jugadores · Metodología de academia",
        "location": "Monterrey, México · Disponible para reubicación · Nacionalidad española y mexicana (pasaporte UE)",
        "s_profile": "Perfil",
        "profile": "Entrenador de fútbol formativo especializado en el desarrollo técnico del jugador. Tercera temporada al frente del grupo Sub‑10 en las fuerzas básicas de Rayados de Monterrey, donde creé los Retos de habilidad, un programa técnico en casa con su propia aplicación web. Antes contribuí a la metodología y puse en marcha el programa de entrenamiento individual de Houston Dutch Lions FC. Trabajo por nivel y no por edad, con cuatro pilares: personal, individual, grupal y cultura futbolística.",
        "s_experience": "Experiencia",
        "experience": [
            {"role": "Entrenador Sub‑10", "org": "Rayados de Monterrey · Fuerzas Básicas (Rayados en la Mira)",
             "where": "Monterrey, México", "when": "Ago 2023 – Actualidad",
             "points": [
                 "Entreno al grupo Sub‑10 por tercera temporada, con sesiones de dominio del balón, toma de decisiones y transferencia al partido.",
                 "Creé y dirijo los Retos de habilidad: retos semanales en casa con gestos de jugadores históricos, envío de vídeos y feedback con criterios definidos. Edición actual: unos 15 jugadores, desde septiembre de 2026.",
                 "Diseñé y desarrollé la app web del programa: registro de padres, acceso para entrenadores, vídeos y feedback.",
                 "Uso vídeo y observación para dar feedback individual y conectar el trabajo en casa con el partido.",
             ]},
            {"role": "Entrenador y becario de Operaciones", "org": "Houston Dutch Lions FC",
             "where": "Houston / The Woodlands, TX, EE. UU.", "when": "Ago 2021 – Dic 2022",
             "points": [
                 "Planifiqué y dirigí sesiones para varios equipos, de 4 a 18 años, adaptadas a la etapa y el nivel de cada jugador.",
                 "Contribuí a la metodología del club, dando más peso a los espacios reducidos y a la progresión con balón.",
                 "Puse en marcha el programa de entrenamiento individual del club.",
                 "Apoyé la operación del club: familias, uniformes, imagen, patrocinadores, ligas y comunidad.",
                 "Fui el enlace con las familias hispanohablantes.",
             ]},
            {"role": "Entrenador de desarrollo individual (tiempo parcial)", "org": "",
             "where": "Estados Unidos", "when": "2011 – 2021",
             "points": ["Sesiones técnicas individuales para jugadores de distintas edades y niveles, con feedback en vídeo."]},
        ],
        "s_projects": "Proyectos",
        "projects": [
            {"name": "Rayados Scouting Lab", "tag": "Proyecto final del máster",
             "text": "Herramienta de scouting y decisión deportiva (Python, Streamlit) que diagnostica las necesidades de la plantilla, puntúa a unos 3.100 jugadores de 8 ligas y comprueba las reglas de Liga MX.",
             "link": "github.com/manumanusanroman-rgb/rayados-scouting-lab"},
        ],
        "s_education": "Formación",
        "education": [
            {"title": "Máster de Formación Permanente en Big Data Deportivo",
             "org": "Real Madrid Graduate School – Universidad Europea, Madrid", "when": "2026"},
            {"title": "Licenciatura (B.S.) en Sports Business Administration (Management & Sales)",
             "org": "Stephen F. Austin State University, Texas", "when": "2019 – 2023"},
        ],
        "s_certs": "Licencias y certificaciones",
        "certs": [
            "Licencias Grassroots de U.S. Soccer: 4v4, 7v7, 9v9 y 11v11",
            "Especialista en Scouting y Análisis del Juego (45 h) · Coaches' Voice School, 2026",
            "Metodología del Fútbol · MBP School of Coaches",
            "Certificación de Google Analytics",
        ],
        "s_skills": "Competencias",
        "skills": [
            "Diseño de sesiones y progresiones técnicas por nivel",
            "Feedback con vídeo y evaluación de jugadores",
            "Scouting y análisis del juego",
            "Python (pandas, Streamlit) y Google Analytics",
            "Comunicación bilingüe con jugadores, familias y staff",
        ],
        "s_languages": "Idiomas",
        "languages": "Español (nativo) · Inglés (fluido)",
    },
    "en": {
        "lang": "en",
        "title": "Youth Football Coach · Player Development · Academy Methodology",
        "location": "Monterrey, Mexico · Open to relocation · Spanish and Mexican citizen (EU passport)",
        "s_profile": "Profile",
        "profile": "Youth football coach focused on technical player development. Third season coaching the U‑10 group at the Rayados de Monterrey academy, where I created the Skills Challenge, an at-home technical program with its own web app. Previously helped shape the coaching methodology and started the 1-on-1 training program at Houston Dutch Lions FC. I develop players by level, not age, around four pillars: personal, individual, group, and football culture.",
        "s_experience": "Experience",
        "experience": [
            {"role": "U‑10 Coach", "org": "Rayados de Monterrey Academy (Rayados en la Mira)",
             "where": "Monterrey, Mexico", "when": "Aug 2023 – Present",
             "points": [
                 "Coach the U‑10 group for a third straight season, with sessions built on ball mastery, decision-making, and carrying skills into games.",
                 "Created and run the Skills Challenge: weekly at-home challenges based on skills from the game's legends, with video submissions and criteria-based feedback. Current round: about 15 players, started September 2026.",
                 "Designed and built the program's web app: parent sign-up, coaching staff access, video uploads, and feedback.",
                 "Use video and training observation to give individual feedback and connect home work to match performance.",
             ]},
            {"role": "Coach & Operations Intern", "org": "Houston Dutch Lions FC",
             "where": "Houston / The Woodlands, TX", "when": "Aug 2021 – Dec 2022",
             "points": [
                 "Planned and ran sessions for multiple teams, ages 4 to 18, adapted to each player's stage and level.",
                 "Helped shape the club's coaching methodology around small-sided games and progressing the ball.",
                 "Started the club's 1-on-1 training program.",
                 "Supported club operations: family communication, uniforms, branding, sponsors, leagues, and community events.",
                 "Served as the main contact for Spanish-speaking families.",
             ]},
            {"role": "Private Skills Coach (part-time)", "org": "",
             "where": "United States", "when": "2011 – 2021",
             "points": ["1-on-1 technical sessions for players of different ages and levels, using video feedback."]},
        ],
        "s_projects": "Projects",
        "projects": [
            {"name": "Rayados Scouting Lab", "tag": "Master's final project",
             "text": "Scouting and recruitment tool (Python, Streamlit) that diagnoses squad needs, scores about 3,100 players from 8 leagues, and checks Liga MX squad rules.",
             "link": "github.com/manumanusanroman-rgb/rayados-scouting-lab"},
        ],
        "s_education": "Education",
        "education": [
            {"title": "Master's in Sports Big Data (Continuing Education)",
             "org": "Real Madrid Graduate School – Universidad Europea, Madrid", "when": "2026"},
            {"title": "B.S. in Sports Business Administration (Management & Sales)",
             "org": "Stephen F. Austin State University, Texas", "when": "2019 – 2023"},
        ],
        "s_certs": "Licenses & certifications",
        "certs": [
            "U.S. Soccer Grassroots Licenses: 4v4, 7v7, 9v9, and 11v11",
            "Scouting & Game Analysis Specialist (45 hrs) · Coaches' Voice School, 2026",
            "Football Methodology · MBP School of Coaches",
            "Google Analytics Certification",
        ],
        "s_skills": "Skills",
        "skills": [
            "Session design and technical progressions by level",
            "Video feedback and player evaluation",
            "Scouting and game analysis",
            "Python (pandas, Streamlit) and Google Analytics",
            "Bilingual communication with players, families, and staff",
        ],
        "s_languages": "Languages",
        "languages": "Spanish (native) · English (fluent)",
    },
}

TEMPLATE = Template("""<!doctype html>
<html lang="{{ cv.lang }}">
<head>
<meta charset="utf-8">
<title>Manu Sanroman · CV</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,500;6..96,700&family=Manrope:wght@400;500;700&display=swap">
<style>
  @page { size: Letter; margin: 11mm 15mm; }
  * { box-sizing: border-box; }
  body { margin: 0; font-family: "Manrope", Arial, sans-serif; font-size: 9.2pt; line-height: 1.36; color: #17181C; }
  h1 { font-family: "Bodoni Moda", Georgia, serif; font-weight: 500; font-size: 27pt; line-height: 1; margin: 0; letter-spacing: .01em; }
  .title { margin: 6px 0 0; font-size: 10.5pt; font-weight: 700; color: #8A6A22; }
  .meta { margin: 4px 0 0; color: #4A4D55; }
  .meta a { color: #17181C; text-decoration: none; }
  header { border-bottom: 2px solid #C9A54E; padding-bottom: 8px; margin-bottom: 2px; }
  h2 { font-size: 8.6pt; letter-spacing: .16em; text-transform: uppercase; color: #8A6A22; margin: 11px 0 4px; }
  p { margin: 0; }
  .job, .edu, .proj { break-inside: avoid; margin-bottom: 6px; }
  .row { display: flex; justify-content: space-between; gap: 12px; align-items: baseline; }
  .role { font-weight: 700; font-size: 10pt; }
  .when { font-weight: 700; color: #8A6A22; white-space: nowrap; }
  .org { color: #3A3B40; }
  ul { margin: 3px 0 0; padding-left: 15px; }
  li { margin-bottom: 1px; }
  .cols { break-inside: avoid; display: grid; grid-template-columns: 1fr 1fr; gap: 0 28px; }
  .muted { color: #5F6670; }
</style>
</head>
<body>
<header>
  <h1>Manu Sanroman</h1>
  <p class="title">{{ cv.title }}</p>
  <p class="meta">{{ cv.location }}</p>
  <p class="meta"><a href="mailto:manumanusanroman@gmail.com">manumanusanroman@gmail.com</a>{% if phone %} · {{ phone }}{% endif %} · <a href="https://msanroman.com">msanroman.com</a> · <a href="https://linkedin.com/in/manusanromanfdz">linkedin.com/in/manusanromanfdz</a></p>
</header>

<h2>{{ cv.s_profile }}</h2>
<p>{{ cv.profile }}</p>

<h2>{{ cv.s_experience }}</h2>
{% for job in cv.experience %}
<div class="job">
  <div class="row"><span class="role">{{ job.role }}{% if job.org %} · <span class="org">{{ job.org }}</span>{% endif %}</span><span class="when">{{ job.when }}</span></div>
  <p class="muted">{{ job.where }}</p>
  <ul>{% for p in job.points %}<li>{{ p }}</li>{% endfor %}</ul>
</div>
{% endfor %}

<h2>{{ cv.s_projects }}</h2>
{% for pr in cv.projects %}
<div class="proj">
  <p><span class="role">{{ pr.name }}</span> · <span class="muted">{{ pr.tag }}</span></p>
  <p>{{ pr.text }} <a href="https://{{ pr.link }}" style="color:#17181C">{{ pr.link }}</a></p>
</div>
{% endfor %}

<h2>{{ cv.s_education }}</h2>
{% for e in cv.education %}
<div class="edu">
  <div class="row"><span class="role">{{ e.title }}</span><span class="when">{{ e.when }}</span></div>
  <p class="org">{{ e.org }}</p>
</div>
{% endfor %}

<div class="cols">
  <div>
    <h2>{{ cv.s_certs }}</h2>
    <ul>{% for c in cv.certs %}<li>{{ c }}</li>{% endfor %}</ul>
  </div>
  <div>
    <h2>{{ cv.s_skills }}</h2>
    <ul>{% for s in cv.skills %}<li>{{ s }}</li>{% endfor %}</ul>
    <h2>{{ cv.s_languages }}</h2>
    <p>{{ cv.languages }}</p>
  </div>
</div>
</body>
</html>
""")


def build() -> None:
    if not EDGE.exists():
        raise SystemExit(f"No encuentro Microsoft Edge en {EDGE}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="cv_"))
    try:
        for code, cv in CV.items():
            html = tmp / f"cv_{code}.html"
            html.write_text(TEMPLATE.render(cv=cv, phone=PHONE if INCLUDE_PHONE else ""), encoding="utf-8")
            pdf = OUT_DIR / f"Manu_Sanroman_CV_2026_{code.upper()}.pdf"
            subprocess.run(
                [str(EDGE), "--headless", "--disable-gpu", "--no-pdf-header-footer",
                 "--virtual-time-budget=8000", f"--user-data-dir={tmp / 'edge'}",
                 f"--print-to-pdf={pdf}", html.as_uri()],
                check=True, timeout=120,
            )
            print("OK", pdf.relative_to(ROOT), pdf.stat().st_size, "bytes")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    build()
