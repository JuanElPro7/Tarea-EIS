import csv
import psycopg
from collections import defaultdict

# Funciones seguras para convertir valores
def safe_int(value):
	try:
		return int(float(value))
	except (ValueError, TypeError):
		return 0

def safe_float(value):
	try:
		return float(value)
	except (ValueError, TypeError):
		return 0

# Conexión a la base de datos
conn = psycopg.connect(
	"host=localhost dbname=nombre_de_tu_bd user=tu_usuario password=tu_password"
)
cur = conn.cursor()

# Diccionarios para cachear los IDs de las dimensiones y evitar duplicados
fecha_ids = {}
institucion_ids = {}
carrera_ids = {}
sede_ids = {}

# Abrimos el CSV
with open("archivo.csv", encoding="utf-8") as csvfile:
	reader = csv.DictReader(csvfile)

	for row in reader:
		# Insertar fecha (solo año)
		anio = safe_int(row["Año"])
		if anio not in fecha_ids:
			cur.execute("INSERT INTO dim_fecha (anio) VALUES (%s) RETURNING id_fecha", (anio,))
			fecha_ids[anio] = cur.fetchone()[0]
		id_fecha = fecha_ids[anio]

		# Insertar institución
		institucion_key = (row["Clasificación6"], row["Tipo Institución"], row["Nombre Institución"])
		if institucion_key not in institucion_ids:
			cur.execute(
				"INSERT INTO dim_institucion (subsistema, tipo, nombre) VALUES (%s, %s, %s) RETURNING id_institucion",
				institucion_key
			)
			institucion_ids[institucion_key] = cur.fetchone()[0]
		id_institucion = institucion_ids[institucion_key]

		# Insertar carrera
		carrera_key = (row["Area Conocimiento"], row["Carrera Genérica"], row["Nombre Programa"])
		if carrera_key not in carrera_ids:
			cur.execute(
				"INSERT INTO dim_carrera (area, generica, programa) VALUES (%s, %s, %s) RETURNING id_carrera",
				carrera_key
			)
			carrera_ids[carrera_key] = cur.fetchone()[0]
		id_carrera = carrera_ids[carrera_key]

		# Insertar sede
		sede_key = (row["Nombre Region"], row["Comuna donde se imparte la carrera o programa"], row["Nombre de la Sede"])
		if sede_key not in sede_ids:
			cur.execute(
				"INSERT INTO dim_sede (region, comuna, nombre_sede) VALUES (%s, %s, %s) RETURNING id_sede",
				sede_key
			)
			sede_ids[sede_key] = cur.fetchone()[0]
		id_sede = sede_ids[sede_key]

		# Insertar en hechos_matriculas
		cur.execute("""
			INSERT INTO hechos_matriculas (
				id_fecha, id_institucion, id_carrera, id_sede,
				vacantes, matricula_hombres, matricula_mujeres, matricula_extranjeros,
				matricula_total_hombres, matricula_total_mujeres, matricula_total_extranjeros, matricula_total
			) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		""", (
			id_fecha, id_institucion, id_carrera, id_sede,
			safe_int(row["Vacantes"]),
			safe_int(row["Matrícula primer año hombres"]),
			safe_int(row["Matrícula primer año mujeres"]),
			safe_int(row["Matrícula primer año extranjeros"]),
			safe_int(row["Matrícula total hombres"]),
			safe_int(row["Matrícula total mujeres"]),
			safe_int(row["Matrícula total extranjeros"]),
			safe_int(row["Matrícula Total"])
		))

		# Insertar en hechos_puntajes
		cur.execute("""
			INSERT INTO hechos_puntajes (
				id_fecha, id_institucion, id_carrera, id_sede,
				max_promedio, prom_promedio, min_promedio,
				max_nem, prom_nem, min_nem,
				max_ranking, prom_ranking, min_ranking
			) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		""", (
			id_fecha, id_institucion, id_carrera, id_sede,
			safe_float(row["Máximo Puntaje (promedio matemáticas y lenguaje)"]),
			safe_float(row["Promedio Puntaje (promedio matemáticas y lenguaje)"]),
			safe_float(row["Mínimo Puntaje (promedio matemáticas y lenguaje)"]),
			safe_float(row["Máximo Puntaje NEM"]),
			safe_float(row["Promedio Puntaje NEM"]),
			safe_float(row["Mínimo Puntaje NEM"]),
			safe_float(row["Máximo Puntaje Ranking"]),
			safe_float(row["Promedio Puntaje Ranking"]),
			safe_float(row["Mínimo Puntaje Ranking"])
		))

# Confirmamos cambios y cerramos
conn.commit()
cur.close()
conn.close()

print("Carga completada correctamente.")
