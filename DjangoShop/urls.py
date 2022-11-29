from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from shop.serializers import AdminArticleSerializer
from shop.views import CategoryViewSet, ProductViewSet, ArticleViewSet, AdminCategoryViewSet, AdminArticleViewSet

# Here we create our router
router = routers.SimpleRouter()
# Then we define a url based on the keyword 'category'
# and our view in other for the genrated url should be one we expect
router.register('category', CategoryViewSet, basename='category')
router.register('product', ProductViewSet, basename='product')
router.register('article', ArticleViewSet, basename='article')
router.register('admin/category', AdminCategoryViewSet, basename='admin-category')
router.register('admin/article', AdminArticleViewSet, basename='admin-article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))  # Remember to add the router urls to the list of available urls.
]
