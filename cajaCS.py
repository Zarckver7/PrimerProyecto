# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:34:55 2024

@author: ruizf
"""

import random
import requests

class cajaCS:
    url_api = "https://bymykel.github.io/CSGO-API/api/en/skins.json"

    traduccion_rareza = {
        "Consumer Grade": "Común",
        "Industrial Grade": "Poco común",
        "Mil-Spec Grade": "Rara",
        "Restricted": "Mítica",
        "Classified": "__*Legendaria*__",
        "Covert": "__**Ancestral**__",
        "Exceedingly Rare": "__***Extremadamente Raro***__"
    }
    
    traduccion_desgaste = {
        "Factory New": "__*New Factory*__",
        "Minimal Wear": "Casi Nuevo",
        "Field-Tested": "Algo Desgastado",
        "Well-Worn": "Bastante Desgastado",
        "Battle-Scarred": "Deplorable"
    }

    probabilidades_rareza = {
        "rarity_common_weapon": 79.92,  
        "rarity_uncommon_weapon": 15.98,  
        "rarity_rare_weapon": 3.2,  
        "rarity_mythical_weapon": 0.64,  
        "rarity_legendary_weapon": 0.32,  
        "rarity_ancient_weapon": 0.06  
    }
    
    probabilidades_desgaste = {
        "Factory New": 5.0,  
        "Minimal Wear": 10.0,  
        "Field-Tested": 30.0,  
        "Well-Worn": 30.0,  
        "Battle-Scarred": 25.0  
    }

    def __init__(self):
        self.armas = self.obtener_datos_api()

    def obtener_datos_api(self):
        try:
            respuesta = requests.get(self.url_api)
            respuesta.raise_for_status()  
            return respuesta.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los datos de la API: {e}")
            return []

    def elegir_rareza(self):
        total = sum(self.probabilidades_rareza.values())
        rand = random.uniform(0, total)
        acumulado = 0
        for rareza, prob in self.probabilidades_rareza.items():
            acumulado += prob
            if rand <= acumulado:
                return rareza
        return list(self.probabilidades_rareza.keys())[-1]  

    def filtrar_por_rareza(self, rareza):
        return [arma for arma in self.armas if arma["rarity"]["id"] == rareza]
    
    def elegir_desgaste(self):
       total = sum(self.probabilidades_desgaste.values())
       rand = random.uniform(0, total)
       acumulado = 0
       for desgaste, prob in self.probabilidades_desgaste.items():
           acumulado += prob
           if rand <= acumulado:
               return desgaste
       return list(self.probabilidades_desgaste.keys())[-1] 
    
    def abrir_caja(self):
        if not self.armas:
            print("No se pudo obtener los datos de las armas.")
            return

        rareza_seleccionada = self.elegir_rareza()
        armas_filtradas = self.filtrar_por_rareza(rareza_seleccionada)

        if not armas_filtradas:
            print("No se encontraron armas con la rareza seleccionada. Intentando de nuevo...")
            return self.abrir_caja()

        arma = random.choice(armas_filtradas)
        nombre_arma = arma["name"]
        rareza_arma = arma["rarity"]["name"]
        rareza_traduccion = self.traduccion_rareza.get(rareza_arma, rareza_arma)
        
        desgaste_seleccionado = self.elegir_desgaste()
        desgaste_traduccion = self.traduccion_desgaste.get(desgaste_seleccionado, desgaste_seleccionado)

        print("Ha salido:")
        print(f"Arma: {nombre_arma}")
        print(f"Rareza: {rareza_traduccion}")
        print(f"Desgaste: {desgaste_traduccion}")
        
        return {
          "nombre": nombre_arma,
          "rareza": rareza_traduccion,
          "desgaste": desgaste_traduccion
      }
