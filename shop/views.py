from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product, Article
from shop.serializers import (
    CategoryListSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ArticleSerializer,
    CategoryDetailSerializer
)


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    # We add a class attribut to let us define our category detils serializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)

    def get_serializer_class(self):
        # If the action performed is 'retrieve' we return the detail's serializer
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer

    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        # We get all the products in a variable caled queryset
        queryset = Product.objects.filter(active=True)
        # Check the presence of the 'category_id' parameter in the url and if present we apply our filter
        category_id = self.request.GET.get('category_id')

        if category_id is not None:
            queryset = Product.objects.filter(category_id=category_id)
        return queryset

    def get_serializer_class(self):
        # If the action performed is 'retrieve' we return the detail's serializer
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


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
