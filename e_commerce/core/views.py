from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from blog.serializers import BlogSerializer
from blog.models import Blog
from django.views.generic import TemplateView

# Create your views here.



class IndexView(APIView):
    
    
    def get(self, request):
        blogs = Blog.objects.filter(status=Blog.ACTIVE).order_by('-created_at')[:3]
        serializer = BlogSerializer(blogs, many=True)
        data = []

        for blog in serializer.data:
            post_image = None  # varsayılan olarak post_image değeri yok kabul edilir
            if blog['post_image']:
                post_image = blog['post_image']
                if isinstance(post_image, str):
                    post_image = None  # post_image bir URL değilse None olarak ayarlanır

            blog_data = {
                'title': blog['title'],
                'created_at': blog['created_at'],
                'post_image': post_image.url if post_image else None,
                'url': request.build_absolute_uri(blog['slug'])
            }
            data.append(blog_data)

        return Response(data)


class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your message has been sent. Thank you for your message.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



