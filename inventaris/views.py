from rest_framework import viewsets, permissions
from .models import Kategori, Supplier, Barang, TransaksiPenjualan, Transaksi
from .serializers import (
    KategoriSerializer, 
    SupplierSerializer, 
    BarangSerializer, 
    TransaksiPenjualanSerializer,
    TransaksiSerializer
)
from .permissions import IsStaffOrReadOnly

# 1. ViewSet Kategori
class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all().order_by('id')
    serializer_class = KategoriSerializer
    permission_classes = [IsStaffOrReadOnly]

# 2. ViewSet Supplier
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('id')
    serializer_class = SupplierSerializer
    permission_classes = [IsStaffOrReadOnly]

# 3. ViewSet Barang (Ini yang tadi error ImproperlyConfigured)
class BarangViewSet(viewsets.ModelViewSet):
    queryset = Barang.objects.all().order_by('id')
    serializer_class = BarangSerializer
    permission_classes = [IsStaffOrReadOnly]

# 4. ViewSet Transaksi
class TransaksiPenjualanViewSet(viewsets.ModelViewSet):
    queryset = TransaksiPenjualan.objects.all().order_by('-tanggal')
    serializer_class = TransaksiPenjualanSerializer
    permission_classes = [IsStaffOrReadOnly]
    

# 5. ViewSet Transaksi Pembelian
class TransaksiViewSet(viewsets.ModelViewSet):
    queryset = Transaksi.objects.all().order_by('-tanggal') # Urutkan dari yang terbaru
    serializer_class = TransaksiSerializer
    permission_classes = [permissions.IsAuthenticated] # Hanya user login yang bisa akses
