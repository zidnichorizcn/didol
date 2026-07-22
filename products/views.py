from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Product, SaleRecord
from .forms import ProductForm, CustomUserCreationForm, ProductImageFormSet

def product_list_view(request):
    products = Product.objects.all()

    kategori = request.GET.get("category")
    if kategori:
        products = products.filter(kategori=kategori)

    kondisi = request.GET.get("kondisi")
    if kondisi:
        products = products.filter(kondisi=kondisi)

    query = request.GET.get("q")
    if query:
        products = products.filter(nama__icontains=query)

    context = {
        "products": products,
        "kategori_aktif": kategori,
        "kondisi_aktif": kondisi,
        "query": query or "",
    }
    return render(request, "products/product_list.html", context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_url = request.build_absolute_uri()
    return render(request, "products/product_detail.html", {
        "product": product,
        "product_url": product_url,
    })


@login_required
def product_create_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.penjual = request.user
            product.save()
            formset.instance = product
            formset.save()
            return redirect("product_list")
    else:
        form = ProductForm()
        formset = ProductImageFormSet()

    return render(request, "products/product_form.html", {"form": form, "formset": formset})


@login_required
def dashboard_view(request):
    products = Product.objects.filter(penjual=request.user)

    jumlah_terjual = sum(p.jumlah_terjual for p in products)
    total_pendapatan = sum(p.pendapatan() for p in products)

    context = {
        "products": products,
        "jumlah_terjual": jumlah_terjual,
        "total_pendapatan": total_pendapatan,
    }
    return render(request, "products/dashboard.html", context)


@login_required
def riwayat_penjualan_view(request):
    riwayat = SaleRecord.objects.filter(penjual=request.user)
    total_pendapatan = sum(r.subtotal() for r in riwayat)
    return render(request, "products/riwayat_penjualan.html", {
        "riwayat": riwayat,
        "total_pendapatan": total_pendapatan,
    })


@login_required
def riwayat_delete_view(request, pk):
    record = get_object_or_404(SaleRecord, pk=pk, penjual=request.user)
    if request.method == "POST":
        product = record.product
        product.jumlah_terjual = max(0, product.jumlah_terjual - record.jumlah)
        if product.kondisi == "Ready":
            product.stok += record.jumlah
        product.save()
        record.delete()
    return redirect("riwayat_penjualan")


@login_required
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk, penjual=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("dashboard")
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(request, "products/product_form.html", {"form": form, "formset": formset})


@login_required
def product_delete_view(request, pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product, pk=pk)
    else:
        product = get_object_or_404(Product, pk=pk, penjual=request.user)

    if request.method == "POST":
        product.delete()
        return redirect("dashboard")

    return render(request, "products/product_confirm_delete.html", {"product": product})


@login_required
def product_catat_terjual_view(request, pk):
    product = get_object_or_404(Product, pk=pk, penjual=request.user)
    if request.method == "POST":
        try:
            jumlah = int(request.POST.get("jumlah", 0))
        except ValueError:
            jumlah = 0

        if jumlah > 0:
            if product.kondisi == "Ready" and jumlah > product.stok:
                jumlah = product.stok

            if jumlah > 0:
                product.jumlah_terjual += jumlah
                if product.kondisi == "Ready":
                    product.stok -= jumlah
                product.save()

                SaleRecord.objects.create(
                    product=product,
                    penjual=request.user,
                    jumlah=jumlah,
                    harga_saat_itu=product.harga,
                )
    return redirect("dashboard")


@login_required
def admin_all_products_view(request):
    if not request.user.is_superuser:
        return redirect("dashboard")
    products = Product.objects.all().order_by("-dibuat")
    return render(request, "products/admin_all_products.html", {"products": products})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})