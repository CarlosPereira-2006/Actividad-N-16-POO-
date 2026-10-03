import json


class ArchivoServicio:
    def leer_json(self, ruta):
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar_json(self, ruta, datos):
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
