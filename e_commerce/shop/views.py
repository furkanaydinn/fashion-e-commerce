from django.shortcuts import get_object_or_404
from .models import Product,Category,Comment
from django.core.paginator import Paginator
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer,CategorySerializer,CommentSerializer

# Create your views here.

class Shop(APIView):
    def get(self, request):

        categories = Category.objects.all()
        products = Product.objects.all()

        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        category_slug = request.GET.get('category_slug')
        if category_slug:
            products = products.filter(category__slug=category_slug)

        category_count = Category.objects.annotate(items_count=Count('product_categories', distinct=True))

        paginator = Paginator(products, per_page=3)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serialized_products = ProductSerializer(page_obj.object_list, many=True).data
        serialized_categories = [category.toJSON() for category in categories]
        #serialized_categories = CategorySerializer(categories, many=True).data

        total_count = paginator.count
        page_start_index = (page_number - 1) * paginator.per_page + 1
        page_end_index = page_start_index + len(page_obj) - 1
        page_text = f"Showing {page_start_index}–{page_end_index} of {total_count} results"


        response_data = {
            'products': serialized_products,
            'paginator': {
                'page_number': int(page_number),
                'total_pages': paginator.num_pages,
                'page_text': page_text

            },
            'categories': serialized_categories,
            'category_count': category_count
        }

        return Response(response_data, status=status.HTTP_200_OK)
    


class ProductDetail(APIView):
    def get(self, request, id, category_slug, slug):
        product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE, pk=id)
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
        product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE, pk=id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    