import os
import pandas as pd

def buscar_jugador():
    os.system('cls' if os.name == 'nt' else 'clear')
    if os.path.exists("jugadores.csv"):
        jugadores = pd.read_csv("jugadores.csv")
        nombre = input("Nombre del jugador a buscar: ").lower()
        encontrados = jugadores[jugadores["Nombre"].str.lower().str.contains(nombre)]

        if encontrados.empty:
            print("No se encontraron jugadores.")
        else:
            for i, row in encontrados.iterrows():
                print(f"{i}. {row['Nombre']} - Hoy: {row['Hoy']} - Valor: {row['Valor']}")
        input("Presione la tecla enter para continuar")
    
