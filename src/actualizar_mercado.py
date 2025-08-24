import pandas as pd
import os
import time
from urllib import request

os.system('cls' if os.name == 'nt' else 'clear')
def actualizar_mercado():
    print()
    print("# Actualizando mercado #")
    url = "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado"

    r = request.urlopen(url)
    data = r.read().decode("utf-8")
    jugadores = []
    valorAux = '0'
    valor = '0'
    
    for linea in data.splitlines():

        if ('strong class="m-auto columna_diferencia columna_diferencia1"><span class="analytics-up"' in linea) or ('strong class="m-auto columna_diferencia columna_diferencia1"><span class="analytics-down"' in linea):
            hoy = linea.split('>')[2].split('<')[0]
            
        if '<strong class="m-auto columna_diferencia columna_diferencia1">0</strong>' in linea:
            hoy = 0
            
        if '<span class="d-none d-lg-block">' in linea:
            nombre = linea.split('>')[2].split('<')[0]
            
        if '<span class="m-auto">' in linea and not 'c2' in linea:
            valor = linea.split('>')[1].split('<')[0]
        if (valorAux != valor): 
            jugadores.append({
                "Nombre": nombre,
                "Hoy": hoy,
                "Valor": valor
            })
            valorAux = valor
        
    df = pd.DataFrame(jugadores)
    df.to_csv("jugadores.csv", index = False)
    
    ##Equipos##
    archivos = []
    for equipo in os.listdir("Equipos"):
        if equipo.endswith(".csv"):
            archivos.append(equipo)
    jugadores = pd.read_csv("jugadores.csv")
    
    for equipo in archivos:
        rutaEquipo = os.path.join("Equipos", equipo)
        jugadoresEquipo = pd.read_csv(rutaEquipo)
        
        nuevosJugadores = []
        for _, row in jugadoresEquipo.iterrows():
            nombre = row["Nombre"]
            actualizado = jugadores[jugadores["Nombre"].str.lower() == nombre.lower()]
            if not actualizado.empty:
                nuevosJugadores.append(actualizado.iloc[0])
            else:
                nuevosJugadores.append(row)
        dfAux = pd.DataFrame(nuevosJugadores)
        dfAux["Hoy"] = (dfAux["Hoy"].astype(str).str.replace(".", "").str.replace("+", "").astype(int))
        dfAux = dfAux.sort_values(by="Hoy", ascending=False)
        dfAux["Hoy"] = dfAux["Hoy"].apply(lambda x: f"{x:+,}".replace(",", "."))
        dfAux.to_csv(rutaEquipo, index=False, encoding="utf-8-sig")
    
    print()
    print("# Mercado actualizado correctamente #")
    print()
    
    time.sleep(1.5)