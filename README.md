# CSV Cleaner

Una herramienta robusta de limpieza y validación de datos para archivos CSV, diseñada siguiendo principios de **Clean Code** y arquitectura modular. Este sistema permite detectar problemas de calidad y aplicar correcciones automáticas mediante un orquestador configurable.

## Características principales

- **Orquestación de Limpieza**: Sistema de "limpiadores" (Cleaners) independientes para nulos y tipos.
- **Validación de Datos**: Motor de validación que detecta discrepancias antes de procesar la fila.
- **Configuración Flexible**: Control total sobre qué reglas de limpieza aplicar mediante un objeto de configuración.
- **Calidad de Código**: Configuración integrada de `Ruff` (linter), `Pyright` (tipado estático) y `Pytest` (pruebas).
- **Poca necesidad de almacenamiento**: Debido al procesamiento de linea por linea no necesitamos almacenar grandes volúmenes de datos.

## Estructura del Proyecto

El proyecto sigue el estándar de estructura `src/`:

```text
CSV_Cleaner/
├── src/
│   └── csvclean/           # Paquete principal
│       ├── cleaners/       # Orchestrator y lógica de limpieza (Null, Type)
│       ├── validators/     # Validadores de estructura y tipos
│       ├── IO_layer/       # Lectura y escritura de archivos
│       ├── reporters/      # Generación de informes de calidad de datos
│       └── models/         # Definiciones de ErrorTypes, LineError y modelos
├── tests/                  # Suite completa de pruebas unitarias e integración
├── examples/               # Ejemplos de uso y archivos de prueba
├── main.py                 # Punto de entrada de la aplicación
├── pyproject.toml          # Configuración de dependencias

└── README.md
```

## Instalación y uso

Se necesita ejecutar en la terminal:

```text
uv sync
```

Para bajar el entorno virtual y para ejecutar el cleaner debemos poner:

```text

uv run python main.py --input tests\fixtures\dirty_data.csv --output tests\fixtures\clean_csv.csv --report
```

## Ejemplo de Ejecución

A continuación se muestra un ejemplo práctico de cómo el sistema procesa un archivo CSV detectando errores y aplicando la configuración de limpieza.

### 1. Preparar la Configuración (`config.txt`)

Crea un archivo de configuración para definir qué errores quieres tratar:
El usuario debe exponer los tipos de columna y que limpiezas se quieren realizar.
Para nuestro ejemplo, los tipos de columnas son: {str,int,str} y se van a realizar ambas limpiezas.

### 2. Implementación del csv sucio

```csv
name;age;city
Alice;30;Madrid
Bob;;
Charlie;25;Barcelona
;40;Valencia
```

### 3️. Flujo Interno del Sistema

El procesamiento se realiza fila por fila siguiendo este pipeline:

1. **IO_layer** lee cada fila del CSV.
2. La fila se envía a **Validators**, que detectan errores (nulos y tipos).
3. Los errores se encapsulan y se envían al **CleanerOrchestrator**.
4. El orquestador ejecuta los **Cleaners activos** según la configuración.
5. Las filas corregidas se envían a los **Reporters**.
6. Finalmente, se generan dos archivos de salida:
   - Un CSV limpio (`cleaned.csv`)
   - Un reporte detallado (`report.txt`)

```csv

name;age;city
Alice;30;Madrid
Charlie;25;Barcelona
```

Y

```txt
 There are 5 of ErrorTypes.NULL.
There are 0 of ErrorTypes.TYPE.
There were 5 errors in total.
3 rows has been fixed.
```
