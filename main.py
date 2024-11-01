# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:34:55 2024

@author: ruizf
"""

# main.py

import csv
from cajaCS import cajaCS
from inventario import inventarioCS

def mostrar_menu():
    print("\nMenu:")
    print("1. Abrir caja")
    print("2. Ver armas obtenidas")
    print("3. Vender inventario completo")
    print("4. Vender arma específica por ID")
    print("5. Salir")

def crear_csv(cartera_inicial, cartera_final, gastos, ganancias, inventario):
    profit = ganancias - gastos
    with open("registro_cartera.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Cartera Inicial", "Cartera Final", "Gastos Totales", "Ganancias Totales", "Profit"])
        writer.writerow([cartera_inicial, cartera_final, gastos, ganancias, profit])
        
        writer.writerow([])
        writer.writerow(["Inventario Final"])
        writer.writerow(["ID", "Nombre", "Rareza", "Desgaste", "Valor"])
        
        for arma in inventario.armas:
            writer.writerow([arma["Id"], arma["Nombre"], arma["Rareza"], arma["Desgaste"], arma["Valor"]])

def main():
    inventario = inventarioCS()
    caja = cajaCS()
    cartera = 100  
    cartera_inicial = cartera
    gastos = 0
    ganancias = 0

    while True:
        print(f"\nCartera: {cartera}€")
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            if cartera >= 5:
                cartera -= 5  
                gastos += 5
                arma = caja.abrir_caja()
                if arma:
                    inventario.agregar_arma(arma["nombre"], arma["rareza"], arma["desgaste"])
                    print("Arma añadida al inventario.")
            else:
                print("No tienes suficiente dinero para abrir una caja.")
        elif opcion == "2":
            print("\nArmas obtenidas:")
            inventario.mostrar_armas()
        elif opcion == "3":
            total_venta = inventario.vender_inventario()
            ganancias += total_venta
            cartera += total_venta
            print(f"Has vendido todo tu inventario por {total_venta}€. Cartera actualizada.")
        elif opcion == "4":
            try:
                id_arma = int(input("Introduce el ID del arma que deseas vender: "))
                valor_arma = inventario.vender_arma_por_id(id_arma)
                if valor_arma > 0:
                    cartera += valor_arma
                    ganancias += valor_arma
                    print(f"Arma vendida por {valor_arma}€. Cartera actualizada.")
                else:
                    print("No se pudo vender el arma.")
            except ValueError:
                print("ID inválido. Por favor ingresa un número.")
        elif opcion == "5":
            crear_csv(cartera_inicial, cartera, gastos, ganancias, inventario)
            print("Registro guardado en 'registro_cartera.csv'. Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
