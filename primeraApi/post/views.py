from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster = self.request.user)

class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter = user, post = post)
    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('Ya haz votado por este post')
        serializer.save(voter=self.request.user, post = Post.objects.get(pk = self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Tu nunca haz votado por este post')

class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk = self.kwargs['pk'], poster = self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Tu no puedes eliminar este post')