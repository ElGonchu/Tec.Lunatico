from contextlib import closing
import math
import sqlite3
from pathlib import Path


RUTA_BASE_DATOS = Path(__file__).parent / "db.browser" / "tec_lunatico.db"


def clasificar_valor(
    valor: float,
    minimo: float,
    maximo: float,
    critico_bajo: float,
    critico_alto: float,
) -> str:
    limites = (valor, minimo, maximo, critico_bajo, critico_alto)
    if not all(math.isfinite(limite) for limite in limites):
        raise ValueError("El valor y los límites deben ser números finitos.")

    if not critico_bajo <= minimo <= maximo <= critico_alto:
        raise ValueError("Los límites de la base de datos no tienen un orden válido.")

    if valor < critico_bajo:
        return "CRÍTICO BAJO"
    if valor < minimo:
        return "BAJO"
    if valor <= maximo:
        return "DENTRO DEL RANGO"
    if valor < critico_alto:
        return "ALTO"
    return "CRÍTICO ALTO"


def comparar_valor(
    conexion: sqlite3.Connection, variable: str, valor: float
) -> tuple[str, str]:
    cursor = conexion.cursor()
    cursor.execute(
        """
        SELECT unidad, valor_minimo, valor_maximo,
               valor_critico_bajo, valor_critico_alto
        FROM parametros
        WHERE variable = ?
        """,
        (variable,),
    )
    fila = cursor.fetchone()
    if fila is None:
        raise ValueError(f"No existe el parámetro '{variable}' en la base de datos.")

    unidad, minimo, maximo, critico_bajo, critico_alto = fila
    limites = (minimo, maximo, critico_bajo, critico_alto)
    if any(limite is None for limite in limites):
        raise ValueError(f"El parámetro '{variable}' no tiene todos sus límites.")

    resultado = clasificar_valor(
        valor, minimo, maximo, critico_bajo, critico_alto
    )
    return resultado, unidad or ""


def main() -> None:
    with closing(sqlite3.connect(RUTA_BASE_DATOS)) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT variable FROM parametros ORDER BY variable")
        parametros = [fila[0] for fila in cursor.fetchall()]

        print("Parámetros disponibles:", ", ".join(parametros))
        variable = input("Nombre del parámetro: ").strip()
        try:
            valor = float(input("Valor a comparar: "))
            resultado, unidad = comparar_valor(conexion, variable, valor)
        except ValueError as error:
            print(f"Error: {error}")
            return

        print(f"Resultado: {resultado} ({valor:g} {unidad})")


if __name__ == "__main__":
    main()
