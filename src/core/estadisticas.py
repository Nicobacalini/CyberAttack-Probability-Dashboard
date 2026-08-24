import pandas as pd
import math

# ==========================================
# FUNCIONES DE VARIABLE DISCRETA (X)
# ==========================================

def contar_ataques_por_hora(df):
    print("\n--- PASO 2: Agrupando por Hora ---")
    resultado = df.groupby('hour').size()
    print(f"Se encontraron {len(resultado)} horas con al menos 1 ataque.")
    return resultado

def completar_horas_faltantes(ataques_por_hora):
    print("\n--- PASO 3: Rellenando horas de paz (0 ataques) ---")
    rango_completo = pd.date_range(
        start=ataques_por_hora.index.min(),
        end=ataques_por_hora.index.max(),
        freq='h'
    )
    serie_completa = ataques_por_hora.reindex(rango_completo, fill_value=0)
    print(f"Horas totales analizadas (con y sin ataques): {len(serie_completa)} horas.")
    return serie_completa

def calcular_min_max_ataques(df):
    return {"min": df.min(), "max": df.max(), "unique": df.unique()}

def calcular_probabilidades_ataques(df_ataques_hora):
    print("\n--- PASO 4: Calculando Probabilidades p_X(x) ---")
    probabilidad = df_ataques_hora.value_counts(normalize=True).sort_index()
    
    suma_prob = probabilidad.sum()
    print(f"Verificacion -> Suma de probabilidades: {suma_prob:.4f}")

    if round(suma_prob, 4) != 1.0:
        print("Atencion: La suma de probabilidades no es 1.")

    tabla = probabilidad.reset_index()
    tabla.columns = ['Cantidad de Ataques', 'Probabilidad']
    return tabla

def calcular_esperanza(df):
    # E[X] = Σ x * p_X(x)
    esperanza = (df['Cantidad de Ataques'] * df['Probabilidad']).sum()
    return esperanza

def calcular_varianza(df):
    # Var(X) = E[X^2] - (E[X])^2
    esperanza_cuadrado = calcular_esperanza(df) ** 2
    esperanza_de_x_al_cuadrado = (df['Cantidad de Ataques'] ** 2 * df['Probabilidad']).sum()
    varianza = esperanza_de_x_al_cuadrado - esperanza_cuadrado
    return varianza

def calcular_fda_discreta(df):
    # F_X(x) = P(X <= x)
    return df['Probabilidad'].cumsum()

def calcular_probabilidad_umbral_discreto(df_probabilidades, k):
    """
    Calcula P(X <= k) de forma segura. Si k no existe exactamente en la muestra,
    toma el valor acumulado del escalón anterior, respetando la teoría de la FDA.
    """
    if 'FDA' not in df_probabilidades.columns:
        df_probabilidades['FDA'] = calcular_fda_discreta(df_probabilidades)
    
    # Filtramos todos los valores menores o iguales a k
    filtro = df_probabilidades[df_probabilidades['Cantidad de Ataques'] <= k]
    
    if filtro.empty:
        return 0.0  # k es menor al minimo de ataques
        
    # Retornamos el ultimo valor de FDA que cumple la condicion
    probabilidad_k = filtro['FDA'].iloc[-1]
    return probabilidad_k

# ==========================================
# FUNCIONES DE VARIABLE CONTINUA (Y)
# ==========================================

def regla_de_sturges(df):
    # k = 1 + 3.322 * log10(n)
    n = len(df) 
    return math.ceil(1 + 3.322 * math.log10(n))

def densidad_de_probabilidad(df):
    # f_Y(y) = 1 / (b - a)
    a = df["Packet Length"].min()
    b = df["Packet Length"].max()
    return 1 / (b - a)

def media_muestral(df):
    return df["Packet Length"].mean()

def desviacion_muestral(df):
    # Pandas usa n-1 por defecto, lo cual es correcto para el desvio muestral (s)
    return df["Packet Length"].std()

def fda_uniforme(y, df):
    # F_Y(y) evaluada por partes
    a = df["Packet Length"].min()
    b = df["Packet Length"].max()
    
    if y < a:
        return 0.0
    elif y > b:
        return 1.0
    else:
        return (y - a) / (b - a)

def calcular_probabilidades_continuas(df):
    media = media_muestral(df)
    desvio = desviacion_muestral(df)
    
    prob_menor_media = fda_uniforme(media, df)
    
    umbral_superior = media + desvio
    prob_mayor_umbral = 1 - fda_uniforme(umbral_superior, df)
    prob_menor_umbral = fda_uniforme(umbral_superior, df)
    
    return prob_menor_media, prob_mayor_umbral, prob_menor_umbral
