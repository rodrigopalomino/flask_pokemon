import requests
import os


def descargar_img():
    # Asegurarse de que la carpeta exista
    if not os.path.exists("git"):
        os.makedirs("git")

    # Descargar las imágenes
    for x in range(1, 1034):
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{
            x}.gif"
        ruta_archivo = os.path.join("git", f"{x}.gif")

        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            with open(ruta_archivo, 'wb') as archivo:
                archivo.write(respuesta.content)
            print(f'Imagen {x}.png descargada y guardada en {ruta_archivo}')
        else:
            print(f'Error al descargar la imagen {
                  x}.png: {respuesta.status_code}')


# Ejemplo de uso
descargar_img()
