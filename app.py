import re
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, date

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =========================
# DATOS DE PARTIDOS
# =========================
PARTIDOS_DATA = [
    {
        "id": "2026-01-24-rayados-blanco-vs-tuzos",
        "equipo": "Rayados en la Mira Blanco 2015",
        "equipo_color": "Blanco",
        "rival": "Tuzos Cantera Saltillo 2016",
        "liga": "J5 (FUT11)",
        "jornada": "Primera Jornada",
        "fecha": "Sábado 24 de Enero 2026",
        "sede": "NOVA FUT 11-A NATURAL",
        "marcador": "5 - 0",
        "notas": "Hora: 12:20 hrs · Cita: 11:50 hrs · Uniforme: Oficial de juego (espinilleras obligatorias).",
        "video_url": "https://www.facebook.com/100085635710864/videos/1529197534836713",
        "mvp": "ANGEL",
        "titulares": ["IAN","ANDRE","MATEO","LUCAS","TADEO","JUNIOR","IKER","GIO","RODOLFO","ANGEL","MATI"],
        "suplentes": ["ALFRED", "JOVANIE"],
        "eventos": [
            {"gol": "GIO",     "asistencia": "ANGEL",   "minuto": 6,  "asistencia_puntos": 0.5},
            {"gol": "ANGEL",   "asistencia": "JOVANIE", "minuto": 18, "asistencia_puntos": 1.0},
            {"gol": "MATI",    "asistencia": "RODO", "minuto": 27, "asistencia_puntos": 0.5},
            {"gol": "ANGEL",   "asistencia": "MATI",    "minuto": 38, "asistencia_puntos": 0.5},
            {"gol": "JOVANIE", "asistencia": "JUNIOR",  "minuto": 46, "asistencia_puntos": 1.0},
        ]
    },
    {
        "id": "2026-01-23-rayados-azul-vs-inter-nl",
        "equipo": "Rayados en la Mira Azul 2015",
        "equipo_color": "Azul",
        "rival": "Inter N. L.",
        "liga": "J5 (FUT11)",
        "jornada": "Jornada 1",
        "fecha": "Viernes 23 de Enero 2026",
        "sede": "Latin American School F11 Sintético",
        "marcador": "3 - 1",
        "notas": "Hora: 16:30 hrs · Cita: 16:00 hrs · Uniforme: Oficial de juego (espinilleras obligatorias).",
        "video_url": "https://www.facebook.com/100085635710864/videos/1937263017183066",
        "mvp": "RUY",
        "titulares": ["DIEGO","BRACHO","SAMPAYO","ERICK","CARLOS","RUY","PATO","RAMON","TAMEZ","EMI","SANTIAGO"],
        "suplentes": ["SANTI M","OSCAR","DAMIAN","LUIS"],
        "eventos": [
            {"gol": "EMI",   "asistencia": "TAMEZ", "minuto": 15, "asistencia_puntos": 1.0},
            {"gol": "RUY",   "asistencia": "LUIS",  "minuto": 16, "asistencia_puntos": 1.0},
{"gol": "GOL EN CONTRA (SANTI M)", "asistencia": "", "minuto": 24, "asistencia_puntos": 0.0},
            {"gol": "OSCAR", "asistencia": "RUY",   "minuto": 35, "asistencia_puntos": 1.0},
        ]
    },
    {
        "id": "2026-01-31-rayados-blanco-vs-global-sporting",
        "equipo": "Rayados en la Mira Blanco 2015",
        "equipo_color": "Blanco",
        "rival": "Global Sporting",
        "liga": "J5 (FUT11)",
        "jornada": "Jornada 2",
        "fecha": "Sábado 31 de Enero 2026",
        "sede": "TecMilenio Guadalupe F11 Sintético",
        "marcador": "7 - 0",
        "notas": "Hora: 13:10 hrs · Cita: 12:40 hrs · Uniforme: Oficial de juego (espinilleras obligatorias). · MULTITACOS SOLO.",
        "video_url": "https://www.facebook.com/watch/live/?ref=watch_permalink&v=1061364476165294",
        "mvp": "RODO",
        "titulares": ["ALFRED","ANDRE","MATEO","LUCAS","TADEO","JUNIOR","RODO","GIO","JOVANIE","ANGEL","MATI"],
        "suplentes": ["IAN","JORGE","NAPO"],
        "eventos": [
            {"gol": "AUTOGOL", "asistencia": "",       "minuto": 19, "asistencia_puntos": 0.0},
            {"gol": "MATI",    "asistencia": "JUNIOR", "minuto": 20, "asistencia_puntos": 1.0},
            {"gol": "MATI",    "asistencia": "",       "minuto": 26, "asistencia_puntos": 0.0},
            {"gol": "ANGEL",   "asistencia": "",       "minuto": 27, "asistencia_puntos": 0.0},
            {"gol": "JOVANIE", "asistencia": "RODO",   "minuto": 38, "asistencia_puntos": 1.0},
            {"gol": "ANGEL",   "asistencia": "RODO",   "minuto": 41, "asistencia_puntos": 1.0},
            {"gol": "RODO",    "asistencia": "NAPO",   "minuto": 43, "asistencia_puntos": 1.0},
        ]
    },
{
  "id": "2026-02-18-rem-azul-vs-fc-dinastia-2016",
  "equipo": "Rayados en la Mira Azul 2015",
  "equipo_color": "Azul",
  "rival": "F. C. Dinastía 2016",
  "liga": "LIGA NACIONAL ELITE (FUT9)",
  "jornada": "Jornada 4",
  "fecha": "Miércoles 18 de Febrero 2026",
  "sede": "Centro Deportivo Borregos 1 F9-A",
  "marcador": "7 - 0",
  "notas": "Hora: 16:15 hrs · Cita: 15:45 hrs · Uniforme: Oficial de juego (espinilleras obligatorias).",
  "video_url": "https://www.facebook.com/share/v/1C8kQC2pb1/",
  "mvp": "OSCAR",
  "titulares": ["SANTI M","LUIS","BRACHO","SANTIAGO","PATO","RUY","RAMON","OSCAR","EMI"],
  "suplentes": ["DIEGO","TAMEZ","DAMIAN","ENRIQUEZ","CARLOS"],
  "eventos": [
    {"gol": "OSCAR", "asistencia": "RUY",          "minuto": 2,  "asistencia_puntos": 1.0},
    {"gol": "RAMON", "asistencia": "EMI",          "minuto": 4,  "asistencia_puntos": 1.0},
    {"gol": "EMI",   "asistencia": "SANTIAGO",     "minuto": 15, "asistencia_puntos": 1.0},
    {"gol": "TAMEZ", "asistencia": "RAMON",        "minuto": 20, "asistencia_puntos": 1.0},
    {"gol": "RAMON", "asistencia": "CARLOS",       "minuto": 23, "asistencia_puntos": 1.0},
    {"gol": "OSCAR", "asistencia": "LUIS",         "minuto": 56, "asistencia_puntos": 1.0},
    {"gol": "OSCAR", "asistencia": "ENRIQUEZ (R)", "minuto": 59, "asistencia_puntos": 0.5}
  ]
},

{
  "id": "2026-02-18-rem-blanco-vs-selectivo-azul",
  "equipo": "Rayados en la Mira Blanco 2015",
  "equipo_color": "Blanco",
  "rival": "Selectivo Azul",
  "liga": "LIGA NACIONAL ELITE (FUT9)",
  "jornada": "Jornada 4",
  "fecha": "Miércoles 18 de Febrero 2026",
  "sede": "Centro Deportivo Borregos 1 F9-B",
  "marcador": "5 - 0",
  "notas": "Hora: 16:15 hrs · Cita: 15:45 hrs · Uniforme: Oficial de juego (espinilleras obligatorias).",
  "video_url": "https://www.facebook.com/share/v/1APjLknZrk/?mibextid=wwXIfr",
  "mvp": "IKER",
  "titulares": ["IAN","ANDRE","MATEO","LUCAS","JUNIOR","IKER","TADEO","RODO","ANGEL"],
  "suplentes": ["ALFRED","JORGE","GIO","MATI","JOVANIE"],
  "eventos": [
    {"gol": "TADEO", "asistencia": "RODO", "minuto": 2,  "asistencia_puntos": 1.0},
    {"gol": "IKER",  "asistencia": "ANDRE","minuto": 18, "asistencia_puntos": 1.0},
    {"gol": "ANGEL", "asistencia": "",     "minuto": 40, "asistencia_puntos": 0.0},
    {"gol": "IKER",  "asistencia": "RODO", "minuto": 53, "asistencia_puntos": 1.0},
    {"gol": "JORGE", "asistencia": "",     "minuto": 54, "asistencia_puntos": 0.0}
  ]
},

    {
        "id": "2026-01-31-rayados-azul-vs-tigres-zuazua",
        "equipo": "Rayados en la Mira Azul 2015",
        "equipo_color": "Azul",
        "rival": "Tigres Zuazua",
        "liga": "J5 (FUT11)",
        "jornada": "Jornada 2",
        "fecha": "Sábado 31 de Enero 2026",
        "sede": "TecMilenio Guadalupe F11 Sintético",
        "marcador": "9 - 0",
        "notas": "Hora: 08:30 hrs · MULTITACOS SOLO.",
        "video_url": "https://www.facebook.com/watch/live/?ref=watch_permalink&v=1456475806102684",
        "mvp": "RUY",
        "titulares": ["SANTI M","IKER","BRACHO","DAMIAN","ERICK","ALEXANDER","ARMANDO","MATIAS","LUIS","VICTOR","OSCAR"],
        "suplentes": ["DIEGO","EMILIANO","SANTIAGO"],
        "eventos": [
            {"gol": "RUY",     "asistencia": "OSCAR", "minuto": 1,  "asistencia_puntos": 1.0},
            {"gol": "RUY",     "asistencia": "",      "minuto": 2,  "asistencia_puntos": 0.0},
            {"gol": "RAMON",   "asistencia": "TAMEZ", "minuto": 5,  "asistencia_puntos": 1.0},
            {"gol": "OSCAR",   "asistencia": "TAMEZ", "minuto": 9,  "asistencia_puntos": 1.0},
            {"gol": "RAMON",   "asistencia": "EMI",   "minuto": 16, "asistencia_puntos": 1.0},
            {"gol": "OSCAR",   "asistencia": "RUY",   "minuto": 26, "asistencia_puntos": 1.0},
            {"gol": "LUIS",    "asistencia": "OSCAR", "minuto": 29, "asistencia_puntos": 1.0},
            {"gol": "ERICK",   "asistencia": "EMI",   "minuto": 30, "asistencia_puntos": 1.0},
            {"gol": "AUTOGOL", "asistencia": "",      "minuto": 36, "asistencia_puntos": 0.0},
        ]
    },
    {
        "id": "2026-01-31-global-sporting-negro-vs-rayados-azul",
        "equipo": "Rayados en la Mira Azul 2015",
        "equipo_color": "Azul",
        "rival": "Global Sporting Club Negro",
        "liga": "LIGA NACIONAL ELITE (FUT9)",
        "jornada": "Jornada 1",
        "fecha": "Sábado 31 de Enero 2026",
        "sede": "Centro Deportivo Nova F9 (Natural)",
        "marcador": "6 - 0",
        "notas": "Hora: 15:30 hrs.",
        "video_url": "https://www.facebook.com/100085635710864/videos/1061364476165294/",
        "mvp": "RAMON",
        "titulares": ["DIEGO","DAMIAN","BRACHO","SANTIAGO","PATO","LUIS","EMI","OSCAR","RAMON"],
        "suplentes": ["RUY","TAMEZ","ERICK"],
        "eventos": [
            {"gol": "SANTIAGO", "asistencia": "",      "minuto": 38, "asistencia_puntos": 0.0},
            {"gol": "OSCAR", "asistencia": "RAMON", "minuto": 45, "asistencia_puntos": 1.0},
            {"gol": "ERICK", "asistencia": "RAMON", "minuto": 50, "asistencia_puntos": 1.0},
            {"gol": "RAMON",  "asistencia": "",      "minuto": 51, "asistencia_puntos": 0.0},
            {"gol": "TAMEZ", "asistencia": "ERICK", "minuto": 52, "asistencia_puntos": 1.0},
            {"gol": "TAMEZ", "asistencia": "RUY",   "minuto": 54, "asistencia_puntos": .5},
        ]
    },
{
    "id": "2026-02-01-rayados-blanco-vs-jogo-mty",
    "equipo": "Rayados en la Mira Blanco 2015",
    "equipo_color": "Blanco",
    "rival": "Jogo MTY",
    "liga": "LIGA NACIONAL ELITE (FUT9)",
    "jornada": "Jornada 1",
    "fecha": "Domingo 1 de Febrero 2026",
    "sede": "Club Central Esfera F9-A",
    "marcador": "2 - 1",
    "notas": "Hora: 15:30 hrs · Cita: 15:00 hrs · Uniforme: OFICIAL DE JUEGO (uso obligatorio de espinilleras).",
    "video_url": "https://www.facebook.com/PlanetaDeportivo/videos/798652486585226/",
    "mvp": "JUNIOR",
    "titulares": ["IAN","JORGE","MATEO","LUCAS","JUNIOR","MATI","GIO","RODO","ANGEL"],
    "suplentes": ["JOVANIE","TADEO","ANDRE","ALFRED"],
    "eventos": [
        {"gol": "ANGEL",   "asistencia": "JOVANIE", "minuto": 38, "asistencia_puntos": 1.0},
{"gol": "GOL EN CONTRA (ALFRED)", "asistencia": "", "minuto": 45, "asistencia_puntos": 0.0},        {"gol": "RODO",    "asistencia": "MATI",    "minuto": 53, "asistencia_puntos": 1.0},
    ]
},
{
    "id": "2026-02-04-rayados-blanco-vs-dinastia",
    "equipo": "Rayados en la Mira Blanco 2015",
    "equipo_color": "Blanco",
    "rival": "Dinastia",
    "liga": "LIGA NACIONAL ELITE (FUT9)",
    "jornada": "Jornada 2",
    "fecha": "Miercoles 4 de Febrero 2026",
    "sede": "Centro Deportivo Borregos",
    "marcador": "4 - 0",
    "notas": "Hora: 4:00 pm · Cita: 3:30 pm · Uniforme: OFICIAL DE JUEGO (uso obligatorio de espinilleras).",
    "video_url": "https://www.facebook.com/Yisusrdz20/videos/1248430700546102",

    "mvp": "MATI",

    "titulares": [
        "ALFRED", "ANDRE", "MATEO", "LUCAS",
        "JUNIOR", "JOVANIE", "TADEO",
        "RODO", "ANGEL"
    ],
    "suplentes": ["IAN", "GIO", "MATI", "JORGE"],

    "eventos": [
        {
            "gol": "MATI",
            "asistencia": "RODO (R)",
            "minuto": 39,
            "asistencia_puntos": 0.5
        },
        {
            "gol": "ANGEL",
            "asistencia": "MATI",
            "minuto": 41,
            "asistencia_puntos": 1.0
        },
        {
            "gol": "RODO",
            "asistencia": "ANGEL",
            "minuto": 43,
            "asistencia_puntos": 1.0
        },
              {
            "gol": "MATI",
            "asistencia": "TADEO",
            "minuto": 47,
            "asistencia_puntos": 1.0
        }
    ]
},
{
    "id": "2026-02-13-rayados-blanco-vs-inter-nl-j5",
    "equipo": "Rayados en la Mira Blanco 2015",
    "equipo_color": "Blanco",
    "rival": "Inter NL",
    "liga": "J5 (FUT11)",
    "jornada": "Jornada 4",
    "fecha": "Viernes 13 de Febrero 2026",
    "sede": "Col. Himalaya F11 Natural",
    "marcador": "3 - 0",
    "notas": "Hora: 18:00 pm · Cita: 17:30 pm · Uniforme: Oficial de juego (espinilleras obligatorias).",
    "video_url": "https://www.facebook.com/100085635710864/videos/1273795254599013/",
    "mvp": "JUNIOR",
    "titulares": ["ALFRED","ANDRE","JORGE","LUCAS","LEO","GIO","JUNIOR","MATI","RODO","ANGEL","TADEO"],
    "suplentes": ["IAN","MATEO","NAPO","JUNIOR","IKER"],
    "eventos": [
        {"gol": "MATI",  "asistencia": "MATI",   "minuto": 24, "asistencia_puntos": 0.5},
        {"gol": "RODO",  "asistencia": "TADEO",  "minuto": 27, "asistencia_puntos": 1.0},
        {"gol": "ANGEL", "asistencia": "RODO",   "minuto": 29, "asistencia_puntos": 1.0}
    ]
},
{
    "id": "2026-02-13-rayados-azul-vs-global-sporting-lsp",
    "equipo": "Rayados en la Mira Azul 2015",
    "equipo_color": "Azul",
    "rival": "Global Sporting",
    "liga": "J5 (FUT11)",
    "jornada": "Jornada 4",
    "fecha": "Viernes 13 de Febrero 2026",
    "sede": "Colegio Himalaya F11 Natural",
    "marcador": "10 - 0",
    "notas": "Hora: 19:00 hrs · Cita: 18:30 hrs · Uniforme: Oficial de juego (espinilleras obligatorias).",
    "video_url": "https://www.facebook.com/100085635710864/videos/1435253727966087/",
    "mvp": "BRACHO",
    "titulares": ["SANTI M","TAMEZ","IKER","BRACHO","SANTIAGO","LUIS","PATO","RUY","RAMON","OSCAR","EMI"],
    "suplentes": ["DIEGO","DAMIAN","CARLOS"],
    "eventos": [
        {"gol": "EMI",    "asistencia": "",        "minuto": 2,  "asistencia_puntos": 0.0},
        {"gol": "TAMEZ",  "asistencia": "OSCAR",   "minuto": 7,  "asistencia_puntos": 1.0},
        {"gol": "OSCAR",  "asistencia": "BRACHO",  "minuto": 19, "asistencia_puntos": 1.0},
        {"gol": "EMI",    "asistencia": "BRACHO",  "minuto": 23, "asistencia_puntos": 1.0},
        {"gol": "TAMEZ",  "asistencia": "OSCAR",   "minuto": 28, "asistencia_puntos": 1.0},
        {"gol": "RUY",    "asistencia": "PATO",    "minuto": 32, "asistencia_puntos": 1.0},
        {"gol": "RUY",    "asistencia": "RAMON",   "minuto": 40, "asistencia_puntos": 1.0},
        {"gol": "TAMEZ",  "asistencia": "PATO",    "minuto": 45, "asistencia_puntos": 0.5},
        {"gol": "OSCAR",  "asistencia": "BRACHO",  "minuto": 47, "asistencia_puntos": 1.0},
        {"gol": "PATO",   "asistencia": "RAMON",   "minuto": 49, "asistencia_puntos": 1.0}
    ]
},
{
    "id": "2026-02-15-fc-dinastia-2015-vs-rayados-azul",
    "equipo": "Rayados en la Mira Azul 2015",
    "equipo_color": "Azul",
    "rival": "F. C. Dinastía 2015",
    "liga": "LIGA NACIONAL ELITE (FUT9)",
    "jornada": "Jornada 3",
    "fecha": "Domingo 15 de Febrero 2026",
    "sede": "Club Central Esfera F9-B",
    "marcador": "3 - 0",
    "notas": "Hora: 8:00 hrs · Cita: 7:30 hrs · Uniforme: OFICIAL DE JUEGO (uso obligatorio de espinilleras).",
    "video_url": "https://www.facebook.com/100085635710864/videos/1825038014833528",
    "mvp": "TAMEZ",
    "titulares": ["DIEGO","DAMIAN","BRACHO","SANTIAGO","PATO","RUY","RAMON","OSCAR","EMI"],
    "suplentes": ["SANTI M","LUIS","CARLOS","TAMEZ"],
    "eventos": [
        {"gol": "SANTIAGO", "asistencia": "",       "minuto": 2,  "asistencia_puntos": 0.0},
        {"gol": "TAMEZ",    "asistencia": "RAMON",  "minuto": 24, "asistencia_puntos": 1.0},
        {"gol": "OSCAR",    "asistencia": "TAMEZ",  "minuto": 41, "asistencia_puntos": 1.0}
    ]
},
{
    "id": "2026-02-15-fc-dinastia-2016-vs-rayados-blanco",
    "equipo": "Rayados en la Mira Blanco 2015",
    "equipo_color": "Blanco",
    "rival": "FC Dinastia 2016",
    "liga": "LIGA NACIONAL ELITE (FUT9)",
    "jornada": "Jornada 3",
    "fecha": "Domingo 15 de Febrero 2026",
    "sede": "Club Central Esfera F9-A",
    "marcador": "6 - 0",
    "notas": "Hora: 10:30 am · Cita: 10:00 am · Uniforme: OFICIAL DE JUEGO (uso obligatorio de espinilleras).",
    "video_url": "https://www.facebook.com/100085635710864/videos/2737155066653114",
    "mvp": "ANDRE",
    "titulares": ["ALFRED","JORGE","MATEO","LUCAS","JUNIOR","MATI","IKER","RODO","ANGEL"],
    "suplentes": ["IAN","ANDRE","JOVANIE","TADEO","GIO"],
    "eventos": [
        {"gol": "IKER",  "asistencia": "",        "minuto": 3,  "asistencia_puntos": 0.0},
        {"gol": "RODO",  "asistencia": "",        "minuto": 14, "asistencia_puntos": 0.0},
        {"gol": "GIO",   "asistencia": "ANDRE",   "minuto": 31, "asistencia_puntos": 1.0},
        {"gol": "ANGEL", "asistencia": "ANDRE",   "minuto": 37, "asistencia_puntos": 1.0},
        {"gol": "ANGEL", "asistencia": "JOVANIE", "minuto": 40, "asistencia_puntos": 1.0},
        {"gol": "IKER",  "asistencia": "ANDRE",   "minuto": 57, "asistencia_puntos": 1.0}
    ]
},
{
    "id": "2026-02-04-rayados-azul-vs-jogo-mty",
    "equipo": "Rayados en la Mira Azul 2015",
    "equipo_color": "Azul",
    "rival": "Jogo MTY",
    "liga": "LIGA NACIONAL ELITE (FUT9)",
    "jornada": "Jornada 2",
    "fecha": "Miercoles 4 de Febrero 2026",
    "sede": "Centro Deportivo Borregos",
    "marcador": "5 - 0",
    "notas": "Hora: 16:00 hrs · Cita: 15:45 hrs · Uniforme: OFICIAL DE JUEGO (uso obligatorio de espinilleras).",
    "video_url": "https://www.facebook.com/100085635710864/videos/3482328658585509",

    "mvp": "TAMEZ",

    "titulares": [
        "DIEGO", "DAMIAN", "BRACHO", "ERICK",
        "LUIS", "PATO", "RAMON",
        "OSCAR", "TAMEZ"
    ],
    "suplentes": ["EMI", "RUY", "SANTIAGO"],

    "eventos": [
        {
            "gol": "RUY",
            "asistencia": "",
            "minuto": 15,
            "asistencia_puntos": 0.0
        },
        {
            "gol": "TAMEZ",
            "asistencia": "PATO (R)",
            "minuto": 35,
            "asistencia_puntos": 0.5
        },
        {
            "gol": "RUY",
            "asistencia": "TAMEZ",
            "minuto": 44,
            "asistencia_puntos": 1.0
        },
        {
            "gol": "TAMEZ",
            "asistencia": "EMI",
            "minuto": 47,
            "asistencia_puntos": 1.0
        },
        {
            "gol": "RUY",
            "asistencia": "EMI",
            "minuto": 48,
            "asistencia_puntos": 1.0
       }
    ]
},
{
    "id": "2026-02-08-rayados-blanco-vs-tigres-zuazua",
    "equipo": "Rayados en la Mira Blanco 2015",
    "equipo_color": "Blanco",
    "rival": "Tigres Zuazua",
    "liga": "J5 (FUT11)",
    "jornada": "Jornada 3",
    "fecha": "Domingo 8 de Febrero 2026",
    "sede": "AKRA Soccer #2 F11 Natural",
    "marcador": "5 - 0",
    "notas": "Hora: 14:10 hrs · Cita: 13:40 hrs · Uniforme: OFICIAL DE JUEGO (uso obligatorio de espinilleras).",
    "video_url": "https://www.facebook.com/Yisusrdz20/videos/1419518666302341",

    "mvp": "RODO",

    "titulares": [
        "IAN", "ANDRE", "JORGE", "LUCAS", "LEO",
        "JUNIOR", "JOVANIE", "GIO", "NAPO", "ANGEL", "RODO"
    ],
    "suplentes": ["ALFRED", "TADEO"],

    "eventos": [
        {
            "gol": "RODO",
            "asistencia": "JUNIOR",
            "minuto": 12,
            "asistencia_puntos": 1.0
        },
        {
            "gol": "ANGEL",
            "asistencia": "RODO",
            "minuto": 13,
            "asistencia_puntos": 1.0
        },
        {
            "gol": "GIO",
            "asistencia": "",
            "minuto": 31,
            "asistencia_puntos": 0.0
        },
        {
            "gol": "TADEO",
            "asistencia": "RODO",
            "minuto": 40,
            "asistencia_puntos": 1.0
        },
        {
            "gol": "GIO",
            "asistencia": "TADEO",
            "minuto": 49,
            "asistencia_puntos": 1.0
        }
    ]
},
{

    "id": "2026-02-06-rayados-azul-vs-leon-mty-pte",
    "equipo": "Rayados en la Mira Azul 2015",
    "equipo_color": "Azul",
    "rival": "León MTY Pte.",
    "liga": "J5 (FUT11)",
    "jornada": "Jornada 3",
    "fecha": "Viernes 6 de Febrero 2026",
    "sede": "NOVA Fut 11-A Natural",
    "marcador": "1 - 1",
    "notas": "Hora: 18:50 hrs · Cita: 18:20 hrs · Uniforme: OFICIAL DE JUEGO (uso obligatorio de espinilleras).",
    "video_url": "https://www.facebook.com/61558629234089/videos/898640319822005/",

    "mvp": "DIEGO",

    "titulares": [
        "DIEGO",
        "DAMIAN", "IKER", "BRACHO", "ERICK",
        "PATO", "RUY",
        "LUIS", "RAMON",
        "EMI", "TAMEZ"
    ],
    "suplentes": ["OSCAR"],

    "eventos": [
        {
            "gol": "EMI",
            "asistencia": "OSCAR (R)",
            "minuto": 39,
            "asistencia_puntos": 0.5
        },
        {
            "gol": "GOL EN CONTRA (DIEGO)",
            "asistencia": "",
            "minuto": 46,
            "asistencia_puntos": 0.0
        }
    ]
}
]
# =========================
# HELPERS
# =========================
MESES_ES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12
}

def parse_fecha_es(fecha_str: str):
    """
    Soporta: 'Viernes 23 de Enero 2026' (con o sin acentos / mayúsculas).
    Regresa datetime.date o None.
    """
    if not fecha_str:
        return None

    s = fecha_str.strip().lower()
    # ejemplo: viernes 23 de enero 2026
    # quitamos comas y dobles espacios
    s = s.replace(",", " ")
    s = " ".join(s.split())

    # buscamos patrón: <dia_semana> <dd> de <mes> <yyyy>
    parts = s.split(" ")
    # mínimo esperado: 5 tokens: viernes 23 de enero 2026
    if len(parts) < 5:
        return None

    # intentamos encontrar el día (número) y el año
    # estrategia robusta: localizar primer token numérico (día) y último token numérico (año)
    day = None
    year = None
    for tok in parts:
        if tok.isdigit():
            day = int(tok)
            break
    if parts[-1].isdigit():
        year = int(parts[-1])

    if not day or not year:
        return None

    # mes: buscamos token que sea un mes en MESES_ES
    mes = None
    for tok in parts:
        t = tok.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
        if t in MESES_ES:
            mes = MESES_ES[t]
            break

    if not mes:
        return None

    try:
        return date(year, mes, day)
    except ValueError:
        return None


def resultado_desde_marcador(marcador: str) -> str:
    """
    Convierte 'X - Y' en 'Victoria' / 'Empate' / 'Derrota'.
    Asume que el primer número es tu equipo y el segundo el rival.
    """
    if not marcador:
        return ""

    limpio = marcador.replace(" ", "")
    if "-" not in limpio:
        return ""

    partes = limpio.split("-")
    if len(partes) != 2:
        return ""

    try:
        gf = int(partes[0])
        gc = int(partes[1])
    except ValueError:
        return ""

    if gf > gc:
        return "Victoria"
    if gf < gc:
        return "Derrota"
    return "Empate"


def calcular_estadisticas(partidos):
    """
    Regresa (goles_top, asist_top, mvps_top) como listas ordenadas:
    - Asistencias: (R) o (F) SIEMPRE valen 0.5, cualquier otra vale 1.0
    - No cuenta "GOL EN CONTRA (...)" como gol a favor
    """
    goles = {}
    asistencias = {}
    mvps = {}

    if not partidos or not isinstance(partidos, list):
        return [], [], []

    for p in partidos:
        if not isinstance(p, dict):
            continue

        # ===============================
        # MVP POR PARTIDO (NO SE TOCA)
        # ===============================
        mvp = (p.get("mvp") or "").strip()
        if mvp:
            mvps[mvp] = mvps.get(mvp, 0) + 1

        # ===============================
        # EVENTOS (GOLES + ASISTENCIAS)
        # ===============================
        for ev in (p.get("eventos") or []):
            if not isinstance(ev, dict):
                continue

            g = (ev.get("gol") or "").strip()
            a = (ev.get("asistencia") or "").strip()

            # ✅ GOLES A FAVOR (NO cuenta goles en contra)
            if g and g != "—" and not g.startswith("GOL EN CONTRA"):
                goles[g] = goles.get(g, 0) + 1

            # ✅ ASISTENCIAS: (R) o (F) siempre = 0.5
            if a and a != "—":
                pts = 0.5 if ("(R)" in a or "(F)" in a) else 1.0
                a_clean = a.replace("(R)", "").replace("(F)", "").strip()
                if a_clean:
                    asistencias[a_clean] = asistencias.get(a_clean, 0.0) + pts

    goles_top = sorted(goles.items(), key=lambda x: x[1], reverse=True)
    asist_top = sorted(asistencias.items(), key=lambda x: x[1], reverse=True)
    mvps_top = sorted(mvps.items(), key=lambda x: x[1], reverse=True)
    return goles_top, asist_top, mvps_top

def parse_marcador(marcador: str):
    """
    Espera formatos: "4 - 0" o "4-0"
    Regresa (gf, gc) o (None, None) si no se puede.
    """
    m = (marcador or "").strip()
    if not m:
        return None, None
    m = m.replace(" ", "")
    if "-" not in m:
        return None, None
    try:
        a, b = m.split("-", 1)
        return int(a), int(b)
    except ValueError:
        return None, None


def tabla_equipos_resumen(partidos):
    """
    Tabla Azul vs Blanco:
    PJ, V, E, D, GF, GC, DG, Pts (3/1/0)
    """
    equipos = {
        "Blanco": {"equipo_color": "Blanco", "pj": 0, "v": 0, "e": 0, "d": 0, "gf": 0, "gc": 0, "dg": 0, "pts": 0},
        "Azul":   {"equipo_color": "Azul",   "pj": 0, "v": 0, "e": 0, "d": 0, "gf": 0, "gc": 0, "dg": 0, "pts": 0},
    }

    for p in (partidos or []):
        color = (p.get("equipo_color") or "").strip()
        if color not in equipos:
            continue

        gf, gc = parse_marcador(p.get("marcador", ""))
        if gf is None:
            continue  # partido sin marcador = no cuenta

        t = equipos[color]
        t["pj"] += 1
        t["gf"] += gf
        t["gc"] += gc

        if gf > gc:
            t["v"] += 1
            t["pts"] += 3
        elif gf == gc:
            t["e"] += 1
            t["pts"] += 1
        else:
            t["d"] += 1

    for t in equipos.values():
        t["dg"] = t["gf"] - t["gc"]

    tabla = list(equipos.values())
    tabla.sort(key=lambda r: (r["pts"], r["dg"], r["gf"]), reverse=True)
    return tabla

def tabla_acumulada_por_jugador(partidos):

    goles = {}
    asist = {}
    mvps = {}
    jugadores = set()

    for p in partidos:

        # MVP
        mvp = (p.get("mvp") or "").strip()
        if mvp:
            jugadores.add(mvp)
            mvps[mvp] = mvps.get(mvp, 0) + 1

        # titulares y suplentes
        for j in (p.get("titulares") or []):
            jj = (j or "").strip()
            if jj:
                jugadores.add(jj)

        for j in (p.get("suplentes") or []):
            jj = (j or "").strip()
            if jj:
                jugadores.add(jj)

        # eventos
        for ev in (p.get("eventos") or []):
            g = (ev.get("gol") or "").strip()
            a = (ev.get("asistencia") or "").strip()

            # goles
            if g and g != "—" and not g.startswith("GOL EN CONTRA"):
                jugadores.add(g)
                goles[g] = goles.get(g, 0) + 1

            # asistencias
            if a and a != "—":
                jugadores.add(a)
                pts = ev.get("asistencia_puntos", 1.0)
                try:
                    pts = float(pts)
                except:
                    pts = 1.0
                asist[a] = asist.get(a, 0.0) + pts

    tabla = []

    for j in jugadores:
        g = goles.get(j, 0)
        a = asist.get(j, 0.0)
        m = mvps.get(j, 0)

        total = g + a + m

        if total == 0:
            continue

        tabla.append({
            "jugador": j,
            "goles": g,
            "asistencias": a,
            "mvps": m,
            "total": total
        })

    # Ordenar por TOTAL primero
    tabla.sort(key=lambda r: (-r["total"], -r["goles"], -r["asistencias"]))

    return tabla


import re

def tabla_porteros(partidos):
    """
    Tabla SIMPLE de porteros (solo goles recibidos):
    - Cuenta goles recibidos únicamente por eventos:
        "GOL EN CONTRA (NOMBRE)"
    - No usa marcador
    - No cuenta partidos jugados
    - Robusta ante mayúsculas/minúsculas y espacios
    """

    PORTEROS = ["ALFRED", "IAN", "SANTI M", "DIEGO"]
    goles_recibidos = {p: 0 for p in PORTEROS}

    # Regex flexible: "GOL EN CONTRA (ALFRED)" con variaciones de espacios/mayúsculas
    patron = re.compile(r"^gol\s+en\s+contra\s*\(\s*(.*?)\s*\)\s*$", re.IGNORECASE)

    if not partidos or not isinstance(partidos, list):
        return [{"portero": p, "goles_recibidos": 0} for p in PORTEROS]

    for partido in partidos:
        eventos = partido.get("eventos") or []
        if not isinstance(eventos, list):
            continue

        for ev in eventos:
            g = (ev.get("gol") or "").strip()
            if not g:
                continue

            m = patron.match(g)
            if not m:
                continue

            nombre = (m.group(1) or "").strip().upper()

            # Normalizamos espacios dobles
            nombre = " ".join(nombre.split())

            # Solo contamos si está en nuestra lista de porteros
            if nombre in goles_recibidos:
                goles_recibidos[nombre] += 1

    tabla = [{"portero": p, "goles_recibidos": goles_recibidos[p]} for p in PORTEROS]
    tabla.sort(key=lambda r: (-r["goles_recibidos"], r["portero"]))
    return tabla
def ordenar_partidos(partidos):
    """
    Próximos arriba (ascendente por fecha), pasados abajo (descendente por fecha).
    Si no puede parsear fecha, se va al final.
    """
    hoy = date.today()

    def key(p):
        d = p.get("fecha_dt")
        if not d:
            return (2, date.min)  # al final
        if d >= hoy:
            return (0, d)         # próximos
        return (1, date(1900, 1, 1))  # placeholder, ordenamos pasados aparte

    proximos = [p for p in partidos if p.get("fecha_dt") and p["fecha_dt"] >= hoy]
    pasados  = [p for p in partidos if p.get("fecha_dt") and p["fecha_dt"] < hoy]
    sin_dt   = [p for p in partidos if not p.get("fecha_dt")]

    proximos.sort(key=lambda p: p["fecha_dt"])
    pasados.sort(key=lambda p: p["fecha_dt"], reverse=True)

    return proximos + pasados + sin_dt

import re
from collections import defaultdict
from typing import Any

def _norm_name(s: str) -> str:
    """Normaliza nombre para conteo consistente (espacios, mayúsculas)."""
    if not s:
        return ""
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s

def _names_from_field(val: Any) -> list[str]:
    """
    Convierte titulares/suplentes a lista de nombres.
    Soporta:
      - list[str]
      - string separado por comas o saltos de línea
      - None
    """
    if not val:
        return []
    if isinstance(val, list):
        return [_norm_name(x) for x in val if _norm_name(x)]
    if isinstance(val, str):
        parts = re.split(r"[,\n]+", val)
        return [_norm_name(x) for x in parts if _norm_name(x)]
    return []

def build_pj_index(partidos_data: list[dict]) -> dict[str, int]:
    """
    PJ = cantidad de partidos donde aparece el nombre en titulares o suplentes.
    (Si aparece en suplentes también cuenta como jugó.)
    """
    pj = defaultdict(int)

    for p in partidos_data:
        titulares = set(_names_from_field(p.get("titulares")))
        suplentes = set(_names_from_field(p.get("suplentes")))
        convocados = titulares | suplentes

        for nombre in convocados:
            pj[nombre] += 1

    return dict(pj)

# =========================
# RUTAS
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/metodologia", response_class=HTMLResponse)
def metodologia(request: Request):
    return templates.TemplateResponse("metodologia.html", {"request": request})



@app.get("/sobre-mi", response_class=HTMLResponse)
def sobre_mi(request: Request):
    return templates.TemplateResponse("sobre_mi.html", {"request": request})

@app.get("/contacto", response_class=HTMLResponse)
def contacto(request: Request):
    return templates.TemplateResponse("contacto.html", {"request": request})

@app.get("/partidos", response_class=HTMLResponse)
def partidos(request: Request):
    partidos_out = []

    COLORES_FIJOS = ["Blanco", "Azul"]
    LIGAS_FIJAS = ["J5 (FUT11)", "LIGA NACIONAL ELITE (FUT9)", "GOLDEN LEAGUE (FUT11)"]

    sedes = set()
    hoy = date.today()

    for p in PARTIDOS_DATA:
        p2 = dict(p)

        p2["resultado"] = resultado_desde_marcador(p2.get("marcador", ""))
        p2["equipo_color"] = (p2.get("equipo_color") or "").strip()

        # fecha parseada para ordenar y marcar "próximo"
        p2["fecha_dt"] = parse_fecha_es(p2.get("fecha", ""))

        # flags UI
        marcador_txt = (p2.get("marcador") or "").strip()
        p2["pendiente"] = (not marcador_txt)
        p2["is_upcoming"] = bool(p2["fecha_dt"] and p2["fecha_dt"] >= hoy)

        partidos_out.append(p2)

        sede = (p2.get("sede") or "").strip()
        if sede:
            sedes.add(sede)

    # ✅ PJ (Partidos Jugados) — TIENE que ir dentro de la función
    # Usamos partidos_out para contar exactamente lo que se renderiza (más seguro).
    pj_index = build_pj_index(partidos_out)

    partidos_out = ordenar_partidos(partidos_out)

    # highlight: siguiente partido (primer upcoming)
    proximo = next((p for p in partidos_out if p.get("is_upcoming")), None)

    # ===== tus tablas actuales (NO se tocan) =====
    goles_top, asist_top, mvps_top = calcular_estadisticas(partidos_out)

    # ===== LEADERBOARD (Goles + Asistencias + MVPs + GA + TOTAL) =====
    sort = (request.query_params.get("sort") or "total").strip().lower()
    if sort not in ("total", "goles", "asistencias", "mvps", "ga", "pj"):
    sort = "total"

    lb = {}

    # goles
    for nombre, n in (goles_top or []):
        j = (nombre or "").strip()
        if not j:
            continue
        lb.setdefault(j, {"jugador": j, "goles": 0, "asistencias": 0.0, "mvps": 0, "ga": 0.0, "total": 0.0})
        lb[j]["goles"] = int(n or 0)

    # asistencias (pueden ser .5)
    for nombre, n in (asist_top or []):
        j = (nombre or "").strip()
        if not j:
            continue
        lb.setdefault(j, {"jugador": j, "goles": 0, "asistencias": 0.0, "mvps": 0, "ga": 0.0, "total": 0.0})
        try:
            lb[j]["asistencias"] = float(n or 0)
        except (TypeError, ValueError):
            lb[j]["asistencias"] = 0.0

    # mvps
    for nombre, n in (mvps_top or []):
        j = (nombre or "").strip()
        if not j:
            continue
        lb.setdefault(j, {"jugador": j, "goles": 0, "asistencias": 0.0, "mvps": 0, "ga": 0.0, "total": 0.0})
        lb[j]["mvps"] = int(n or 0)

   leaderboard = list(lb.values())

# calcular GA y TOTAL
for r in leaderboard:
    g = float(r.get("goles", 0) or 0)
    a = float(r.get("asistencias", 0) or 0)
    m = float(r.get("mvps", 0) or 0)
    r["ga"] = g + a
    r["total"] = g + a + m

# ✅ INYECTAR PJ EN LEADERBOARD
for r in leaderboard:
    nombre = (r.get("jugador") or "").strip()
    r["pj"] = pj_index.get(nombre, 0)

    # ordenar (con desempates para que sea estable)
    if sort == "goles":
        leaderboard.sort(key=lambda r: (-float(r["goles"]), -float(r["total"]), r["jugador"]))
    elif sort == "asistencias":
        leaderboard.sort(key=lambda r: (-float(r["asistencias"]), -float(r["total"]), r["jugador"]))
    elif sort == "pj":
    leaderboard.sort(key=lambda r: (-float(r.get("pj", 0) or 0), -float(r["total"]), r["jugador"]))
    elif sort == "mvps":
        leaderboard.sort(key=lambda r: (-float(r["mvps"]), -float(r["total"]), r["jugador"]))
    elif sort == "ga":
        leaderboard.sort(key=lambda r: (-float(r["ga"]), -float(r["total"]), r["jugador"]))
    else:
        leaderboard.sort(key=lambda r: (-float(r["total"]), -float(r["goles"]), -float(r["asistencias"]), -float(r["mvps"]), r["jugador"]))

    tabla_equipos = tabla_equipos_resumen(partidos_out)
    stats_jugadores = tabla_acumulada_por_jugador(partidos_out)
    porteros_tabla = tabla_porteros(partidos_out)

    # =========================
# INYECTAR PJ (Partidos Jugados)
# =========================

if isinstance(stats_jugadores, list):
    for r in stats_jugadores:
        if isinstance(r, dict):
            nombre = (r.get("jugador") or r.get("nombre") or "").strip()
            r["pj"] = pj_index.get(nombre, 0)

if isinstance(porteros_tabla, list):
    for r in porteros_tabla:
        if isinstance(r, dict):
            nombre = (r.get("portero") or r.get("jugador") or "").strip()
            r["pj"] = pj_index.get(nombre, 0)

    return templates.TemplateResponse(
        "partidos.html",
        {
            "request": request,
            "partidos": partidos_out,
            "proximo": proximo,
            "ligas": LIGAS_FIJAS,
            "sedes": sorted(sedes),
            "colores": COLORES_FIJOS,

            "goles_top": goles_top,
            "asist_top": asist_top,
            "mvps_top": mvps_top,

            "leaderboard": leaderboard,
            "sort": sort,

            "tabla_equipos": tabla_equipos,
            "stats_jugadores": stats_jugadores,
            "porteros_tabla": porteros_tabla
        }
    )




@app.get("/partidos/{partido_id}", response_class=HTMLResponse)
def partido_detalle(request: Request, partido_id: str):
    partidos_by_id = {p["id"]: p for p in PARTIDOS_DATA}
    p = partidos_by_id.get(partido_id)

    if not p:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    p = dict(p)
    p["resultado"] = p.get("resultado") or resultado_desde_marcador(p.get("marcador", ""))

    # fecha_dt para UI
    p["fecha_dt"] = parse_fecha_es(p.get("fecha", ""))

    # =========================
    # RESUMEN: GOLES Y ASISTENCIAS (con puntos)
    # =========================
    goles = {}
    asistencias = {}

    for ev in p.get("eventos", []):
        g = (ev.get("gol") or "").strip()
        a = (ev.get("asistencia") or "").strip()

        if g and g != "—":
            goles[g] = goles.get(g, 0) + 1

        if a and a != "—":
            pts = ev.get("asistencia_puntos", 1.0)
            try:
                pts = float(pts)
            except (TypeError, ValueError):
                pts = 1.0
            asistencias[a] = asistencias.get(a, 0.0) + pts

    goles_top = sorted(goles.items(), key=lambda x: x[1], reverse=True)
    asist_top = sorted(asistencias.items(), key=lambda x: x[1], reverse=True)

    return templates.TemplateResponse(
        "partido_detalle.html",
        {"request": request, "p": p, "goles_top": goles_top, "asist_top": asist_top}
    )


