"""
URL configuration for gudang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from inventaris.views import BarangListView, BarangCreateView, BarangUpdateView, BarangDeleteView, RiwayatListView, RiwayatCreateView
from rest_framework.routers import DefaultRouter
from inventaris.views import BarangViewSet, RiwayatTransaksiViewSet

# Membuat router otomatis
router = DefaultRouter()
router.register(r'barang', BarangViewSet)
router.register(r'riwayat', RiwayatTransaksiViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # --- URL UNTUK WEBSITE ---
    path('', BarangListView.as_view(), name='daftar_barang'),
    path('tambah/', BarangCreateView.as_view(), name='tambah_barang'),
    path('edit/<int:pk>/', BarangUpdateView.as_view(), name='edit_barang'),
    path('hapus/<int:pk>/', BarangDeleteView.as_view(), name='hapus_barang'),
    # URL RIWAYAT
    path('riwayat/', RiwayatListView.as_view(), name='daftar_riwayat'),
    path('riwayat/tambah/', RiwayatCreateView.as_view(), name='tambah_riwayat'),
]
