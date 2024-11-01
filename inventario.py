# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:22:40 2024

@author: ruizf
"""

import json
import os

class inventarioCS:
    def __init__(self, archivo="inventario.json"):
        self.archivo = archivo
        self.armas = self.cargar_armas()

    def cargar_armas(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def obtener_siguiente_id(self):
        if not self.armas:
            return 1
        
        return max(arma["Id"] for arma in self.armas) + 1

    def agregar_arma(self, nombre, rareza, desgaste):
        valor = self.calcular_precio_arma(rareza, desgaste)
        nuevo_objeto = {
            "Id": self.obtener_siguiente_id(),  
            "Nombre": nombre,
            "Rareza": rareza,
            "Desgaste": desgaste,
            "Valor": valor
        }
        self.armas.append(nuevo_objeto)
        self.guardar_armas()

    def guardar_armas(self):
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(self.armas, f, ensure_ascii=False, indent=4)

    def mostrar_armas(self):
        if not self.armas:
            print("No has abierto ninguna caja aún.")
            return

        for arma in self.armas:
            print(f"ID: {arma['Id']}, Nombre: {arma['Nombre']}, Rareza: {arma['Rareza']}, Desgaste: {arma['Desgaste']}, Valor: {arma['Valor']}€")

    def calcular_precio_arma(self, rareza, desgaste):
        precios_rareza = {
            "Común": 1,
            "Poco común": 5,
            "Rara": 20,
            "Mítica": 100,
            "__*Legendaria*__": 500,
            "__**Ancestral**__": 2000,
            "__***Extremadamente Raro***__": 10000
        }
        precios_desgaste = {
            "Deplorable": 0.5,
            "Bastante Desgastado": 0.75,
            "Algo Desgastado": 1,
            "Casi Nuevo": 1.5,
            "New Factory": 2
        }
        precio_base = precios_rareza.get(rareza, 1)
        multiplicador_desgaste = precios_desgaste.get(desgaste, 1)
        return precio_base * multiplicador_desgaste

    def vender_inventario(self):
        total_venta = sum(arma["Valor"] for arma in self.armas)
        self.armas.clear()  
        self.guardar_armas()  
        return total_venta
    
    
    def vender_arma_por_id(self, id_arma):
        for arma in self.armas:
            if arma["Id"] == id_arma:
                valor_arma = arma["Valor"]
                self.armas.remove(arma)  
                self.guardar_armas()  
                return valor_arma
        print("Arma no encontrada.")
        return 0  
