import pandas as pd

# ==========================================
# 1. FUNCIONES DE LIMPIEZA Y PREPARACIÓN
# ==========================================

def limpiar_dataframe(df):
    print("\n--- PASO 1: Limpieza de Datos ---")
    print(f"Dataframe original cargado con {len(df)} filas.")
    
    # filtramos solo las columnas que importan para el TP
    df_limpio = df[['Timestamp', 'Attack Type', 'Packet Length']].copy()
    
    # Convertimos el texto a un formato de fecha real que Python entienda
    df_limpio['Timestamp'] = pd.to_datetime(df_limpio['Timestamp'])
    
    # Magia para Poisson: Redondeamos los minutos y segundos a 00:00
    # Esto crea "ventanas" exactas de 1 hora.
    df_limpio['hour'] = df_limpio['Timestamp'].dt.floor('h')
    
    # Limpiamos cualquier fila que tenga datos vacíos (NaN)
    df_limpio = df_limpio.dropna()
    print(f"Dataframe limpio listo. Quedaron {len(df_limpio)} filas válidas.")

    return df_limpio
