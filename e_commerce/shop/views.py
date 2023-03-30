from django.shortcuts import get_object_or_404
from .models import Product,Category,Comment
from django.core.paginator import Paginator
from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from .serializers import ProductSerializer,CategorySerializer,CommentSerializer

# Create your views here.

class Shop(APIView):
    def get(self, request):
        try:
            # Retrieve query parameters
            category = request.GET.get('category')
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            sort_by = request.GET.get('sort_by', 'default')
            page = request.GET.get('page', 1)

            # Filter products based on query parameters
            products = Product.objects.filter(status='ACTIVE')
            if category:
                products = products.filter(category__slug=category)
            if min_price:
                products = products.filter(price__gte=min_price)
            if max_price:
                products = products.filter(price__lte=max_price)

            if sort_by == 'price_asc':
                products = products.order_by('price')
            elif sort_by == 'price_desc':
                products = products.order_by('-price')

            # Paginate products
            paginator = Paginator(products, 3)
            page_obj = paginator.get_page(page)
            page_start_index = (page_obj.number - 1) * paginator.per_page + 1
            page_end_index = min(page_obj.number * paginator.per_page, paginator.count)

            # Serialize products
            products_data = []
            for product in page_obj:
                product_data = {
                    'id': product.id,
                    'title': product.title,
                    'image': product.image.url,
                    'avg_rating': product.avaregereview(),
                    'price': product.price,
                }
                products_data.append(product_data)

            # Return JSON response
            response_data = {
                'products': products_data,
                'categories': [],
                'page_text': f"Showing {page_start_index}–{page_end_index} of {paginator.count} results",
            }
            categories = Category.objects.all()
            for cat in categories:
                cat_data = {
                    'title': cat.title,
                    'slug': cat.slug,
                    'count': Product.objects.filter(category=cat, status='ACTIVE').count()
                }
                response_data['categories'].append(cat_data)

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get(self, request, id, category_slug, slug):
        product = get_object_or_404(Product, slug=slug, status='ACTIVE', pk=id)
        serializer = ProductSerializer(product)
        comments = Comment.objects.filter(product=product, status='True')
        comment_serializer = CommentSerializer(comments, many=True)
        return Response({
            'product': serializer.data,
            'comments': comment_serializer.data,
            'total_reviews': comments.count(),
            'avg_rating': product.avaregereview(),
        })
    
    def post(self, request, id, category_slug, slug):
        product = get_object_or_404(Product, slug=slug, status='ACTIVE', pk=id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    