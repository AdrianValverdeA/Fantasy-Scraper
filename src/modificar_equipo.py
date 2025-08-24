import os
import time
import pandas as pd

os.system('cls' if os.name == 'nt' else 'clear')
def listar_equipos():
    archivos = []
    for equipo in os.listdir("Equipos"):
        if equipo.endswith(".csv"):
            archivos.append(equipo)

    return archivos

def seleccionar_equipo():
    os.system('cls' if os.name == 'nt' else 'clear')
    equipos = listar_equipos()
    print("\n=== MODIFICAR EQUIPO ===")
    for i, equipo in enumerate(equipos, 1):
        print(f"{i}. {equipo}")
    print(f"{len(equipos)+1}. Crear equipo")
    print("0. Volver al menu principal")
    while True:
        opcion = int(input("Selecciona un equipo: "))
        if opcion != 0:
            if opcion == len(equipos)+1:
                nombre = input("Nombre del nuevo equipo: ") + ".csv"
                ruta = os.path.join("Equipos", nombre)
                pd.DataFrame(columns=["Nombre","Hoy","Valor"]).to_csv(ruta, index=False, encoding="utf-8-sig")
                return ruta
            elif 1 <= opcion <= len(equipos):
                return os.path.join("Equipos", equipos[opcion-1])
            else:
                print("\nOpcion invalida.\n")
        else:
            return "a"
def mostrar_equipo(ruta):
    os.system('cls' if os.name == 'nt' else 'clear')
    df = pd.read_csv(ruta)
    if df.empty:
        print("Equipo vacio.")
    else:
        df["Hoy"] = (df["Hoy"].astype(str).str.replace(".", "").str.replace("+", "").astype(int))
        df = df.sort_values(by="Hoy", ascending=False)
        df["Hoy"] = df["Hoy"].apply(lambda x: f"{x:+,}".replace(",", "."))
        print(df.to_string(index=False))

def anadir_jugador(ruta):
    os.system('cls' if os.name == 'nt' else 'clear')
    jugadores = pd.read_csv("jugadores.csv")
    jugadores = jugadores.reset_index(drop=True)
    jugadores.index = jugadores.index + 1
    nombre = input("Nombre del jugador a buscar: ").lower()
    encontrados = jugadores[jugadores["Nombre"].str.lower().str.contains(nombre)]
    
    if encontrados.empty:
        print("No se encontraron jugadores.")
        time.sleep(1)
        return

    for i, row in encontrados.iterrows():
        print(f"{i}. {row['Nombre']}")
    print("0. Cancelar")

    idx = int(input("Selecciona el numero del jugador: "))
    if idx == 0:
        print("Operacion cancelada.")
        time.sleep(1)
        return

    if idx not in encontrados.index:
        print("Opcion invalida.")
        time.sleep(1)
        return

    jugador = jugadores.loc[idx]
    equipo = pd.read_csv(ruta)
    equipo = pd.concat([equipo, pd.DataFrame([jugador])], ignore_index=True)
    equipo.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"Jugador {jugador['Nombre']} agregado.")
    time.sleep(1)

def eliminar_jugador(ruta):
    os.system('cls' if os.name == 'nt' else 'clear')
    equipo = pd.read_csv(ruta)
    equipo = equipo.reset_index(drop=True)
    equipo.index = equipo.index + 1

    if equipo.empty:
        print("El equipo esta vacio.")
        time.sleep(1)
        return

    for i, row in equipo.iterrows():
        print(f"{i}. {row['Nombre']} ")
    print("0. Cancelar")

    idx = int(input("Selecciona el numero del jugador a eliminar: "))
    if idx == 0:
        print("Operacion cancelada.")
        return

    if idx not in equipo.index:
        print("Opcion invalida.")
        return

    jugador = equipo.loc[idx]
    equipo = equipo.drop(idx)
    equipo.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"Jugador {jugador['Nombre']} eliminado.")
    time.sleep(1)
    

def modificar_equipo():
    os.system('cls' if os.name == 'nt' else 'clear')
    ruta = seleccionar_equipo()
    while ruta!="a":
        mostrar_equipo(ruta)
        print("\n1. Agregar jugador")
        print("2. Eliminar jugador")
        print("3. Volver al menu principal")

        opcion = input("Opcion: ")
        if opcion == "1":
            anadir_jugador(ruta)
        elif opcion == "2":
            eliminar_jugador(ruta)
        elif opcion == "3":
            break
