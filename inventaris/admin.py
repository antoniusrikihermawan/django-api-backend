from django.contrib import admin
from .models import Kategori, Supplier, Barang, TransaksiPenjualan, Transaksi

admin.site.register(Kategori)
admin.site.register(Supplier)
admin.site.register(Barang)
admin.site.register(TransaksiPenjualan)
admin.site.register(Transaksi)