from rest_framework import serializers

from shop.models import Category, Product, Article


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'created_at', 'updated_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    # When using a `SerializerMethodField`, it is necessary to write a method
    # named 'get_XXX' where XXX is the name of the attribute, here 'artilces'
    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'articles', 'created_at', 'updated_at']

    def get_articles(self, instance):
        # The 'instance' parameter is the instance of the product being consulted.
        # In the case of a list, this method is called as many times as there are
        # of entities in the list

        # We apply the filter on our queryset to have only the active articles
        queryset = instance.articles.filter(active=True)
        # The serializer is created with the queryset defined and always set as many=True
        serializer = ArticleSerializer(queryset, many=True)
        # the '.data' property is the render of our serializer that we return here
        return serializer.data


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'name', 'price', 'product_id', 'active', 'created_at', 'updated_at']

    def validate(self, data):
        # Effectuons le contrôle sur le prix de l'article
        if data['price'] < 1:
        # Levons une ValidationError si ça n'est pas le cas
            raise serializers.ValidationError('Price must be > $1')
        return data


class AdminArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'name', 'price', 'product_id', 'active', 'created_at', 'updated_at']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at']

    def validate_name(self, value):
        # Nous vérifions que la catégorie existe
        if Category.objects.filter(name=value).exists():
            # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('Category already exists')
        return value

    def validate(self, data):
        # Effectuons le contrôle sur la présence du nom dans la description
        if data['name'] not in data['description']:
            # Levons une ValidationError si ça n'est pas le cas
            raise serializers.ValidationError('Name must be in description')
        return data


class CategoryDetailSerializer(serializers.ModelSerializer):
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
        serializer = ProductDetailSerializer(queryset, many=True)
        # the '.data' property is the render of our serializer that we return here
        return serializer.data

