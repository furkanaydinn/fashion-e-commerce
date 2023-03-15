from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Blog,Comment
from .serializers import BlogSerializer,CommentSerializer

# Create your views here.

class BlogList(APIView):
    def get(self, request):
        blog = Blog.objects.filter(status=Blog.ACTIVE)
        serializer = BlogSerializer(blog, many=True)
        return Response(serializer.data)
    

class BlogDetail(APIView):
    def get_object(self, slug):
        try:
            return Blog.objects.get(slug=slug, status=Blog.ACTIVE)
        except Blog.DoesNotExist:
            raise Http404
        
    def get(self, request, slug):
        blog = self.get_object(slug)
        serializer = BlogSerializer(blog)
        prev_post = Blog.objects.filter(status=Blog.ACTIVE, created_at__lt=blog.created_at).order_by('-created_at').first()
        next_post = Blog.objects.filter(status=Blog.ACTIVE, created_at__gt=blog.created_at).order_by('created_at').first()
        if not next_post:
            next_post = Blog.objects.filter(status=Blog.ACTIVE, created_at__lt=blog.created_at).order_by('-created_at').last()
        return Response({
            'blog': serializer.data,
            'prev_post': {
                'title': prev_post.title,
                'slug': prev_post.slug
            } if prev_post else None,
            'next_post': {
                'title': next_post.title,
                'slug': next_post.slug
            } if next_post else None            
        })

    def post(self, request, slug):
        blog = self.get_object(slug)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    


    


    

    



