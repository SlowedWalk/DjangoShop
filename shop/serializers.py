from rest_framework import serializers

from shop.models import Category, Product, Article


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'created_at', 'updated_at']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'name', 'price', 'product_id', 'active', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    # When using a `SerializerMethodField`, it is necessary to write a method
    # named 'get_XXX' where XXX is the name of the attribute, here 'products'
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products', 'created_at', 'updated_at']

    def get_products(self, instance):
        # The 'instance' parameter is the instance of the category being consulted.
        # In the case of a list, this method is called as many times as there are
        # of entities in the list

        # We apply the filter on our queryset to have only the active products
        queryset = instance.products.filter(active=True)
        # The serializer is created with the queryset defined and always set as many=True
        serializer = ProductSerializer(queryset, many=True)
        # the '.data' property is the render of our serializer that we return here
        return serializer.data
