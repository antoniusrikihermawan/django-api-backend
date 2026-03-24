from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import KategoriViewSet, SupplierViewSet, BarangViewSet, TransaksiPenjualanViewSet, TransaksiViewSet

router = DefaultRouter()
router.register(r'kategori', KategoriViewSet)
router.register(r'supplier', SupplierViewSet)
router.register(r'barang', BarangViewSet)
router.register(r'transaksi', TransaksiPenjualanViewSet)
router.register(r'pembelian', TransaksiViewSet)

urlpatterns = [
    # 1. API Router (CRUD)
    path('', include(router.urls)),
    
    # 2. Autentikasi (Login)
    path('auth/login/', obtain_auth_token, name='api_token_auth'),
    
    # 3. Dokumentasi API (Swagger)
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]