import os
import pandas as pd

def ver_mercado():
    os.system('cls' if os.name == 'nt' else 'clear')
    if os.path.exists("jugadores.csv"):
        df = pd.read_csv("jugadores.csv")
        df["Hoy"] = (df["Hoy"].astype(str).str.replace(".", "").str.replace("+", "").astype(int))
        orden_desc = True
        df = df.sort_values(by="Hoy", ascending=not orden_desc).reset_index(drop=True)
        df["Hoy"] = df["Hoy"].apply(lambda x: f"{x:+,}".replace(",", "."))
    
        inicio = 0
        pag = 30
        while True:
            fin = inicio + pag
            print(df.iloc[inicio:fin][["Nombre","Hoy","Valor"]])
            opcion = input("\nPulsa 's' para ver mas, 'r' para invertir orden o 'x' para salir: ").lower()
            if opcion == "s":
                inicio += pag
                if inicio >= len(df):
                    print("No hay mas jugadores.")
                    break
            elif opcion == "r":           
                df["Hoy"] = (df["Hoy"].astype(str).str.replace(".", "").str.replace("+", "").astype(int))         
                orden_desc = not orden_desc
                df = df.sort_values(by="Hoy", ascending=not orden_desc)
                df["Hoy"] = df["Hoy"].apply(lambda x: f"{x:+,}".replace(",", "."))

                inicio = 0
            elif opcion == "x":
                break
    else:
        input("No tiene el archivo jugadores.csv. Reinicie")