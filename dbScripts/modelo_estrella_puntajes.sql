-- Dimensiones
CREATE TABLE dim_institucion (
    cod_institucion INT PRIMARY KEY,
    nombre_institucion VARCHAR(255),
    tipo_institucion VARCHAR(100)
);

CREATE TABLE dim_sede (
    cod_sede INT PRIMARY KEY,
    nombre_sede VARCHAR(255),
    comuna VARCHAR(100),
    region VARCHAR(100),
    orden_geografico INT
);

CREATE TABLE dim_carrera (
    cod_carrera INT PRIMARY KEY,
    nombre_programa VARCHAR(255),
    carrera_generica VARCHAR(255),
    area_conocimiento VARCHAR(255),
    tipo_carrera VARCHAR(255),
    titulo_otorgado VARCHAR(255),
    grado_academico VARCHAR(255)
);

CREATE TABLE dim_fecha (
    anio INT PRIMARY KEY
);

CREATE TABLE dim_modalidad (
    id_modalidad SERIAL PRIMARY KEY,
    horario VARCHAR(50),
    tipo_programa VARCHAR(100),
    pregrado_posgrado VARCHAR(50)
);

-- Hecho: Matriculas y Puntajes
CREATE TABLE hechos_matriculas_puntajes (
    id_hecho SERIAL PRIMARY KEY,
    anio INT REFERENCES dim_fecha(anio),
    cod_institucion INT REFERENCES dim_institucion(cod_institucion),
    cod_sede INT REFERENCES dim_sede(cod_sede),
    cod_carrera INT REFERENCES dim_carrera(cod_carrera),
    id_modalidad INT REFERENCES dim_modalidad(id_modalidad),
    max_puntaje NUMERIC,
    prom_puntaje NUMERIC,
    min_puntaje NUMERIC,
    puntaje_corte_primero NUMERIC,
    puntaje_corte_promedio NUMERIC,
    puntaje_corte_ultimo NUMERIC,
    max_puntaje_nem NUMERIC,
    prom_puntaje_nem NUMERIC,
    min_puntaje_nem NUMERIC,
    max_puntaje_ranking NUMERIC,
    prom_puntaje_ranking NUMERIC,
    min_puntaje_ranking NUMERIC,
    alumnos_psu NUMERIC,
    alumnos_otra_via NUMERIC
);
