import pandas as pd
from csvclean.cleaners.null_cleaner import NullCleaner, TypeCleaner, DuplicateCleaner, DataCleaner, ErrorTypes
import pandas as pd


df = pd.DataFrame({
    "edad": [25, "30", None, 40, "abc"],
    "nombre": ["Ana", None, "Carlos", "Luis", "Marta"],
    "fecha": ["2023-01-01", "2023-02-30", "2023-03-05", None, "invalid"]
})

# Detectar nulos, tipos y duplicados
issues = {
    0:[{"edad", ErrorTypes.TYPE}],
    1: [("edad", ErrorTypes.NULL), ("fecha", ErrorTypes.TYPE),("ciudad", ErrorTypes.NULL)],
    2: [("nombre", ErrorTypes.TYPE), ("fecha", ErrorTypes.TYPE)]
}


null_cleaner = NullCleaner(strategy="impute", impute_strategy="mode")
type_cleaner = TypeCleaner(type_mapping={"edad": int, "fecha":"datetime", "nombre": str })
dup_cleaner = DuplicateCleaner(strategy="drop_all")

data_cleaner = DataCleaner([null_cleaner, type_cleaner, dup_cleaner])
df_cleaned, report = data_cleaner.clean_all(df, issues)
print(df)
print(df_cleaned)
print(report)

