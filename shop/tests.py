from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product


class ShopAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        cls.product = cls.category.products.create(name='Ananas', active=True)
        cls.category.products.create(name='Banane', active=False)

        cls.category_2 = Category.objects.create(name='Légumes', active=True)
        cls.product_2 = cls.category_2.products.create(name='Tomate', active=True)

    # This method is a helper which enalbe the formating of date in a string under the same formt as that as the api
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_product_list_data(self, products):

        return [
            {
                'id': product.pk,
                'name': product.name,
                'articles': self.product.articles,
                'created_at': self.format_datetime(product.created_at),
                'updated_at': self.format_datetime(product.updated_at),
                'category': product.category_id
            } for product in products
        ]


class TestCategory(ShopAPITestCase):
    # We store the endpoint's url in a class variable in other to acces it more easily in each of out test
    url = reverse_lazy('category-list')

    # def test_list(self):
    #     # We perform the GET request by using the client of the test class
    #     response = self.client.get(self.url)
    #     # We verify the status code is 200 and that the data returned is what's expected
    #     self.assertEqual(response.status_code, 200)
    #     expected = [
    #         {
    #             'id': category.id,
    #             'name': category.name,
    #             'created_at': self.format_datetime(category.created_at),
    #             'updated_at': self.format_datetime(category.updated_at)
    #         } for category in [self.category, self.category_2]
    #     ]
    #     self.assertEqual(expected, response.json())

    def test_detail(self):
        # We use the category detail url
        url_detail = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url_detail)

        self.assertEqual(response.status_code, 200)
        excepted = {
            'id': self.category.pk,
            'name': self.category.name,
            'created_at': self.format_datetime(self.category.created_at),
            'updated_at': self.format_datetime(self.category.updated_at),
            'products': self.get_product_list_data(self.category.products.filter(active=True))
        }
        self.assertEqual(excepted, response.json())

    # def test_create(self):
    #     # We make sur that a category does not exist before creating it.
    #     category_count = Category.objects.count()
    #     response = self.client.post(self.url, data={'name': 'Nouvelle categorie'})
    #     # Verify that the status code is an error and prevents us from creating a category
    #     self.assertEqual(response.status_code, 405)
    #     # Finnaly, we verify that a category has not been created despite the error code 405
    #     self.assertEqual(Category.objects.exists(), category_count)


# class TestProduct(ShopAPITestCase):
#     url = reverse_lazy('product-list')
#
#     def get_product_data(self, products):
#         return [
#             {
#                 'id': product.pk,
#                 'name': product.name,
#                 'date_created': self.format_datetime(product.date_created),
#                 'date_updated': self.format_datetime(product.date_updated),
#                 'category': product.category_id
#             } for product in products
#         ]
#
#     def test_list(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(self.get_product_data([self.product, self.product_2]), response.json())
#
#     def test_list_filter(self):
#         response = self.client.get(self.url + '?category_id=%i' % self.category.pk)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(self.get_product_data(self.product), response.json())
#
#     def test_create(self):
#         product_count = Product.objects.count()
#         response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
#         self.assertEqual(response.status_code, 405)
#         self.assertEqual(Product.objects.count(), product_count)
#
#     def test_delete(self):
#         response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}))
#         self.assertEqual(response.status_code, 405)
#         self.product.refresh_from_db()
