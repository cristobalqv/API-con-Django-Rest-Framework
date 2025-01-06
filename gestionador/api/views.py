from rest_framework import viewsets, serializers
from gestionador.api.serializers import LibroSerializer, AutorSerializer, PrestamoSerializer, UserSerializer, RegisterSerializer
from gestionador.models import Libro, Autor, Prestamo, User
from django.db import transaction
from datetime import datetime, timedelta
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.http import JsonResponse



class IsAdminOrReadOnly(BasePermission):
    # Permiso que permite acceso de solo lectura para todos, pero escritura solo para administradores.
  
    def has_permission(self, request, view):
        # Permitir GET, HEAD, OPTIONS para todos
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Permitir POST, PUT, DELETE solo para administradores
        return request.user and (request.user.is_staff or request.user.is_superuser)



class LibroViewSet(viewsets.ModelViewSet):     #ESTOS CLASES HEREDARAN DE MODELVIEWSET METODOS FUNDAMENTALES DE CRUD
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminOrReadOnly]  # Solo administradores pueden modificar



class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAdminOrReadOnly]  # Solo administradores pueden modificar



class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):       #REESCRIBO EL METODO PERFORM_CREATE QUE ES LLAMADO LUEGO DE LA VALIDACION CON CREATE PERO ANTES DE GUARDAR EL OBJETO. DE ESTA FORMA VOY A INTERCEPTAR EL METODO CREATE USADO PARA AÑADIR UN REGISTRO CON "POST"
        libro = serializer.validated_data['libro']  #obtengo el libro del request una vez es validada la data
        print(f"Objeto libro obtenido: {libro} (tipo: {type(libro)})")   #ASEGURO QUE libro ES UNA INSTANCIA DE Libro(la clase)
        usuario_actual = self.request.user   #'''OJO con este user'''

        if libro.copias_disponibles <= 0:
            raise serializers.ValidationError({"error": "No hay copias disponibles de este libro"})

        prestamo_existente = Prestamo.objects.filter(usuario=usuario_actual, libro=libro, estado='ACTIVO').exists()  

        if prestamo_existente:
            raise serializers.ValidationError({"error": "Ya tienes este libro prestado"})

        # Uso transaction.atomic para asegurar que todas las operaciones se realicen o ninguna de ellas (para mantener la integridad de los datos)
        try:
            with transaction.atomic():
                libro.copias_disponibles -= 1
                libro.save()
                libro.refresh_from_db()  # Refresca el estado desde la base de datos
                #calculo fecha de devolucion con timedelta
                fecha_vencimiento = now() + timedelta(days=14)
                #guardo el prestamo con el usuario actual
                serializer.save(usuario=usuario_actual, fecha_vencimiento=fecha_vencimiento, estado='ACTIVO')

        except Exception as e:
            print(f"Error al crear el préstamo: {e}")
            raise serializers.ValidationError({"error": "No se pudo procesar el préstamo."})

    #este metodo es usado justo antes de guardar un serializador modificado. metodo perform_update es usado por el metodo update, que a su vez es gatillado por una solicitud PUT
    def perform_update(self, serializer):
        prestamo = serializer.instance   #accedo a la instancia que esta siendo actualizada al hacer la solicitud http respectiva. 
        nuevo_estado = serializer.validated_data.get('estado')

        if nuevo_estado == 'DEVUELTO' and prestamo.estado != 'DEVUELTO':
            with transaction.atomic():
                libro = prestamo.libro
                # Aumento las copias disponibles
                libro.copias_disponibles += 1
                libro.save()

                # Guardo la fecha de devolución
                serializer.save(return_date=datetime.now())

        else:
            serializer.save()

    #modifico get_queryset para personalizar los prestamos que puede ver cada usuario
    def get_queryset(self):
        if self.request.user.is_staff:
            return Prestamo.objects.all()   #staff puede ver todos los prestamos 
        
        return Prestamo.objects.filter(usuario=self.request.user)
        


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]  # Solo administradores pueden modificar



class RegisterView(APIView):         #CLASE PARA PODER REGISTRAR USUARIOS FUERA DEL PANEL DE ADMINISTRACION
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer  # Especificamos el serializador a usar

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Guardamos el nuevo usuario
            user = serializer.save()

            # Generamos el token
            token, created = Token.objects.get_or_create(user=user)
        
            # Devolvemos la respuesta con el token
            return Response({'message': 'Usuario creado exitosamente', 'token': token.key}, status=status.HTTP_201_CREATED)
        
        # Si hay errores de validación, los devolvemos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # Agregamos el método GET para mostrar el formulario en el navegador
        return Response({
            'username': 'Ingresa tu nombre de usuario',
            'password': 'Ingresa tu contraseña'
        })
    
