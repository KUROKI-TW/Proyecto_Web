from rest_framework import serializers
from .models import Post, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class PostSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField()          # username
    categoria = CategoriaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'titulo', 'contenido', 'imagen', 'autor',
                    'categoria', 'created', 'updated']