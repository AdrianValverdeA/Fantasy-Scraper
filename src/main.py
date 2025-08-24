import os
import time
from src import actualizar_mercado, modificar_equipo, ver_equipo, ver_mercado, buscar_jugador

def menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== MENU PRINCIPAL ===")
        print("1. Modificar equipo")
        print("2. Ver equipo")
        print("3. Ver mercado")
        print("4. Buscar jugador")
        print("5. Salir")

        opcion = input("Selecciona una opcion: ")

        if opcion == "1":
            modificar_equipo.modificar_equipo()
        elif opcion == "2":
            ver_equipo.ver_equipo()
        elif opcion == "3":
            ver_mercado.ver_mercado()
        elif opcion == "4":
            buscar_jugador.buscar_jugador()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opcion invalida.")
            time.sleep(1)

if __name__ == "__main__":
    os.makedirs("Equipos", exist_ok=True)
    actualizar_mercado.actualizar_mercado()
    menu()
    