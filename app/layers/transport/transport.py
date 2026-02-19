# capa de transporte/comunicación con otras interfaces o sistemas externos.

import requests
from ...config import config

# comunicación con la REST API.
# este método se encarga de "pegarle" a la API y traer una lista de objetos JSON.
def getAllImages():
    response = requests.get(config.SIMPSONS_CHARACTERS_URL)
    json_data = response.json()
    
    json_collection = []
    
    if 'results' in json_data:
        for character in json_data['results']:
            if character.get('portrait_path'):
                json_collection.append(character)
    
    return json_collection