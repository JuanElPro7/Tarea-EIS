-- Dimensiones compartidas
CREATE TABLE dim_institucion_pregrado (
    cod_institucion INT PRIMARY KEY,
    nombre_institucion VARCHAR(255),
    tipo_institucion VARCHAR(100)
);

CREATE TABLE dim_carrera_pregrado (
    cod_carrera INT PRIMARY KEY,
    nombre_programa VARCHAR(255),
    area_conocimiento VARCHAR(255),
    tipo_carrera VARCHAR(255),
    titulo VARCHAR(255),
    grado_academico VARCHAR(255)
);

CREATE TABLE dim_sede_pregrado (
    cod_sede INT PRIMARY KEY,
    nombre_sede VARCHAR(255),
    comuna VARCHAR(100),
    region VARCHAR(100),
    orden_geografico INT
);

CREATE TABLE dim_fecha_pregrado (
    anio INT PRIMARY KEY
);

CREATE TABLE dim_modalidad_pregrado (
    id_modalidad SERIAL PRIMARY KEY,
    horario VARCHAR(50),
    tipo_programa VARCHAR(100),
    pregrado_posgrado VARCHAR(50)
);

-- Hecho aranceles
CREATE TABLE hechos_aranceles (
    id_hecho SERIAL PRIMARY KEY,
    anio INT REFERENCES dim_fecha_pregrado(anio),
    cod_institucion INT REFERENCES dim_institucion_pregrado(cod_institucion),
    cod_sede INT REFERENCES dim_sede_pregrado(cod_sede),
    cod_carrera INT REFERENCES dim_carrera_pregrado(cod_carrera),
    id_modalidad INT REFERENCES dim_modalidad_pregrado(id_modalidad),
    valor_matricula NUMERIC,
    valor_arancel NUMERIC,
    valor_titulo NUMERIC,
    vacantes INT,
    tipo_moneda VARCHAR(50)
);
