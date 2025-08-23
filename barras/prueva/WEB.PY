import requests
from bs4 import BeautifulSoup
import os

# URL de la página
URL = "https://www.softecpharma.com/farmamiperu/mantenimiento/productos/add"

# Carpeta de salida
os.makedirs("pagina_descargada", exist_ok=True)

# Descargar la página
response = requests.get(URL)
if response.status_code == 200:
    html_content = response.text

    # Guardar el HTML original
    with open("pagina_descargada/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # Parsear con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Buscar todos los enlaces a CSS
    css_links = soup.find_all("link", rel="stylesheet")

    for i, link in enumerate(css_links, start=1):
        css_url = link.get("href")
        if css_url and css_url.startswith("http"):
            css_response = requests.get(css_url)
            if css_response.status_code == 200:
                css_filename = f"pagina_descargada/style_{i}.css"
                with open(css_filename, "w", encoding="utf-8") as f:
                    f.write(css_response.text)
                print(f"CSS guardado en {css_filename}")
else:
    print("Error al descargar la página:", response.status_code)
