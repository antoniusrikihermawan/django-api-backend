from django.db import models

class Barang(models.Model):
    kode_barang = models.CharField(max_length=20, unique=True)
    nama_barang = models.CharField(max_length=100)
    kategori = models.CharField(max_length=50)
    harga_satuan = models.DecimalField(max_digits=12, decimal_places=2)
    jumlah_stok = models.IntegerField()
    tanggal_masuk = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_barang
    
class RiwayatTransaksi(models.Model):
    JENIS_TRANSAKSI = [
        ('MASUK', 'Barang Masuk (Restock)'),
        ('KELUAR', 'Barang Keluar (Terjual/Rusak)'),
    ]

    # Menghubungkan riwayat ke barang tertentu
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, related_name='riwayat')
    jenis = models.CharField(max_length=10, choices=JENIS_TRANSAKSI)
    jumlah = models.IntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.jenis} - {self.barang.nama_barang} ({self.jumlah})"