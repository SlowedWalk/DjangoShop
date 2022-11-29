from django.db import models, transaction


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    @transaction.atomic
    def disable(self):
        # We define our action to be accessible only via POST method
        # it includes the details as it can disable a category

        # We equally put in placed an actomic transaction as many request will be executed
        # In cas of any error, we revert to the previos state

        # Deactivate the category
        if self.active is False:
            # We do nothing if the category is already deactivated
            return

        self.active = False
        self.save()

        # Deactivate the category's prodcuts
        self.products.update(active=False)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='articles')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.name
