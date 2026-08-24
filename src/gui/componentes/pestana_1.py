import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.visualizacion.graficos import graficar_probabilidades, graficar_fda, graficar_histograma_y

def construir_pestaña_1(app, tab_name):
    tab_frame = app.tabview.tab(tab_name)
    tab_frame.grid_rowconfigure(0, weight=1) # Fila superior para métricas
    tab_frame.grid_rowconfigure(1, weight=5) # Fila inferior para gráficos
    tab_frame.grid_columnconfigure(0, weight=1)
    
    # Contenedor superior de métricas (Cards)
    app.metrics_container = ctk.CTkFrame(tab_frame, fg_color="transparent")
    app.metrics_container.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="nsew")
    app.metrics_container.grid_rowconfigure(0, weight=1)
    app.metrics_container.grid_columnconfigure(0, weight=1, uniform="metric_col")
    app.metrics_container.grid_columnconfigure(1, weight=1, uniform="metric_col")
    app.metrics_container.grid_columnconfigure(2, weight=1, uniform="metric_col")
    
    # --- CARD 1: VARIABLE DISCRETA X ---
    card_x = ctk.CTkFrame(app.metrics_container)
    card_x.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    
    lbl_title_x = ctk.CTkLabel(
        card_x,
        text="Variable Discreta X - Cantidad de Ataques",
        font=("Consolas", 12, "bold"),
        text_color="#00F0FF",
        anchor="w"
    )
    lbl_title_x.pack(pady=(10, 5), padx=15, fill="x")
    
    ctk.CTkLabel(
        card_x, 
        text=f"• Esperanza E[X]: {app.esperanza:.4f} ataques/hora", 
        font=("Consolas", 11),
        anchor="w"
    ).pack(pady=2, padx=15, fill="x")
    
    ctk.CTkLabel(
        card_x, 
        text=f"• Varianza Var(X): {app.varianza:.4f}", 
        font=("Consolas", 11),
        anchor="w"
    ).pack(pady=2, padx=15, fill="x")
    
    ctk.CTkLabel(
        card_x, 
        text=f"• Probabilidad P(X <= {app.k_elegido}): {app.prob_umbral_x:.4f} ({app.prob_umbral_x * 100:.2f}%)", 
        font=("Consolas", 11),
        anchor="w"
    ).pack(pady=2, padx=15, fill="x")
    
    # --- CARD 2: VARIABLE CONTINUA Y - GENERAL ---
    card_y1 = ctk.CTkFrame(app.metrics_container)
    card_y1.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    
    lbl_title_y1 = ctk.CTkLabel(
        card_y1,
        text="Variable Continua Y - Longitud de Paquetes",
        font=("Consolas", 12, "bold"),
        text_color="#00F0FF",
        anchor="w"
    )
    lbl_title_y1.pack(pady=(10, 5), padx=15, fill="x")
    
    ctk.CTkLabel(
        card_y1, 
        text=f"• Intervalos (Sturges): {app.n_intervalos}", 
        font=("Consolas", 11),
        anchor="w"
    ).pack(pady=2, padx=15, fill="x")
    
    ctk.CTkLabel(
        card_y1, 
        text=f"• Densidad f_Y(y): {app.densidad:.6f}", 
        font=("Consolas", 11),
        anchor="w"
    ).pack(pady=2, padx=15, fill="x")
    
    ctk.CTkLabel(
        card_y1, 
        text=f"• Media Muestral (y_barra): {app.media_muestral:.2f} bytes", 
        font=("Consolas", 11),
        anchor="w"
    ).pack(pady=2, padx=15, fill="x")
    
    ctk.CTkLabel(
        card_y1, 
        text=f"• Desviación Muestral (s): {app.desviacion_muestral:.2f} bytes", 
        font=("Consolas", 11),
        anchor="w"
    ).pack(pady=2, padx=15, fill="x")
    
    # --- CARD 3: VARIABLE CONTINUA Y - PROBABILIDADES ---
    card_y2 = ctk.CTkFrame(app.metrics_container)
    card_y2.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
    
    lbl_title_y2 = ctk.CTkLabel(
        card_y2,
        text="Variable Continua Y - Longitud de Paquetes",
        font=("Consolas", 12, "bold"),
        text_color="#00F0FF",
        anchor="w"
    )
    lbl_title_y2.pack(pady=(10, 5), padx=15, fill="x")
    
    ctk.CTkLabel(
        card_y2, 
        text=f"• Probabilidad P(Y <= media): {app.prob_menor_media:.4f} ({app.prob_menor_media * 100:.2f}%)", 
        font=("Consolas", 11),
        anchor="w"
    ).pack(pady=2, padx=15, fill="x")
    
    ctk.CTkLabel(
        card_y2, 
        text=f"• Probabilidad P(Y > media + s): {app.prob_mayor_umbral:.4f} ({app.prob_mayor_umbral * 100:.2f}%)", 
        font=("Consolas", 11),
        anchor="w"
    ).pack(pady=2, padx=15, fill="x")
    
    # Contenedor inferior de gráficos (Side-by-Side)
    app.graphs_container = ctk.CTkFrame(tab_frame, fg_color="transparent")
    app.graphs_container.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    app.graphs_container.grid_rowconfigure(0, weight=1)
    app.graphs_container.grid_columnconfigure(0, weight=1, uniform="graph_col")
    app.graphs_container.grid_columnconfigure(1, weight=1, uniform="graph_col")
    app.graphs_container.grid_columnconfigure(2, weight=1, uniform="graph_col")
    
    # Gráfico 1: Masa de Probabilidad Discreta
    fig_prob = graficar_probabilidades(app.tabla_prob)
    canvas_prob = FigureCanvasTkAgg(fig_prob, master=app.graphs_container)
    canvas_prob.draw()
    canvas_prob.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    
    # Gráfico 2: FDA Discreta
    fig_fda = graficar_fda(app.tabla_prob)
    canvas_fda = FigureCanvasTkAgg(fig_fda, master=app.graphs_container)
    canvas_fda.draw()
    canvas_fda.get_tk_widget().grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    
    # Gráfico 3: Histograma Y
    fig_hist = graficar_histograma_y(app.df_limpio)
    canvas_hist = FigureCanvasTkAgg(fig_hist, master=app.graphs_container)
    canvas_hist.draw()
    canvas_hist.get_tk_widget().grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
