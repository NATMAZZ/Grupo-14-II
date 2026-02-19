# capa de servicio/lógica de negocio

import random
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from django.db import IntegrityError

def getAllImages():
    coleccion=transport.getAllImages()
    cards=[]

    for personaje in coleccion:
        carta=translator.fromRequestIntoCard(personaje)
        if carta.phrases:
            frase_random= random.choice(carta.phrases)
            carta.phrases=[frase_random]
        cards.append(carta)
    return cards
    """
    Obtiene todas las imágenes de personajes desde la API y las convierte en objetos Card.
    
    Esta función debe obtener los datos desde transport, transformarlos en Cards usando 
    translator y retornar una lista de objetos Card.
    """
    pass

def filterByCharacter(name):
    """
    Filtra las cards de personajes según el nombre proporcionado.
    Se debe filtrar los personajes cuyo nombre contenga el parámetro recibido. Retorna una lista de Cards filtradas.
    """
    cards = getAllImages() #Obtiene todas las cards.
    filtradas = [] 
    for carta in cards: #Se recorre cada una de las cartas.
        if name.lower() in carta.name.lower(): #name sale de translator.py 
            filtradas.append(carta) #Si el nombre de la card coincide con el parametro buscado, la misma se agrega a la lista.
    return filtradas # Se devuelve la lista generada.

def filterByStatus(status_name):
    """
    Filtra las cards de personajes según su estado (Alive/Deceased).
    Se deben filtrar los personajes que tengan el estado igual al parámetro 'status_name'. Retorna una lista de Cards filtradas.
    """
    cards = getAllImages() #Obtiene todas las cards.
    filtradas = []
    for carta in cards: # Se recorrecada una de las cartas.
        if carta.status == status_name: #Si el estado buscado coincide con el estado dentro de la card, se agrega a la lista. 
            filtradas.append(carta) 
    return filtradas #Se devuelve la lista generada.


def saveFavourite(request):
    try:
        fav = translator.fromTemplateIntoCard(request)  #Se transforma el request en una Card usando el translator.
        fav.user = get_user(request) #Se asigna el usuario actual a la Card.
        return repositories.saveFavourite(fav) #Se guarda la Card en el repositorio y se retorna el resultado.
    except IntegrityError:
        return None #si el personaje ya es un favorito, devuelve None y en la vista se vera el mensaje que definimos para este caso.

    """
    Guarda un favorito en la base de datos.
    Se deben convertir los datos del request en una Card usando el translator,
    asignarle el usuario actual, y guardarla en el repositorio.
    """
    
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request) # Obtener el usuario actual desde el request

        favourite_list= repositories.getAllFavourites(user)# Busca desde el repositorio los favoritos del usuario (User).
        mapped_favourites = [] # Se crea una lista vacía para almacenar los favoritos transformados en Cards.

        for fav in favourite_list: # Se itera sobre cada favorito obtenido del repositorio.
            card = translator.fromRepositoryIntoCard(fav) # Se transforma cada favorito en una Card usando el translator. 
            mapped_favourites.append(card) # Se agrega la Card a la lista de favoritos transformados.

        return mapped_favourites # Se retorna la lista de Cards que representan los favoritos del usuario.
    """
    Obtiene todos los favoritos del usuario autenticado.
    Si el usuario está autenticado, se deben obtener sus favoritos desde el repositorio,
    transformarlos en Cards usando translator y retornar la lista. Si no está autenticado, se retorna una lista vacía.
    """
    
def deleteFavourite(request):
    favId = request.POST.get('id') # Se obtiene el ID del favorito a eliminar desde el POST del request.
    return repositories.deleteFavourite(favId) # Se llama al repositorio para eliminar el favorito con el ID obtenido y se retorna el resultado.
    
    """
    Elimina un favorito de la base de datos.
    Se debe obtener el ID del favorito desde el POST y eliminarlo desde el repositorio.

    """

