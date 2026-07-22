from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from products.views import register_view

admin.site.site_header = "DiDol Admin"
admin.site.site_title = "DiDol"
admin.site.index_title = "Kelola Produk DiDol"
urlpatterns = [
    path("", RedirectView.as_view(url="/products/", permanent=False)),
    path("admin/", admin.site.urls),
    path("accounts/register/", register_view, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("products/", include("products.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)