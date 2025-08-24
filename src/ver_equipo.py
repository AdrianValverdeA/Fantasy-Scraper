import os
import pandas as pd

def listar_equipos():
    archivos = []
    for equipo in os.listdir("Equipos"):
        if equipo.endswith(".csv"):
            archivos.append(equipo)
    if not archivos:
        print("No hay equipos disponibles. Vuelva al menu principal y crea uno en la seccion de 'Modificar equipo'.")
        
    return archivos

def ver_equipo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== VER EQUIPO ===")
    equipos = listar_equipos()
    for i, equipo in enumerate(equipos, 1):
        print(f"{i}. {equipo}")
    print("0. Volver al menu principal")

    while True:
        opcion = int(input("Selecciona un equipo: "))
        if opcion != 0:
            if 1 <= opcion <= len(equipos):
                ruta = os.path.join("Equipos", equipos[opcion-1])
                os.system('cls' if os.name == 'nt' else 'clear')
                df = pd.read_csv(ruta)
                if df.empty:
                    print("Equipo vacio.")
                else:
                    df["Hoy"] = (df["Hoy"].astype(str).str.replace(".", "").str.replace("+", "").astype(int))
                    df = df.sort_values(by="Hoy", ascending=False)
                    df["Hoy"] = df["Hoy"].apply(lambda x: f"{x:+,}".replace(",", "."))
                    df = df.reset_index(drop=True)
                    df.index = df.index + 1
                    print(df)
                input("Presione la tecla enter para continuar")
                break
            else:
                print("\nOpcion invalida.\n")
        else:
            break
