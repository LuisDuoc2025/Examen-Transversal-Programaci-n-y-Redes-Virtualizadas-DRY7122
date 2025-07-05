import urllib.parse, urllib.request
import json

key = "cd6cbe40-aafa-4857-807a-f88cd92b43d4"
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

def obtener_coordenadas(ciudad):
    parametros = urllib.parse.urlencode({"q": ciudad, "limit": 1, "key": key})
    url = geocode_url + parametros
    respuesta = urllib.request.urlopen(url)
    datos = json.load(respuesta)

    if len(datos["hits"]) == 0:
        return None

    info = datos["hits"][0]
    pais = info.get("country", "")

    if pais not in ["Chile", "Argentina"]:
        return "FueraDeRegion"

    lat = info["point"]["lat"]
    lng = info["point"]["lng"]
    nombre = info["name"]
    return (lat, lng, nombre, pais)

while True:
    print("\n Calculador de Ruta entre Chile y Argentina")
    print("Escribe 's' en cualquier momento para salir.\n")

    # CIUDAD DE ORIGEN
    origen = input("Ciudad de Origen: ")
    if origen.lower() == "s":
        break
    origen_datos = obtener_coordenadas(origen)
    if origen_datos is None:
        print(" Ciudad no encontrada. Intenta de nuevo.")
        continue
    elif origen_datos == "FueraDeRegion":
        print("Solo se aceptan ciudades de Chile o Argentina.")
        continue

    # CIUDAD DE DESTINO
    destino = input("Ciudad de Destino: ")
    if destino.lower() == "s":
        break
    destino_datos = obtener_coordenadas(destino)
    if destino_datos is None:
        print("Ciudad no encontrada. Intenta de nuevo.")
        continue
    elif destino_datos == "FueraDeRegion":
        print("Solo se aceptan ciudades de Chile o Argentina.")
        continue

    # MEDIO DE TRANSPORTE
    print("\nTipos de transporte disponibles:")
    print("1 - auto")
    print("2 - bicicleta")
    print("3 - caminar")
    transporte = input("Selecciona el tipo de transporte (1/2/3): ")
    if transporte == "s":
        break
    elif transporte == "1":
        vehicle = "car"
    elif transporte == "2":
        vehicle = "bike"
    elif transporte == "3":
        vehicle = "foot"
    else:
        print("Opción no válida. Se usará 'car' por defecto.")
        vehicle = "car"

    # URL para la ruta
    p1 = f"&point={origen_datos[0]},{origen_datos[1]}"
    p2 = f"&point={destino_datos[0]},{destino_datos[1]}"
    params = {"key": key, "vehicle": vehicle, "locale": "es"}
    ruta_url = route_url + urllib.parse.urlencode(params) + p1 + p2

    # Petición a la API de rutas
    respuesta = urllib.request.urlopen(ruta_url)
    datos_ruta = json.load(respuesta)

    print("\n=================================================")
    print(f"Ruta desde {origen_datos[2]}, {origen_datos[3]} hasta {destino_datos[2]}, {destino_datos[3]}")
    print(f"Transporte: {vehicle}")
    print("=================================================")

    if datos_ruta.get("paths"):
        distancia_km = datos_ruta["paths"][0]["distance"] / 1000
        distancia_mi = distancia_km / 1.61
        tiempo_seg = datos_ruta["paths"][0]["time"] / 1000
        horas = int(tiempo_seg // 3600)
        minutos = int((tiempo_seg % 3600) // 60)
        segundos = int(tiempo_seg % 60)

        print(f"Distancia: {distancia_km:.2f} km / {distancia_mi:.2f} mi")
        print(f"Duración estimada: {horas:02}:{minutos:02}:{segundos:02}")
        print("=================================================")
        print(" Instrucciones del viaje:")
        for paso in datos_ruta["paths"][0]["instructions"]:
            texto = paso["text"]
            dist = paso["distance"] / 1000
            dist_mi = dist / 1.61
            print(f"- {texto} ({dist:.2f} km / {dist_mi:.2f} mi)")
        print("=================================================")
    else:
        print(" No se pudo calcular la ruta. Revisa los datos.")

    continuar = input("\n¿Deseas calcular otra ruta? (s para salir / Enter para continuar): ")
    if continuar.lower() == "s":
        print(" ¡Hasta luego!")
        break
