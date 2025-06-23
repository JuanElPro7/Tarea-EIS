import csv
import psycopg

conn = psycopg.connect(dbname="tarea-ies", user="postgres", password="postgres", host="localhost")
cur = conn.cursor()

with open('../data/matriculas_puntajes.csv', encoding='utf-8') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		# Insertar institución
		cur.execute("""
			INSERT INTO dim_institucion (cod_institucion, nombre_institucion, tipo_institucion)
			VALUES (%s, %s, %s)
			ON CONFLICT (cod_institucion) DO NOTHING;
		""", (row["Cód. Institución"], row["Nombre Institución"], row["Tipo Institución"]))

		# Insertar sede
		cur.execute("""
			INSERT INTO dim_sede (cod_sede, nombre_sede, comuna, region, orden_geografico)
			VALUES (%s, %s, %s, %s, %s)
			ON CONFLICT (cod_sede) DO NOTHING;
		""", (row["Cód. Sede"], row["Nombre de la Sede"], row["Comuna donde se imparte la carrera o programa"], row["Nombre Region"], row["Orden Geográfico de la Región (Norte aSur)"]))

		# Insertar carrera
		cur.execute("""
			INSERT INTO dim_carrera (cod_carrera, nombre_programa, carrera_generica, area_conocimiento, tipo_carrera, titulo_otorgado, grado_academico)
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			ON CONFLICT (cod_carrera) DO NOTHING;
		""", (row["Cód. Carrera"], row["Nombre Programa"], row["Carrera Genérica"], row["Area Conocimiento"], row["Tipo Carrera"], row["Título"], row["Grado Académico"]))

		# Insertar fecha
		cur.execute("""
			INSERT INTO dim_fecha (anio)
			VALUES (%s)
			ON CONFLICT (anio) DO NOTHING;
		""", (row["Año"],))

		# Insertar modalidad
		cur.execute("""
			INSERT INTO dim_modalidad (horario, tipo_programa, pregrado_posgrado)
			VALUES (%s, %s, %s)
			ON CONFLICT DO NOTHING;
		""", (row["Horario"], row["Tipo Programa"], row["Pregrado/Posgrado"]))

conn.commit()
cur.close()
conn.close()

conn = psycopg.connect(dbname="tarea-ies", user="postgres", password="postgres", host="localhost")
cur = conn.cursor()

# Obtener ID de modalidad
def get_modalidad_id(horario, tipo_programa, pregrado_posgrado):
	cur.execute("""
		SELECT id_modalidad FROM dim_modalidad
		WHERE horario = %s AND tipo_programa = %s AND pregrado_posgrado = %s
		""", (horario, tipo_programa, pregrado_posgrado))
	result = cur.fetchone()
	return result[0] if result else None

with open('../data/matriculas_puntajes.csv', encoding='utf-8') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		id_modalidad = get_modalidad_id(row["Horario"], row["Tipo Programa"], row["Pregrado/Posgrado"])

		cur.execute("""
			INSERT INTO hechos_matriculas_puntajes (
				anio, cod_institucion, cod_sede, cod_carrera, id_modalidad,
				max_puntaje, prom_puntaje, min_puntaje,
				puntaje_corte_primero, puntaje_corte_promedio, puntaje_corte_ultimo,
				max_puntaje_nem, prom_puntaje_nem, min_puntaje_nem,
				max_puntaje_ranking, prom_puntaje_ranking, min_puntaje_ranking,
				alumnos_psu, alumnos_otra_via
			) VALUES (%s, %s, %s, %s, %s,
					%s, %s, %s, %s, %s, %s,
					%s, %s, %s, %s, %s, %s,
					%s, %s)
		""", (
			row["Año"], row["Cód. Institución"], row["Cód. Sede"], row["Cód. Carrera"], id_modalidad,
			row["Máximo Puntaje (promedio matemáticas y lenguaje)"] or None,
			row["Promedio Puntaje (promedio matemáticas y lenguaje)"] or None,
			row["Mínimo Puntaje (promedio matemáticas y lenguaje)"] or None,
			row["Puntaje de corte (primer seleccionado)"] or None,
			row["Puntaje de corte (promedio de la carrera)"] or None,
			row["Puntaje de corte (último seleccionado)"] or None,
			row["Máximo Puntaje NEM"] or None,
			row["Promedio Puntaje NEM"] or None,
			row["Mínimo Puntaje NEM"] or None,
			row["Máximo Puntaje Ranking"] or None,
			row["Promedio Puntaje Ranking"] or None,
			row["Mínimo Puntaje Ranking"] or None,
			row["Nº Alumnos Ingreso Via PSU o PDT"] or None,
			row["Nº Alumnos Ingreso Otra Via"] or None
		))

conn.commit()
cur.close()
conn.close()
