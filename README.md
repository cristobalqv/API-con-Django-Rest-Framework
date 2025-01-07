# API con DRF: Biblioteca con sistema de préstamo de libros

[![1](https://github.com/cristobalqv/Biblioteca-Sistema-de-prestamo-de-libros/blob/main/varios/imagen1.png "1")](https://github.com/cristobalqv/Biblioteca-Sistema-de-prestamo-de-libros/blob/main/varios/imagen1.png "1")

El siguiente proyecto consistió en la creación de una API para una Biblioteca ficticia con el objetivo de gestionar los préstamos e inventario de la misma. Está habilitada para que una persona pueda crear un usuario y contraseña y así poder interactuar y generar un préstamo de un libro dependiendo de la disponibilidad del mismo, lo que está almacenado en una base de datos  Postgresql. Un aspecto a destacar es la interacción entre la base de datos y las solicitudes de préstamos, descontando unidades disponibles y actualizándolas una vez devuelto el libro.
Se profundizaron conceptos de Programación Orientada a Objetos, modelos de bases de datos, serializadores y autenticación en Django-Rest-Framework, entre otros.

**Consideración: ** El enfoque de esta aplicación es de Backend, por lo que las interfaces visuales, dinámicas y de diseño son limitadas y quedan relegadas. Aclarar también que este proyecto corresponde a un **MVP**, por lo que puede estar en constante cambio (cambios que se estarán anunciando)
<br>
<br>

## ️⚙️ Características

Este proyecto permite:

- 🏫Creación de una API de gestión de biblioteca
- 👮‍♂️ Creación de un super-usuario del blog (puede otorgar permisos 🔑)
- 👤 Creación de usuarios por parte de administrador o persona natural
- 📙Agregar libros, usuarios👤 y autores✒️
- 🔄Generar un sistema de préstamo de libros📚

<br>
<br>

## 🗒️ Estructura del proyecto y funcionamiento del código `</>`



```
PROYECTO/
│
├── biblioteca/                           
│         ├── __init__.py                   # Directorio como un paquete de Python
│         ├── asgi.py             
│         ├── settings.py                 # Configuraciones globales del proyecto
│         ├── urls.py                        # Configuración de las rutas del proyecto
│         └── wsgi.py                
│
├── gestionador/                         # Aplicación principal
│         ├── api/          
│         │       ├── serializers.py    # Serializadores
│         │       └── views.py           # Lógica del procesamiento de solicitudes HTTP
│         │ 
│         ├── __init__.py            
│         ├── admin.py                   # Registro de modelos en el admin
│         ├── apps.py                      
│         └── models.py                 # Modelos de base de datos
│
├── venv/                                    # Entorno virtual de Python
├── LICENSE                     
└── manage.py                           # Comando de gestión de Django

```
Los archivos y directorios del proyecto más relevantes para la lógica, funcionamiento e interacción con la API son:

`biblioteca/settings.py` Este [script](https://github.com/cristobalqv/Biblioteca-Sistema-de-prestamo-de-libros/blob/main/biblioteca/settings.py "script") corresponde al archivo de configuración global de la aplicación. Contiene entre otras funcionalidades las instrucciones para la configuración de la base de datos, indicaciones para autenticaciones, además de información sensible como contraseñas.

`biblioteca/urls.py` Este [script](https://github.com/cristobalqv/Biblioteca-Sistema-de-prestamo-de-libros/blob/main/biblioteca/urls.py "script") contiene las configuraciones de url para la aplicación, las que permiten mapear las urls a las vistas posibilitando manejar varios diferentes métodos HTTP.

`gestionador/api/serializers.py` Este [script](https://github.com/cristobalqv/Biblioteca-Sistema-de-prestamo-de-libros/blob/main/gestionador/api/serializers.py "script") contiene los serializadores que convierten (o traducen) los datos de modelos de django (objetos complejos) en formatos mas sencillos que se pueden enviar mediante la API (principalmente JSON o XML). Además validan los datos enviados a tavés de la API antes de guardarlos en la base de datos.

`gestionador/api/views.py` Este [script](https://github.com/cristobalqv/Biblioteca-Sistema-de-prestamo-de-libros/blob/main/gestionador/api/views.py "script") contiene los Views y Viewsets que manejan la lógica de procesamiento de las peticiones HTTP (GET, PUT, POST, DELETE). Los Viewsets son clases que simplifican la creación de endpoints REST.

`gestionador/models.py` [Script](https://github.com/cristobalqv/Biblioteca-Sistema-de-prestamo-de-libros/blob/main/gestionador/models.py " Script") donde se registran los modelos de la base de datos y sus respectivas relaciones.

<br>
<br>

## 💻 Instalación y uso

Clona el repositorio:

```
git clone https://github.com/cristobalqv/Biblioteca-Sistema-de-prestamo-de-libros
```

Para ejecutar el proyecto, en primera instancia deberás crear un superusuario para poder habilitar un usuario en el administrador de Django. Debes situarte en el mismo directorio de `manage.py` :

```python manage.py createsuperuser```

Luego deberás ejecutar el siguiente comando:

```python manage.py runserver```

Posteriormente, abre un navegador y dependiendo si quieres acceder al panel de administración de Django o al blog, escribe en la barra de búsqueda:
- http://127.0.0.1:8000/admin
- http://127.0.0.1:8000/api
- http://127.0.0.1:8000/register/     (debes situarte en la pestaña HTML form)

**Consideración**: Para la solicitud de devolución de libros, usar Postman con los siguientes parámetros:
- Solicitud PUT con el endpoint "http://127.0.0.1:8000/api/prestamos/{id_prestamo}/"   (el id_prestamo se encuentra en la tabla gestionador_prestamo)
- Autorización de tipo "API Key" con Key = "Authorization" y Value = "Token {numero_token}"   (token generado al crear un usuario)
- En headers, Key = "Content-type" y Value = "application/json"
- Por último, en la pestaña "Body" colocar Raw y Json. con el siguiente diccionario: {"estado": "DEVUELTO", "libro": id_del_libro}

<br>
<br>

## 🤝 Contribuciones



¡Las contribuciones son bienvenidas! Por favor, sigue los siguientes pasos:

- ** Haz un fork del proyecto y crea una nueva rama:**

`git checkout -b feature/nueva-funcionalidad`

- ** Realiza tus cambios y haz commit:**

`git commit -am 'Agrega nueva funcionalidad'`

- ** Sube los cambios:**

`git push origin feature/nueva-funcionalidad`

- ** Envía un Pull Request.**

<br>
<br>

## 📜 Licencia



Este proyecto está licenciado bajo la Licencia MIT, lo que permite su libre uso y modificación con fines personales o comerciales.