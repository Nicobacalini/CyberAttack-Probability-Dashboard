# 🛡️ Análisis Estadístico de Ciberataques

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-00F0FF?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Plots-Matplotlib-11557C?style=for-the-badge)

Aplicación de escritorio interactiva con estética **Futurista/Neón** desarrollada en Python para el procesamiento, análisis probabilístico y visualización estadística de eventos de ciberseguridad a partir de un conjunto de datos masivo.

Este proyecto fue desarrollado en el marco de la asignatura **Probabilidad y Estadística** para la carrera **Analista en Sistemas**.

---

## 📋 Tabla de Contenidos
- [Descripción General](#-descripción-general)
- [Fundamento Teórico y Funcionalidades](#-fundamento-teórico-y-funcionalidades)
  - [Variable Discreta ($X$): Frecuencia de Ataques](#1-variable-discreta-x---cantidad-de-ataques-por-hora)
  - [Variable Continua ($Y$): Tamaño de Paquetes](#2-variable-continua-y---longitud-de-paquetes-packet-length)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Requisitos e Instalación](#-requisitos-e-instalación)
- [Uso y Ejecución](#-uso-y-ejecución)
- [Dataset](#-dataset)

---

## 🔍 Descripción General

La herramienta procesa registros de red (*logs*) para evaluar patrones de ciberataques (como DDoS, Malware e Intrusiones). Realiza la limpieza de datos, agrupa temporalmente los eventos en intervalos por hora (contemplando periodos sin ataques) y calcula parámetros estadísticos fundamentales tanto para variables aleatorias discretas como continuas, integrando gráficos interactivos en una interfaz gráfica moderna.

---

## 📐 Fundamento Teórico y Funcionalidades

### 1. Variable Discreta ($X$): Cantidad de Ataques por Hora
Representa la cantidad de ataques detectados en ventanas temporales continuas de 1 hora.
- **Limpieza y Completitud**: Rellena automáticamente los intervalos u "horas de paz" con 0 ataques para mantener la rigurosidad estadística del proceso de Poisson / masa discreta.
- **Función de Masa de Probabilidad $p_X(x)$**: Distribución de frecuencias relativas.
- **Esperanza Matemática $E[X]$**:
  $$E[X] = \sum x \cdot p_X(x)$$
- **Varianza $Var(X)$**:
  $$Var(X) = E[X^2] - (E[X])^2$$
- **Función de Distribución Acumulada (FDA) $F_X(x)$**:
  $$F_X(x) = P(X \le x)$$
- **Evaluación de Umbrales**: Cálculo probabilístico de eventos acumulados $P(X \le k)$ (por defecto $k = 3$).

### 2. Variable Continua ($Y$): Longitud de Paquetes (`Packet Length`)
Representa el tamaño en bytes del paquete de red involucrado en el ataque.
- **Regla de Sturges**: Determinación óptima del número de intervalos para el histograma:
  $$k = \lceil 1 + 3.322 \cdot \log_{10}(n) \rceil$$
- **Función de Densidad de Probabilidad Uniforme $f_Y(y)$**:
  $$f_Y(y) = \frac{1}{b - a} \quad \text{para } a \le y \le b$$
- **Parámetros Muestrales**: Media muestral ($\bar{y}$) y Desviación estándar muestral ($s$).
- **Cálculo de Probabilidades Acumuladas**: Evaluación de eventos en la distribución uniforme como $P(Y \le \bar{y})$ y $P(Y > \bar{y} + s)$.

---

## 🏗️ Arquitectura del Proyecto

El código está organizado de forma modular separando la lógica de datos, los modelos estadísticos y la capa de presentación:

```text
trabajo practico/
├── data/
│   └── cybersecurity_attacks.csv   # Dataset con eventos de red y ciberataques
├── src/
│   ├── core/
│   │   ├── limpiar_datos.py        # Parsing de timestamp y filtrado de datos
│   │   └── estadisticas.py         # Fórmulas de E[X], Var(X), Sturges, FDA y Densidad
│   ├── gui/
│   │   ├── app.py                  # Clase principal de la GUI (CustomTkinter)
│   │   └── componentes/
│   │       └── pestana_1.py        # Renderizado de tarjetas KPI y contenedores
│   └── visualizacion/
│       └── graficos.py             # Generación de plots Matplotlib estilo Neón/Slate
├── main.py                         # Punto de entrada de la aplicación
├── requirements.txt                # Lista de dependencias del proyecto
└── README.md                       # Documentación del proyecto
```

---

## 💻 Requisitos e Instalación

### Prerrequisitos
- **Python 3.9** o superior.

### Pasos de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <URL_DEL_REPOSOTORIO>
   cd "trabajo practico"
   ```

2. **Crear y activar un entorno virtual (opcional pero recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   # venv\Scripts\activate   # En Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Uso y Ejecución

Para iniciar la aplicación, ejecuta el archivo principal `main.py`:

```bash
python main.py
```

Al ejecutarse:
1. Se muestra un **Reporte Estadístico Resumido** en la consola de comandos.
2. Se despliega la **Interfaz Gráfica de Usuario (GUI)** en modo oscuro con tres gráficos interactivos integrados:
   - **Distribución de Masa de Probabilidad (Poisson / Discreta)** (Gráfico de Barras).
   - **Función de Distribución Acumulada (FDA)** (Gráfico Escalonado).
   - **Histograma de Densidad Uniforme** (Longitud de paquetes con densidad teórica superpuesta).

---

## 📊 Dataset

El archivo dataset de entrada se encuentra en `data/cybersecurity_attacks.csv`.
Contiene registros detallados de tráfico de red, de los cuales se extraen las variables clave:
- `Timestamp`: Marca temporal para calcular la tasa de ataques por hora ($X$).
- `Packet Length`: Tamaño del paquete en bytes ($Y$).
- `Attack Type`: Tipo de ataque detectado (DDoS, Malware, Intrusion).
