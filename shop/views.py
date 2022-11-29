from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from shop.mixins import MultipleSerializerMixin
from shop.models import Category, Product, Article
from shop.serializers import (
    CategoryListSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ArticleSerializer,
    CategoryDetailSerializer
)


class CategoryViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    # We add a class attribut to let us define our category detils serializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)

    # def get_serializer_class(self):
    #     # If the action performed is 'retrieve' we return the detail's serializer
    #     if self.action == 'retrieve':
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().disable()
        return Response()


class AdminCategoryViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.all()


class ProductViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
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

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

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


class AdminArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

