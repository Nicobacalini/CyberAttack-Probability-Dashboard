import customtkinter as ctk
import pandas as pd
from src.core.limpiar_datos import limpiar_dataframe
from src.core.estadisticas import (
    contar_ataques_por_hora,
    completar_horas_faltantes,
    calcular_min_max_ataques,
    calcular_probabilidades_ataques,
    calcular_esperanza,
    calcular_varianza,
    calcular_fda_discreta,
    regla_de_sturges,
    densidad_de_probabilidad,
    media_muestral,
    desviacion_muestral,
    calcular_probabilidades_continuas,
    calcular_probabilidad_umbral_discreto
)
from src.gui.componentes.pestana_1 import construir_pestaña_1

# Configuracion de estilo general de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StatsApp(ctk.CTk):
    def __init__(self, df):
        super().__init__()
        
        # Configuracion de la ventana principal
        self.title("Analisis Estadistico de Ciberataques - Trabajo Practico")
        self.geometry("1920x1080")
        self.minsize(1280, 720)
        
        # Procesamiento de los datos del dataset
        self.procesar_datos(df)
        
        # Inicializacion de los componentes de la interfaz
        self.inicializar_gui()
        
    def procesar_datos(self, df):
        # Fase de limpieza para Pestaña 1
        self.df_limpio = limpiar_dataframe(df)
        
        # --- PESTAÑA 1 ---
        self.ataques_por_hora_incompletos = contar_ataques_por_hora(self.df_limpio)
        self.ataques_por_hora = completar_horas_faltantes(self.ataques_por_hora_incompletos)
        
        self.min_max_ataques = calcular_min_max_ataques(self.ataques_por_hora)
        self.tabla_prob = calcular_probabilidades_ataques(self.ataques_por_hora)
        self.tabla_prob['FDA'] = calcular_fda_discreta(self.tabla_prob)
        
        self.esperanza = calcular_esperanza(self.tabla_prob)
        self.varianza = calcular_varianza(self.tabla_prob)
        
        self.k_elegido = 3
        self.prob_umbral_x = calcular_probabilidad_umbral_discreto(self.tabla_prob, self.k_elegido)
        
        self.n_intervalos = regla_de_sturges(self.df_limpio)
        self.densidad = densidad_de_probabilidad(self.df_limpio)
        self.media_muestral = media_muestral(self.df_limpio)
        self.desviacion_muestral = desviacion_muestral(self.df_limpio)
        
        self.prob_menor_media, self.prob_mayor_umbral, self.prob_menor_umbral = calcular_probabilidades_continuas(self.df_limpio)
        
        # Llamada al nuevo reporte por consola
        self.imprimir_reporte_consola()
        
    def imprimir_reporte_consola(self):
        print("\n" + "="*55)
        print(" REPORTE ESTADÍSTICO FINAL (RESUMEN)")
        print("="*55)
        
        print("\n--- VARIABLE DISCRETA (X: Ataques/hora) ---")
        print(f"Esperanza E[X]: {self.esperanza:.4f}")
        print(f"Varianza Var(X): {self.varianza:.4f}")
        print(f"P(X <= {self.k_elegido}): {self.prob_umbral_x:.4f} -> {(self.prob_umbral_x * 100):.2f}%")
        
        print("\n--- VARIABLE CONTINUA (Y: Packet Length) ---")
        print(f"Densidad de probabilidad f_Y(y): {self.densidad:.6f}")
        print(f"Media muestral (y_barra): {self.media_muestral:.2f} bytes")
        print(f"Desviación muestral (s): {self.desviacion_muestral:.2f} bytes")
        
        print("\n--- PROBABILIDADES CONTINUAS (Paso IV) ---")
        print(f"P(Y <= media): {self.prob_menor_media:.4f}")
        print(f"P(Y > media + s): {self.prob_mayor_umbral:.4f}")
        print(f"Porcentaje esperado < (media + s): {(self.prob_menor_umbral * 100):.2f}%")
        print("\n>>> INICIANDO INTERFAZ GRÁFICA... <<<")

    def inicializar_gui(self):
        # Frame contenedor principal
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Titulo de la aplicacion
        self.lbl_title = ctk.CTkLabel(
            self.main_container, 
            text="ANALISIS ESTADISTICO DE SEGURIDAD EN REDES", 
            font=("Consolas", 18, "bold")
        )
        self.lbl_title.pack(pady=(10, 5), padx=20, anchor="w")
        
        # Sistema de Pestañas (Tabview)
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(padx=10, pady=(5, 10), fill="both", expand=True)
        
        # Definicion de pestañas
        tab1_name = "Trabajo Practico"
        self.tabview.add(tab1_name)
        
        # Construccion de la pestaña
        self.construir_pestaña_1(tab1_name)

    def construir_pestaña_1(self, tab_name):
        construir_pestaña_1(self, tab_name)