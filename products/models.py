from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
import os

def optimize_image(image_field, max_width=1200, quality=80):
    if not image_field:
        return
    path = image_field.path
    try:
        img = Image.open(path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)
        img.save(path, quality=quality, optimize=True)
    except Exception:
        pass


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Kerajinan Kayu", "Kerajinan Kayu"),
        ("Mebel", "Mebel"),
        ("Alat Serbaguna", "Alat Serbaguna"),
        ("Kerajinan Umum", "Kerajinan Umum"),
        ("Lainnya", "Lainnya"),
    ]
    KONDISI_CHOICES = [
        ("Ready", "Ready Stock"),
        ("PreOrder", "Pre Order"),
    ]
    STATUS_CHOICES = [
        ("Aktif", "Aktif / Dijual"),
        ("Terjual", "Terjual"),
    ]

    penjual = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100, blank=True)
    harga = models.PositiveIntegerField()
    sembunyikan_harga = models.BooleanField(default=False, help_text="Centang untuk menyensor harga di halaman publik, misal Rp 10000 tampil jadi Rp 1xxxx")
    kondisi = models.CharField(max_length=20, choices=KONDISI_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Aktif")
    stok = models.PositiveIntegerField(default=0, help_text="Jumlah stok tersedia (khusus untuk kondisi Ready Stock)")
    jumlah_terjual = models.PositiveIntegerField(default=0)
    lokasi = models.CharField(max_length=100)
    no_wa = models.CharField(max_length=20, help_text="Contoh: 6281234567890 (kode negara, tanpa + atau 0 di depan)")
    spesifikasi = models.TextField(blank=True, help_text="Detail ukuran, bahan, berat, cara pakai, dll.")
    foto = models.ImageField(upload_to="produk/", blank=True, null=True, help_text="Foto utama/sampul produk")
    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.foto:
            optimize_image(self.foto)

    def harga_tampil(self):
        if self.sembunyikan_harga:
            harga_str = str(self.harga)
            if len(harga_str) > 1:
                tersamar = harga_str[0] + "x" * (len(harga_str) - 1)
            else:
                tersamar = harga_str
            return tersamar
        return f"{self.harga:,}".replace(",", ".")

    def pendapatan(self):
        return self.harga * self.jumlah_terjual


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    foto = models.ImageField(upload_to="produk/tambahan/")

    def __str__(self):
        return f"Foto tambahan - {self.product.nama}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.foto:
            optimize_image(self.foto)


class SaleRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="riwayat")
    penjual = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    harga_saat_itu = models.PositiveIntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.jumlah * self.harga_saat_itu

    def __str__(self):
        return f"{self.jumlah}x {self.product.nama} - {self.tanggal.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ["-tanggal"]