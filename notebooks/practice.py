import pandas as pd

# Cargar la base de la facultad
df = pd.read_csv("../data/raw/p4ds-base-para-facultad.csv")
print(f"Total original: {len(df)}")

# Limpieza rápida de columnas y duplicados
df.columns = df.columns.str.strip()
df_limpio = df.drop_duplicates().dropna()
print(f"Total limpio: {len(df_limpio)}")

# Guardar
df_limpio.to_csv("../data/processed/entregas_limpio.csv", index=False)

# --- REVISIÓN RÁPIDA (EDA) ---
print("--- Info general ---")
print(f"Dimensiones: {df.shape}")

print("\n--- Primeras filas ---")
print(df.head(3))

print("\n--- Tipos y nulos ---")
print(df.dtypes)
print("\nNulos por columna:")
print(df.isnull().sum())

print("\n--- Estadísticas ---")
print(df.describe())

# payment_type por si cambia el nombre
if "payment_type" in df.columns:
    print("\n--- Tipos de pago ---")
    print("\n--- Tipos de pago ---")
    print(df["payment_type"].value_counts())

