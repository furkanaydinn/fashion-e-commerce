from rest_framework import serializers
from .models import Category, Product, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
                  'id', 
                  'category', 
                  'image', 
                  'title', 
                  'tags', 
                  'sku', 
                  'brand', 
                  'intro', 
                  'description', 
                  'price', 
                  'amount', 
                  'slug', 
                  'status', 
                  'created_at', 
                  'updated_at', 
                  'avaregereview', 
                  'countreview'
                  ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
