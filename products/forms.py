from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Product


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"multiple": True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    foto = forms.ImageField(
        required=False,
        label="Foto Sampul",
        help_text="Pilih 1 foto sebagai sampul/foto utama produk.",
    )
    foto_files = MultipleFileField(
        required=False,
        label="Foto Tambahan",
        help_text="Pilih 1-3 foto tambahan untuk produk (opsional).",
    )

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


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]