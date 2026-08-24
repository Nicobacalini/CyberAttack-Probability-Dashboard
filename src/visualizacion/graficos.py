import numpy as np
from matplotlib.figure import Figure
from src.core.estadisticas import regla_de_sturges
import pandas as pd

# ==========================================
# CONFIGURACIÓN GLOBAL DE ESTILO (FUTURISTA/NEÓN)
# ==========================================
BG_COLOR = '#0F172A'       # Slate muy oscuro (Fondo principal)
TEXT_COLOR = '#E2E8F0'     # Gris claro azulado (Textos generales)
AXIS_COLOR = '#334155'     # Slate medio (Líneas de ejes)
GRID_COLOR = '#1E293B'     # Slate oscuro (Grillas secundarias)

# Paleta Neón / Cyber
CYAN_NEON = '#00F0FF'
PURPLE_NEON = '#B026FF'
BLUE_NEON = '#3B82F6'
ACCENT_RED = '#FF003C'

def _setup_axes(ax, title, xlabel, ylabel):
    """Aplica el estilo futurista común a todos los ejes."""
    ax.set_facecolor(BG_COLOR)
    ax.set_title(title, color=CYAN_NEON, fontsize=12, fontweight='bold', pad=15, loc='left')
    ax.set_xlabel(xlabel, color=TEXT_COLOR, fontsize=10, labelpad=10)
    ax.set_ylabel(ylabel, color=TEXT_COLOR, fontsize=10, labelpad=10)
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    
    # Solo mostrar ejes inferior e izquierdo para un look más limpio
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
        
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(AXIS_COLOR)
        ax.spines[spine].set_linewidth(1.5)
        
    ax.grid(True, linestyle='solid', alpha=0.3, color=GRID_COLOR)

# ==========================================
# FUNCIONES DE VISUALIZACIÓN / GRÁFICOS
# ==========================================

def graficar_probabilidades(tabla_prob):
    x_valores = tabla_prob['Cantidad de Ataques'].astype(str)
    probabilidades = tabla_prob['Probabilidad']
    
    # Ajustado figsize and dpi para resoluciones menores (1280x720)
    fig = Figure(figsize=(5.5, 3.5), dpi=100)
    fig.patch.set_facecolor(BG_COLOR)
    ax = fig.add_subplot(111)
    
    # Barras con borde brillante y transparencia
    ax.bar(x_valores, probabilidades, color=BLUE_NEON, edgecolor=CYAN_NEON, linewidth=1.5, alpha=0.7)
    _setup_axes(ax, 'DISTRIBUCIÓN DE MASA (POISSON)', 'ATAQUES POR HORA', 'PROBABILIDAD PUNTUAL')
    
    fig.tight_layout()
    return fig

def graficar_fda(df):
    if 'FDA' not in df.columns:
        df['FDA'] = df['Probabilidad'].cumsum()
    
    x_valores = df['Cantidad de Ataques']
    fda_valores = df['FDA']
    
    fig = Figure(figsize=(5.5, 3.5), dpi=100)
    fig.patch.set_facecolor(BG_COLOR)
    ax = fig.add_subplot(111)
    
    # Escalón con brillo neón morado
    ax.step(x_valores, fda_valores, where='post', color=PURPLE_NEON, linewidth=2.5)
    ax.scatter(x_valores, fda_valores, color=CYAN_NEON, zorder=3, s=40, edgecolor=BG_COLOR, linewidth=1.5)
    
    _setup_axes(ax, 'FUNCIÓN DE DISTRIBUCIÓN ACUMULADA', 'ATAQUES POR HORA', 'PROBABILIDAD ACUMULADA P(X≤x)')
    ax.set_ylim(-0.05, 1.05)
    
    fig.tight_layout()
    return fig

def graficar_histograma_y(df):
    fig = Figure(figsize=(5.5, 3.8), dpi=100)
    fig.patch.set_facecolor(BG_COLOR)
    ax = fig.add_subplot(111)
    
    bins_count = regla_de_sturges(df)
    ax.hist(df['Packet Length'], bins=bins_count, density=True, color=CYAN_NEON, edgecolor=BG_COLOR, alpha=0.6)
    
    min_val = df["Packet Length"].min()
    max_val = df["Packet Length"].max()
    density_val = 1.0 / (max_val - min_val) if max_val != min_val else 0.0
    
    # Línea de densidad teórica en contraste rojo/rosado
    ax.plot([min_val, max_val], [density_val, density_val], color=ACCENT_RED, linewidth=2.5, linestyle='--')
    
    _setup_axes(ax, 'DENSIDAD UNIFORME: PACKET LENGTH', 'TAMAÑO DE PAQUETE (BYTES)', 'DENSIDAD RELATIVA')
    
    fig.tight_layout()
    return fig
