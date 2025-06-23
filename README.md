# Tarea-EIS

## Para poblar la db:

Primero es necesario crear la base de datos llamada "tarea-ies"

### Correr los scripts sql

1. Crear las tablas de las ofertas de pregrado:

```bash
psql -U postgres -d tarea-ies -f modelo_estrella_pregrado.sql 
```

2. Crear las tablas de los puntajes:

```bash
psql -U postgres -d tarea-ies -f modelo_estrella_puntajes.sql 
```

### Poblar las bases de datos

1. Poblar la base de datos de pregrado:

```bash
python3 fillpregrado.py 
```

2. Poblar la base de datos de puntajes (este va a demorar, mucho):

```bash
python3 fillpuntajes.py 
```
