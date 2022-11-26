from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product, Article
from shop.serializers import CategorySerializer, ProductSerializer, ArticleSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)


class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # We get all the products in a variable caled queryset
        queryset = Product.objects.filter(active=True)
        # Check the presence of the 'category_id' parameter in the url and if present we apply our filter
        category_id = self.request.GET.get('category_id')

        if category_id is not None:
            queryset = Product.objects.filter(category_id=category_id)
        return queryset


class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        # We get all the articles in a variable caled queryset
        queryset = Article.objects.filter(active=True)
        # Check the presence of the 'product_id' parameter in the url and if present we apply our filter
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = Article.objects.filter(product_id=product_id)

        return queryset
