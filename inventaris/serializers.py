from rest_framework import serializers
from .models import Kategori, Supplier, Barang, TransaksiPenjualan, Transaksi

# 1. Serializer Kategori
class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

# 2. Serializer Supplier
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

# 3. Serializer Barang
class BarangSerializer(serializers.ModelSerializer):
    kategori_nama = serializers.CharField(source='kategori.nama', read_only=True)
    supplier_nama = serializers.CharField(source='supplier.nama_perusahaan', read_only=True)

    class Meta:
        model = Barang
        fields = '__all__'

# 4. Serializer Transaksi
class TransaksiPenjualanSerializer(serializers.ModelSerializer):
    barang_nama = serializers.CharField(source='barang.nama', read_only=True)
    barang_foto = serializers.ImageField(source='barang.gambar', read_only=True)
    
    tanggal = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = TransaksiPenjualan
        fields = [
            'id', 'barang', 'barang_nama', 'barang_foto',
            'jumlah', 'total_harga', 'tanggal', 'nama_pembeli',
            'sudah_diretur', 'alasan_retur'
        ]
        read_only_fields = ['total_harga']

    # Validasi Stok (Mencegah stok minus)
    def validate(self, data):
        barang_dibeli = data['barang']
        jumlah_dibeli = data['jumlah']

        if jumlah_dibeli > barang_dibeli.stok:
            raise serializers.ValidationError({
                "jumlah": f"Stok tidak cukup! Sisa stok: {barang_dibeli.stok}"
            })
        
        return data
    
# Riwayat Transaksi Pembelian
class TransaksiSerializer(serializers.ModelSerializer):
    barang_nama = serializers.ReadOnlyField(source='barang.nama')
    tanggal = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Transaksi
        fields = ['id', 'barang', 'barang_nama', 'jumlah', 'nama_pembeli', 'tanggal']

    # 1. Validasi: Cek apakah stok cukup sebelum simpan
    def validate(self, data):
        if data['jumlah'] > data['barang'].stok:
            raise serializers.ValidationError({"jumlah": "Stok tidak mencukupi!"})
        return data

    # 2. Aksi: Kurangi stok barang saat transaksi dibuat
    def create(self, validated_data):
        transaksi = Transaksi.objects.create(**validated_data)
        
        # Ambil barang terkait
        barang = transaksi.barang
        # Kurangi stok
        barang.stok -= transaksi.jumlah
        # Simpan perubahan stok barang
        barang.save()
        
        return transaksi
