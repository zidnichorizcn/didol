from django.core.management.base import BaseCommand
from products.models import Product, ProductImage, optimize_image


class Command(BaseCommand):
    help = "Optimasi ulang semua foto produk yang sudah ada"

    def handle(self, *args, **options):
        count = 0
        for product in Product.objects.exclude(foto=""):
            if product.foto:
                optimize_image(product.foto)
                count += 1
                self.stdout.write(f"Optimized: {product.foto.name}")

        for img in ProductImage.objects.all():
            if img.foto:
                optimize_image(img.foto)
                count += 1
                self.stdout.write(f"Optimized: {img.foto.name}")

        self.stdout.write(self.style.SUCCESS(f"Selesai! {count} foto berhasil dioptimasi."))