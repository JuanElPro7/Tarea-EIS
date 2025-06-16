-- DROP TABLES IF EXIST (por seguridad si corres varias veces)
DROP TABLE IF EXISTS hechos_matriculas CASCADE;
DROP TABLE IF EXISTS hechos_puntajes CASCADE;
DROP TABLE IF EXISTS dim_fecha CASCADE;
DROP TABLE IF EXISTS dim_institucion CASCADE;
DROP TABLE IF EXISTS dim_carrera CASCADE;
DROP TABLE IF EXISTS dim_sede CASCADE;

-- DIMENSIONES

CREATE TABLE dim_fecha (
    id_fecha SERIAL PRIMARY KEY,
    anio INTEGER NOT NULL
);

CREATE TABLE dim_institucion (
    id_institucion SERIAL PRIMARY KEY,
    subsistema VARCHAR(100),
    tipo VARCHAR(100),
    nombre VARCHAR(200)
);

CREATE TABLE dim_carrera (
    id_carrera SERIAL PRIMARY KEY,
    area VARCHAR(100),
    generica VARCHAR(150),
    programa VARCHAR(200)
);

CREATE TABLE dim_sede (
    id_sede SERIAL PRIMARY KEY,
    region VARCHAR(100),
    comuna VARCHAR(100),
    nombre_sede VARCHAR(150)
);

-- HECHOS MATRÍCULA

CREATE TABLE hechos_matriculas (
    id SERIAL PRIMARY KEY,
    id_fecha INTEGER REFERENCES dim_fecha(id_fecha),
    id_institucion INTEGER REFERENCES dim_institucion(id_institucion),
    id_carrera INTEGER REFERENCES dim_carrera(id_carrera),
    id_sede INTEGER REFERENCES dim_sede(id_sede),

    vacantes INTEGER,
    matricula_hombres INTEGER,
    matricula_mujeres INTEGER,
    matricula_extranjeros INTEGER,
    matricula_total_hombres INTEGER,
    matricula_total_mujeres INTEGER,
    matricula_total_extranjeros INTEGER,
    matricula_total INTEGER
);

-- HECHOS PUNTAJES

CREATE TABLE hechos_puntajes (
    id SERIAL PRIMARY KEY,
    id_fecha INTEGER REFERENCES dim_fecha(id_fecha),
    id_institucion INTEGER REFERENCES dim_institucion(id_institucion),
    id_carrera INTEGER REFERENCES dim_carrera(id_carrera),
    id_sede INTEGER REFERENCES dim_sede(id_sede),

    max_promedio REAL,
    prom_promedio REAL,
    min_promedio REAL,

    max_nem REAL,
    prom_nem REAL,
    min_nem REAL,

    max_ranking REAL,
    prom_ranking REAL,
    min_ranking REAL
);
