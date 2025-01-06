from django.contrib import admin
from gestionador.models import Libro, Autor, Prestamo

# Register your models here.

admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Prestamo)


