import pandas as pd

df = pd.read_csv("../data/raw/p4ds-base-para-facultad.csv")

print(f"Registros de entregas originales: {len(df)}")

df_sin_duplicados = df.drop_duplicates()

df_limpio = df_sin_duplicados.dropna()
df_limpio = df_sin_duplicados.dropna()
print(f"Registros de entregas limpios: {len(df_limpio)}")

ruta_guardado = "../data/processed/entregas_limpio.csv"
df_limpio.to_csv(ruta_guardado, index=False)

import pandas as pd

# 1. Cargamos el nuevo DataFrame de entregas
df = pd.read_csv("../data/raw/p4ds-base-para-facultad.csv")

# Limpiamos espacios ocultos en los nombres de las columnas si los hay
df.columns = df.columns.str.strip()

print("==================================================")
print("   EDA: DATASET DE LA PLATAFORMA DE ENTREGAS      ")
print("==================================================")


print("\n--- 1. Volumen de Datos (Filas, Columnas) ---")
print(df.shape)

print("\n--- 2. Registro de las primeras 3 filas ---")
print(df.head(3))

print("\n--- 3. Formato y tipo de dato de cada columna ---")
print(df.dtypes)

print("\n--- 4. Casilleros vacíos detectados por columna ---")
print(df.isnull().sum())

print("\n--- 5. Resumen estadístico de los identificadores ---")
print(df.describe())

print("\n--- 6. Conteo de tipos de movimientos registrados ---")
if 'payment_type' in df.columns:
    print(df['payment_type'].value_counts())
else:
    print("La columna 'payment_type' no fue encontrada.")


print("Fase 1 oka")


