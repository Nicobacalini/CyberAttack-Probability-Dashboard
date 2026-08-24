import pandas as pd
from src.gui.app import StatsApp

if __name__ == "__main__":
    # Cargar los datos desde el directorio correspondiente
    df = pd.read_csv("data/cybersecurity_attacks.csv")
    
    # Iniciar la aplicacion grafica principal
    app = StatsApp(df)
    app.mainloop()