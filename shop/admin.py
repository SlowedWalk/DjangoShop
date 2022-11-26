from django.contrib import admin

from shop.models import Category, Product, Article


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'active')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'price', 'active')

    @admin.display(description='Category')
    def categoty(self, obj):
        return obj.product.category


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Article, ArticleAdmin)
