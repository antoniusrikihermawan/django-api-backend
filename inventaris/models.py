from django.db import models

# Tabel 1
class Kategori(models.Model):
    nama = models.CharField(max_length=100) 
    def __str__(self): return self.nama

# Tabel 2
class Supplier(models.Model):
    nama_perusahaan = models.CharField(max_length=100)
    
    alamat = models.TextField(blank=True, null=True)
    telepon = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nama_perusahaan

# Tabel 3
class Barang(models.Model):
    nama = models.CharField(max_length=100) 
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.PositiveIntegerField()
    keterangan = models.TextField(blank=True, null=True)
    gambar = models.ImageField(upload_to='barang/', blank=True, null=True) 

    def __str__(self):
        return self.nama

# Tabel 4 (Transaksi Penjualan)
class TransaksiPenjualan(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    total_harga = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    tanggal = models.DateTimeField(auto_now_add=True)
    nama_pembeli = models.CharField(max_length=100, default="Umum", blank=True)
    
    # Fitur Retur
    sudah_diretur = models.BooleanField(default=False)
    alasan_retur = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # 1. Hitung Total Harga
        self.total_harga = self.barang.harga * self.jumlah

        # 2. LOGIKA STOK
        if not self.pk: 
            # --- TRANSAKSI BARU (JUAL) ---
            # Kurangi stok barang
            self.barang.stok -= self.jumlah
            self.barang.save()
        else:
            # --- UPDATE TRANSAKSI (Misal: RETUR) ---
            transaksi_lama = TransaksiPenjualan.objects.get(pk=self.pk)
            
            # Cek: Jika dulunya BELUM diretur, dan sekarang DIRETUR -> Balikin Stok
            if not transaksi_lama.sudah_diretur and self.sudah_diretur:
                self.barang.stok += self.jumlah
                self.barang.save()
            
            # Cek: Jika dulunya SUDAH diretur, tapi dibatalkan (Uncheck) -> Kurangi Stok lagi
            elif transaksi_lama.sudah_diretur and not self.sudah_diretur:
                self.barang.stok -= self.jumlah
                self.barang.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.barang.nama} - {self.jumlah} pcs"

# Tabel 5 (Transaksi Pembelian)
class Transaksi(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, related_name='transaksi')
    jumlah = models.IntegerField()
    nama_pembeli = models.CharField(max_length=100)
    tanggal = models.DateTimeField(auto_now_add=True) # Otomatis isi waktu sekarang

    def __str__(self):
        return f"{self.nama_pembeli} - {self.barang.nama}"
