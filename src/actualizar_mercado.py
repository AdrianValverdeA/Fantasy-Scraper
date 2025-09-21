import pandas as pd
import os
import time
from urllib import request, parse, error

os.system('cls' if os.name == 'nt' else 'clear')
def actualizar_mercado():
    print("\n# Actualizando mercado #")
    url = "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado"

    r = request.urlopen(url)
    data = r.read().decode("utf-8")
    jugadores = []
    valorAux = '0'
    valor = '0'
    
    for linea in data.splitlines()[450:]:
        if ('strong class="m-auto columna_diferencia columna_diferencia1"><span class="analytics-up"' in linea) or ('strong class="m-auto columna_diferencia columna_diferencia1"><span class="analytics-down"' in linea):
            hoy = linea.split('>')[2].split('<')[0]
            
        if '<strong class="m-auto columna_diferencia columna_diferencia1">0</strong>' in linea:
            hoy = '0'
            
        if '<span class="d-none d-lg-block">' in linea:
            nombre = linea.split('>')[2].split('<')[0]

        if 'data-nombre=' in linea:  
            dnombre = linea.split('"')[1].split('"')[0]
            dnombre = dnombre.replace(" ", "-")
            

        if '<span class="m-auto">' in linea and not 'c2' in linea:
            valor = linea.split('>')[1].split('<')[0]
        if (valorAux != valor):

            jugadores.append({
                "Nombre": nombre,
                "Hoy": hoy,
                "Valor": valor,
                "D-Nombre": dnombre
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
    if "Titularidad" not in jugadores.columns:
        jugadores["Titularidad"] = ""
    for equipo in archivos:
        rutaEquipo = os.path.join("Equipos", equipo)
        jugadoresEquipo = pd.read_csv(rutaEquipo)

        nuevosJugadores = []
        for _, row in jugadoresEquipo.iterrows():
            nombre = row["Nombre"]
            actualizado = jugadores[jugadores["Nombre"].str.lower() == nombre.lower()].copy()
            dnombre = jugadores.loc[jugadores["Nombre"].str.lower() == nombre.lower(), "D-Nombre"]
            if not dnombre.empty:
                dnombre = dnombre.iloc[0]
                link_porcen = "https://www.futbolfantasy.com/jugadores/" + dnombre
                link_porcen_safe = parse.quote(link_porcen, safe=":/")
            else:
                dnombre = None
                link_porcen_safe = None
            if link_porcen_safe:
                try:
                    rp = request.urlopen(link_porcen_safe)
                    datap = rp.read().decode("utf-8")
                    titularidad=""
                    i = 0;
                    for lineap in datap.splitlines()[540:590]:

                        if '<span class="mx-auto prob-' in lineap:
                            titularidad = lineap.split('>')[1].split('<')[0]
                            break
                    if titularidad=="":
                         titularidad="Jornada realizada"
                except error.HTTPError as e:
                    if e.code == 404:
                        titularidad = "Error"
                    else:
                        raise
            else:
                titularidad = "Error"

            actualizado.loc[actualizado["Nombre"].str.lower() == nombre.lower(),"Titularidad"] = titularidad

            if not actualizado.empty:
                nuevosJugadores.append(actualizado.iloc[0])
            else:
                nuevosJugadores.append(row)
            
        dfAux = pd.DataFrame(nuevosJugadores)
        dfAux["Hoy"] = (dfAux["Hoy"].astype(str).str.replace(".", "").str.replace("+", "").astype(int))
        dfAux = dfAux.sort_values(by="Hoy", ascending=False)
        dfAux["Hoy"] = dfAux["Hoy"].apply(lambda x: f"{x:+,}".replace(",", "."))
        if "vInicial" not in dfAux.columns:
            dfAux["vInicial"] = dfAux["Valor"]
        
        if "Beneficio" not in dfAux.columns:
            dfAux["Beneficio"] = '0'
        
        if "vInicial" not in jugadoresEquipo.columns:
            jugadoresEquipo["vInicial"] = jugadoresEquipo["Valor"]
        
        if "Beneficio" not in jugadoresEquipo.columns:
            jugadoresEquipo["Beneficio"] = '0'
        
        dfAux["vInicial"] = dfAux["vInicial"].fillna('0')
        jugadoresEquipo["vInicial"] = jugadoresEquipo["vInicial"].fillna('0')
        dfAux["Beneficio"] = dfAux["Beneficio"].fillna('0')
        jugadoresEquipo["Beneficio"] = jugadoresEquipo["Beneficio"].fillna('0')
        

        for _, a in dfAux.iterrows():
            nombre = a["Nombre"]
            dfAux.loc[dfAux["Nombre"] == nombre, "vInicial"] = jugadoresEquipo.loc[jugadoresEquipo["Nombre"] == nombre, "vInicial"].values[0]
            dfAux.loc[dfAux["Nombre"] == nombre, "Beneficio"] = jugadoresEquipo.loc[jugadoresEquipo["Nombre"] == nombre, "Beneficio"].values[0]


        dfAux.to_csv(rutaEquipo, index=False, encoding="utf-8-sig")
    
    print("\n# Mercado actualizado correctamente #\n")
    time.sleep(1.5)