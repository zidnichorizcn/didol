from django.urls import path
from .views import (
    product_list_view,
    product_detail_view,
    product_create_view,
    dashboard_view,
    riwayat_penjualan_view,
    riwayat_delete_view,
    product_update_view,
    product_delete_view,
    product_catat_terjual_view,
    admin_all_products_view,
)

urlpatterns = [
    path("", product_list_view, name="product_list"),
    path("tambah/", product_create_view, name="product_create"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("riwayat/", riwayat_penjualan_view, name="riwayat_penjualan"),
    path("riwayat/<int:pk>/hapus/", riwayat_delete_view, name="riwayat_delete"),
    path("semua-produk/", admin_all_products_view, name="admin_all_products"),
    path("<int:pk>/", product_detail_view, name="product_detail"),
    path("<int:pk>/edit/", product_update_view, name="product_update"),
    path("<int:pk>/hapus/", product_delete_view, name="product_delete"),
    path("<int:pk>/catat-terjual/", product_catat_terjual_view, name="product_catat_terjual"),
]