from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class PostListAPI(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer

class PostDetailAPI(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'