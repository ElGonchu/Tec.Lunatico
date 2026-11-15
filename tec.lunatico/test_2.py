import sqlite3
from datetime import datetime
from pathlib import Path

ruta_db = Path(__file__).parent / "db.browser" / "astronauta.db"
conexion = sqlite3.connect(ruta_db)

# Ejemplo de datos que llegaron del sensor
lectura = {
    "oxigeno_sangre": 97.5,
    "pulsaciones": 78,
    "presion_sistolica": 122,
    "presion_diastolica": 81,
    "hrv": 45.2,
    "temperatura_corporal": 36.6,
    "impedancia_bioelectrica": 620,
    "conductividad_piel": 8.3,
    "ph_local": 5.4,
    "metilhistidina_3": None,
    "calcio_ionico": None,
    "citoquinas_inflamatorias": None,
    "globulos_blancos": None,
    "tipo": "sensor"
}

conexion = sqlite3.connect(ruta_db)
cursor = conexion.cursor()

cursor.execute("""
    INSERT INTO datos (
        oxigeno_sangre, pulsaciones, presion_sistolica, presion_diastolica,
        hrv, temperatura_corporal, impedancia_bioelectrica, conductividad_piel,
        ph_local, metilhistidina_3, calcio_ionico, citoquinas_inflamatorias,
        globulos_blancos, tipo
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    lectura["oxigeno_sangre"],
    lectura["pulsaciones"],
    lectura["presion_sistolica"],
    lectura["presion_diastolica"],
    lectura["hrv"],
    lectura["temperatura_corporal"],
    lectura["impedancia_bioelectrica"],
    lectura["conductividad_piel"],
    lectura["ph_local"],
    lectura["metilhistidina_3"],
    lectura["calcio_ionico"],
    lectura["citoquinas_inflamatorias"],
    lectura["globulos_blancos"],
    lectura["tipo"]
))

conexion.commit()
conexion.close()