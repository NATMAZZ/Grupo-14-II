# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages 
from django.core.mail import send_mail 
from django.contrib.auth.models import User
from django.conf import settings



def index_page(request):
    return render(request, 'index.html')

def home(request):
    """
    Vista principal que muestra la galería de personajes de Los Simpsons.
    Esta función debe obtener el listado de imágenes desde la capa de servicios
    y también el listado de favoritos del usuario, para luego enviarlo al template 'home.html'.
    Recordar que los listados deben pasarse en el contexto con las claves 'images' y 'favourite_list'.
    """
    images = services.getAllImages()  #Se usa para obtener todas las imágenes de los personajes.
    
    if request.user.is_authenticated: # Se verifica si el usuario está autenticado.
        favourite_list = services.getAllFavourites(request) # Se obtiene la lista de favoritos del usuario autenticado.
        favourite_names = [fav.name for fav in favourite_list] # Se crea una lista con los nombres de los favoritos para facilitar su uso en el template.

    else:
        favourite_list = [] # Si el usuario no está autenticado, se asigna una lista vacía a favourite_list.   
        favourite_names = [] # Se crea una lista vacía para almacenar los nombres de los favoritos.

    return render(request, 'home.html', { 
        'images': images, 
        'favourite_list': favourite_list, 
        'favourite_names': favourite_names 
    }) # Se renderiza el template 'home.html' pasando el listado de imágenes y favoritos en el contexto.


def search(request):
        query = request.POST.get('query') # Se obtiene el valor ingresado por el usuario.
    if not query: # Si no se ingresa ningun dato, se redirige al home.
        return redirect('home')
    images = services.filterByCharacter(query) # Filtra y devuelve las cards que coincidan con el texto ingresado.
    favourite_list = []
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list }) # Se renderiza el template 'home.html' pasando el listado de imágenes.
    """
    Busca personajes por nombre.
    Se debe implementar la búsqueda de personajes según el nombre ingresado.
    Se debe obtener el parámetro 'query' desde el POST, filtrar las imágenes según el nombre
    y renderizar 'home.html' con los resultados. Si no se ingresa nada, redirigir a 'home'.
    """
    

def filter_by_status(request):
    """
    Filtra personajes por su estado (Alive/Deceased).
    Se debe implementar el filtrado de personajes según su estado.
    Se debe obtener el parámetro 'status' desde el POST, filtrar las imágenes según ese estado
    y renderizar 'home.html' con los resultados. Si no hay estado, redirigir a 'home'.
    """
    pass

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_cards = services.getAllFavourites(request) # Se obtiene la lista de favoritos del usuario autenticado.
    return render(request, 'favourites.html', {'favourite_list': favourite_cards}) # Se renderiza el template 'favourites.html' pasando la lista de favoritos en el contexto.

    """
    Obtiene todos los favoritos del usuario autenticado.
    """

@login_required
def saveFavourite(request):
    result = services.saveFavourite(request) # Se guarda el favorito y se obtiene el resultado de la operación.

    if result is None:
        messages.warning(request, 'Ups! No se pudo guardar el personaje a tus favoritos') # Si el resultado es None, se muestra un mensaje de advertencia al usuario.
    else:
        messages.success(request, 'Yeah! El personaje se agregó a tus favoritos!') # Si el resultado no es None, se muestra un mensaje de éxito al usuario.
    
    return redirect('home') # Se redirige al usuario a la página principal después de intentar guardar el favorito.

    """
    Guarda un personaje como favorito.
    """

@login_required
def deleteFavourite(request):
    #Extraer el ID que viene del <input type="hidden" name = "id"> del html
    favId = request.POST.get('id')
    deleted = services.deleteFavourite(request) # Se llama al servicio para eliminar el favorito basado en el ID obtenido del request.

    if deleted:
        messages.success(request, 'El personaje se eliminó de tus favoritos! ') 
    else:
        messages.warning(request, 'Ups! No se pudo eliminar el personaje de tus favoritos')
          
    return redirect('favoritos') # Se redirige al usuario a la página de favoritos después de eliminar el favorito.

    """
    Elimina un favorito del usuario.
    """

@login_required
def exit(request):
    logout(request)
    return redirect('home')

"""
    Hacer un nuevo usuario:
    Con esta funcion voy a pedirle al usuario nuevo sus datos para cadastro: nombre, apellido, email, usuario y contraseña.
    Luego, con esos datos, se crea un nuevo usuario en la base de datos y se le envía un email de bienvenida al correo que proporcionó.
    Con esto y from django.core.mail import send_mail que puse al iniciio puedo enviarle las credenciales al correo del usuario nuevo.
"""

def mostrar_formulario(request):
    return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('first_name')
        apellido = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Aquí se debería crear el nuevo usuario en la base de datos usando los datos obtenidos, antes de crear el usuario, se verifica si el nombre de usuario ya existe para evitar duplicados:
       
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'El nombre de usuario ya existe. Por favor, elige otro.')
            return redirect('register') #Si el nombre de usuario ya existe, se muestra un mensaje de advertencia y se redirige al formulario de registro para que el usuario intente con otro nombre.
        
        #Se crea el nuevo usuario en la base de datos con los datos obtenidos del formulario de registro:
        
        user = User.objects.create_user(username=username, password=password, email=email, first_name=nombre, last_name=apellido)
        user.save()
       
        #Se envía un correo de bienvenida al nuevo usuario con sus credenciales:
       
        subject = 'Bienvenido a la comunidad de fans de Los Simpsons'
        message = f'Hola {nombre}, gracias por registrarte en nuestra comunidad de fans de Los Simpsons.\n\nTu usuario es: {username}\n\nTu pass es: {password}\n\nBienvenido Vecinirijillo!'
        
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            messages.success(request, 'Usuario creado. Email enviado.')
        except Exception:
            messages.success(request, 'Usuario creado correctamente (no se pudo enviar el email).')
        
        return redirect('home') # Se redirige al usuario a la página principal después de registrarse.
    

    return render(request,'register.html') # Se renderiza el template 'register.html' pasando el formulario en el contexto.
