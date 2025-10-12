# скрипт для создания тестовых данных

from django.core.management.base import BaseCommand
from products.models import Brand, Category, Season, Size, Product
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Create sample data for the store'

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Создаем бренды
        brands_data = [
            {"name": "Rick Owens", "description": "American avant-garde fashion designer known for dark, draped aesthetic"},
            {"name": "Enfants Riches Déprimés", "description": "Los Angeles-based luxury brand with punk and grunge influences"},
            {"name": "Comme des Garçons", "description": "Japanese fashion label founded by Rei Kawakubo"},
            {"name": "Raf Simons", "description": "Belgian fashion designer known for minimalist menswear"},
            {"name": "Maison Margiela", "description": "French luxury fashion house known for deconstructive approach"},
            {"name": "Yohji Yamamoto", "description": "Japanese fashion designer pioneering avant-garde fashion"},
            {"name": "Undercover", "description": "Japanese streetwear brand by Jun Takahashi"},
        ]

        brands = []
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_data["name"],
                defaults={"description": brand_data["description"], "slug": slugify(brand_data["name"])}
            )
            brands.append(brand)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created brand: {brand.slug}'))

        # Создаем категории
        categories_data = [
            {"name": "Outerwear", "description": "Jackets, coats, and more"},
            {"name": "Tops", "description": "T-shirts, shirts, sweaters"},
            {"name": "Bottoms", "description": "Pants, shorts, jeans"},
            {"name": "Footwear", "description": "Sneakers, boots, shoes"},
            {"name": "Accessories", "description": "Bags, hats, belts"},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={"description": cat_data["description"], "slug": slugify(cat_data["name"])}
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Создаем сезоны
        seasons_data = [
            {"name": "Spring/Summer 2020", "year": 2020},
            {"name": "Fall/Winter 2019", "year": 2019},
            {"name": "Spring/Summer 2018", "year": 2018},
        ]

        seasons = []
        for season_data in seasons_data:
            season, created = Season.objects.get_or_create(
                name=season_data["name"],
                defaults={"year": season_data["year"]}
            )
            seasons.append(season)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created season: {season.name}'))

        # Создаем размеры
        sizes_data = [
            {"category": "clothing", "value": "XS"},
            {"category": "clothing", "value": "S"},
            {"category": "clothing", "value": "M"},
            {"category": "clothing", "value": "L"},
            {"category": "clothing", "value": "XL"},
            {"category": "clothing", "value": "XXL"},
            {"category": "shoes", "value": "40"},
            {"category": "shoes", "value": "41"},
            {"category": "shoes", "value": "42"},
            {"category": "shoes", "value": "43"},
            {"category": "shoes", "value": "44"},
        ]
        sizes = []
        for size_data in sizes_data:
            size, created = Size.objects.get_or_create(
                category=size_data["category"],
                value=size_data["value"]
            )
            sizes.append(size)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created size: {size.category}-{size.value}'))

        # Создаем товары
        products_data = [
            {
                "name": "Rick Owens DRKSHDW Ramones Sneakers",
                "description": "Iconic high-top sneakers from DRKSHDW line. Canvas construction with signature elongated tongue and exaggerated silhouette.",
                "price": 520.00,
                "brand": brands[0],
                "category": categories[3],
                "condition": "excellent",
                "stock_quantity": 1,
                "is_featured": True,
            },
            {
                "name": "Enfants Riches Déprimés Stop Being Poor Tee",
                "description": "Signature slogan tee in distressed black. Hand-screened graphics with vintage wash. Made in USA.",
                "price": 385.00,
                "brand": brands[1],
                "category": categories[1],
                "condition": "new",
                "stock_quantity": 2,
                "is_featured": True,
            },
            {
                "name": "Comme des Garçons Homme Plus Deconstructed Blazer",
                "description": "Avant-garde wool blazer with asymmetric cut and raw edges. From Rei Kawakubo's experimental collection.",
                "price": 890.00,
                "brand": brands[2],
                "category": categories[0],
                "condition": "excellent",
                "stock_quantity": 1,
                "is_featured": True,
            },
            {
                "name": "Raf Simons Archive Redux Parka",
                "description": "Rare archive piece from FW05 'Waves' collection. Oversized fit with storm flap and multiple pockets.",
                "price": 1450.00,
                "brand": brands[3],
                "category": categories[0],
                "condition": "excellent",
                "stock_quantity": 1,
                "is_featured": True,
            },
            {
                "name": "Maison Margiela Replica GAT Sneakers",
                "description": "German Army Trainer replica in premium leather. Signature paint splatter detail and numbered label.",
                "price": 425.00,
                "brand": brands[4],
                "category": categories[3],
                "condition": "new",
                "stock_quantity": 3,
                "is_featured": False,
            },
            {
                "name": "Yohji Yamamoto Pour Homme Wide Trousers",
                "description": "Signature wide-leg wool trousers with dropped crotch. Japanese craftsmanship and minimalist silhouette.",
                "price": 650.00,
                "brand": brands[5],
                "category": categories[2],
                "condition": "excellent",
                "stock_quantity": 2,
                "is_featured": False,
            },
            {
                "name": "Undercover Scab Denim Jacket",
                "description": "Iconic embroidered denim jacket from 'Scab' collection. Features detailed back graphics and distressed finish.",
                "price": 780.00,
                "brand": brands[6],
                "category": categories[0],
                "condition": "good",
                "stock_quantity": 1,
                "is_featured": True,
            },
        ]

        for product_data in products_data:
            product_data_clean = {k: v for k, v in product_data.items() if k != 'stock_quantity'}
            
            if product_data['category'].slug in ['outerwear', 'tops', 'bottoms']:
                product_data_clean['size'] = [s for s in sizes if s.category == 'clothing'][2]  # M
            elif product_data['category'].slug == 'footwear':
                product_data_clean['size'] = [s for s in sizes if s.category == 'shoes'][2]  # 42
            
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    **product_data_clean,
                    "slug": slugify(product_data["name"]),
                    "is_available": True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.slug}'))

        self.stdout.write(self.style.SUCCESS('\nSample data created successfully!'))
        self.stdout.write(f'Brands: {Brand.objects.count()}')
        self.stdout.write(f'Categories: {Category.objects.count()}')
        self.stdout.write(f'Seasons: {Season.objects.count()}')
        self.stdout.write(f'Sizes: {Size.objects.count()}')
        self.stdout.write(f'Products: {Product.objects.count()}')

