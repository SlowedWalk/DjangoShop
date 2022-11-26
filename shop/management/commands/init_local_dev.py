from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from shop.models import Category

UserModel = get_user_model()

CATEGORIES = [
    {
        'name': 'Fruit',
        'active': True,
        'products': [
            {
                'name': 'Banane',
                'active': True,
                'articles': [
                    {
                        'name': 'Unité',
                        'price': 2.50,
                        'active': True
                    },
                    {
                        'name': 'Lot de 2',
                        'price': 4.50,
                        'active': True
                    },
                ]
            },
            {
                'name': 'Kiwi',
                'active': True,
                'articles': [
                    {
                        'name': 'Unité',
                        'price': 0.75,
                        'active': True
                    },
                    {
                        'name': 'Lot de 5',
                        'price': 3.00,
                        'active': True
                    },
                ]
            },
            {
                'name': 'Ananas',
                'active': False,
                'articles': [
                    {
                        'name': 'Unité',
                        'price': 2.50,
                        'active': False
                    }
                ]
            },
        ]
    },
    {
        'name': 'Légumes',
        'active': True,
        'products': [
            {
                'name': 'Courgette',
                'active': True,
                'articles': [
                    {
                        'name': 'Unité',
                        'price': 1.00,
                        'active': True
                    },
                    {
                        'name': 'Lot de 3',
                        'price': 2.50,
                        'active': False
                    },
                ]
            }
        ]
    },
    {
        'name': 'Épicerie',
        'active': True,
        'products': [
            {
                'name': 'Sel',
                'active': True,
                'articles': [
                    {
                        'name': '100g',
                        'price': 1.00,
                        'active': False
                    },
                    {
                        'name': '300g',
                        'price': 2.50,
                        'active': False
                    },
                ]
            }
        ]
    }
]

ADMIN_ID = 'admin-hb'
ADMIN_PASSWORD = 'password-hb'


class Command(BaseCommand):
    help = 'Initialize projet for local developement'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        Category.objects.all().delete()

        for category_data in CATEGORIES:
            category = Category.objects.create(
                name=category_data['name'],
                active=category_data['active']
            )

            for product_data in category_data['products']:
                product = category.products.create(
                    name=product_data['name'],
                    active=product_data['active']
                )

                for article_data in product_data['articles']:
                    product.articles.create(
                        name=article_data['name'],
                        active=article_data['active'],
                        price=article_data['price']
                    )

        UserModel.objects.create_superuser(ADMIN_ID, 'admin@admin.com', ADMIN_PASSWORD)
        self.stdout.write(self.style.SUCCESS("ALL DONE !"))
