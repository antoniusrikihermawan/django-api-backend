from django.contrib import admin
from .models import Barang, RiwayatTransaksi

@admin.register(Barang)
class BarangAdmin(admin.ModelAdmin):
    list_display = ('kode_barang', 'nama_barang', 'kategori', 'harga_satuan', 'jumlah_stok', 'tanggal_masuk')
    search_fields = ('kode_barang', 'nama_barang', 'kategori')
    list_filter = ('kategori', 'tanggal_masuk')
    ordering = ('nama_barang',)

@admin.register(RiwayatTransaksi)
class RiwayatAdmin(admin.ModelAdmin):
    list_display = ('barang', 'jenis', 'jumlah', 'tanggal')
    search_fields = ('barang__nama_barang', 'jenis')
    list_filter = ('jenis', 'tanggal')
    ordering = ('-tanggal',)
