from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "nama", "kategori", "brand", "harga", "sembunyikan_harga",
            "kondisi", "stok", "lokasi", "no_wa", "spesifikasi", "foto",
        ]
        labels = {
            "no_wa": "Nomor WhatsApp",
            "sembunyikan_harga": "Sensor harga di halaman publik",
            "spesifikasi": "Spesifikasi Produk",
            "foto": "Foto Utama",
            "stok": "Jumlah Stok",
        }
        widgets = {
            "no_wa": forms.TextInput(attrs={"placeholder": "Contoh: 6281234567890"}),
            "spesifikasi": forms.Textarea(attrs={"rows": 5, "placeholder": "Contoh: Ukuran 30x20 cm, bahan kayu jati solid, berat 1.5 kg"}),
        }
        help_texts = {
            "no_wa": "Gunakan kode negara 62 di depan, tanpa tanda + atau angka 0. Contoh: nomor 0812-3456-7890 ditulis 6281234567890",
            "sembunyikan_harga": "Kalau dicentang, harga akan tampil tersamar, misal Rp 10000 jadi Rp 1xxxx",
            "stok": "Isi jumlah stok kalau kondisi Ready Stock. Untuk Pre Order boleh dikosongkan/isi 0.",
        }


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    fields=["foto"],
    extra=2,
    max_num=2,
    can_delete=True,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]