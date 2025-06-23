import csv
import psycopg

# Conexión a la base de datos
conn = psycopg.connect(dbname="tarea-ies", user="postgres", password="postgres", host="localhost")
cur = conn.cursor()

with open('../data/ofertasPregrado2025.csv', encoding='utf-8') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		# Insertar institución
		cur.execute("""
			INSERT INTO dim_institucion_pregrado (cod_institucion, nombre_institucion, tipo_institucion)
			VALUES (%s, %s, %s)
			ON CONFLICT (cod_institucion) DO NOTHING;
		""", (row["Cód. Institución"], row["Nombre Institución"], row["Tipo Institución"]))

		# Insertar sede
		cur.execute("""
			INSERT INTO dim_sede_pregrado (cod_sede, nombre_sede, comuna, region, orden_geografico)
			VALUES (%s, %s, %s, %s, %s)
			ON CONFLICT (cod_sede) DO NOTHING;
		""", (row["Cód. Sede"], row["Nombre de la Sede"], row["Comuna donde se imparte la carrera o programa"], row["Nombre Region"], row["Orden Geográfico de la Región (Norte aSur)"]))

		# Insertar carrera
		cur.execute("""
			INSERT INTO dim_carrera_pregrado (cod_carrera, nombre_programa, area_conocimiento, tipo_carrera, titulo, grado_academico)
			VALUES (%s, %s, %s, %s, %s, %s)
			ON CONFLICT (cod_carrera) DO NOTHING;
		""", (row["Cód. Carrera"], row["Nombre Programa"], row["Area Conocimiento"], row["Tipo Carrera"], row["Título"], row["Grado Académico"]))

		# Insertar fecha
		cur.execute("""
			INSERT INTO dim_fecha_pregrado (anio)
			VALUES (%s)
			ON CONFLICT (anio) DO NOTHING;
		""", (row["Año"],))

		# Insertar modalidad
		cur.execute("""
			INSERT INTO dim_modalidad_pregrado (horario, tipo_programa, pregrado_posgrado)
			VALUES (%s, %s, %s)
			ON CONFLICT DO NOTHING;
		""", (row["Horario"], row["Tipo Programa"], row["Pregrado/Posgrado"]))

conn.commit()

# Obtener ID de modalidad
def get_modalidad_id(horario, tipo_programa, pregrado_posgrado):
	cur.execute("""
		SELECT id_modalidad FROM dim_modalidad_pregrado
		WHERE horario = %s AND tipo_programa = %s AND pregrado_posgrado = %s
		""", (horario, tipo_programa, pregrado_posgrado))
	result = cur.fetchone()
	return result[0] if result else None

# Poblar tabla de hechos
with open('../data/ofertasPregrado2025.csv', encoding='utf-8') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		id_modalidad = get_modalidad_id(row["Horario"], row["Tipo Programa"], row["Pregrado/Posgrado"])

		cur.execute("""
		INSERT INTO hechos_aranceles (
			anio, cod_institucion, cod_sede, cod_carrera, id_modalidad,
			valor_matricula, valor_arancel, valor_titulo, vacantes, tipo_moneda
		) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		""", (
			row["Año"], row["Cód. Institución"], row["Cód. Sede"], row["Cód. Carrera"], id_modalidad,
			row["Valor de matrícula"] or None,
			row["Valor de arancel"] or None,
			row["Valor del Título"] or None,
			int(float(row["Vacantes (1)"])) if row["Vacantes (1)"] else None,
			row["TipoMonedaArancelAnual"].strip() if row["TipoMonedaArancelAnual"] else None
		))


conn.commit()
cur.close()
conn.close()
