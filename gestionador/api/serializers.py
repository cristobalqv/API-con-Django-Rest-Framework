from rest_framework import serializers
from gestionador.models import Libro, Autor, Prestamo, User

class LibroSerializer(serializers.ModelSerializer):    #SERIALIZERS CONVIERTEN (TRADUCEN) OBJETOS EN MI BASE DE DATOS A ARCHIVOS JSON O XML
    class Meta:
        model = Libro
        fields = '__all__'


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'


class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = ['id', 'usuario', 'libro', 'fecha_prestamo', 'fecha_vencimiento', 'fecha_devolucion', 'estado']
        read_only_fields = ['usuario', 'fecha_prestamo', 'fecha_vencimiento', 'fecha_devolucion']

    def validate(self, data):
        # Validación solo para creación
        if self.instance is None:  # Solo se ejecuta al crear un nuevo préstamo
            usuario = self.context['request'].user   #usuario autenticado
            libro = data['libro']

            # Verificar si ya existe un préstamo activo del mismo libro para el usuario
            if Prestamo.objects.filter(usuario=usuario, libro=libro, estado='ACTIVO').exists():
                raise serializers.ValidationError({"error": "Ya tienes este libro prestado"})
            
        #para devoluciones
        if 'estado' in data and data['estado'] == 'DEVUELTO':
            if self.instance and self.instance.estado == 'DEVUELTO':
                raise serializers.ValidationError({"error": "Este préstamo ya fue devuelto"})
            
        return data
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})  # Esto hace que se muestre como campo de contraseña

    class Meta:
        model = User
        fields = ['username', 'password']  # Solo incluimos los campos que queremos
        extra_kwargs = {
            'username': {'help_text': 'Ingresa tu nombre de usuario'},
        }

    def create(self, validated_data):
        # Sobreescribo el método create para asegurar que la contraseña se guarde hasheada
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user