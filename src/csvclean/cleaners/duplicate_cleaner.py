import pandas as pd
from null_cleaner import NullCleaner

# DataFrame con valores nulos
df = pd.DataFrame({
    "edad": [20, None, 30, None],
    "nombre": ["Ana", None, "Luis", None],
    "ciudad": ["Madrid", "Barcelona", None, "Sevilla"]
})

# Diccionario de issues simulado
issues = {
    1: [("edad", "null"), ("nombre", "null")],
    3: [("edad", "null"), ("nombre", "null"), ("ciudad", "null")]
}
