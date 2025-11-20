from rest_framework import serializers
from .models import Barang, RiwayatTransaksi

class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = '__all__'
        
class RiwayatTransaksiSerializer(serializers.ModelSerializer):
    # Menampilkan nama barang di API bukan hanya ID
    nama_barang_info = serializers.ReadOnlyField(source='barang.nama_barang')

    class Meta:
        model = RiwayatTransaksi
        fields = ['id', 'barang', 'nama_barang_info', 'jenis', 'jumlah', 'tanggal', 'keterangan']

    # VALIDASI KHUSUS
    def validate(self, data):
        """
        Cek apakah stok cukup jika barang keluar.
        """
        if data['jenis'] == 'KELUAR':
            barang_terkait = data['barang']
            if barang_terkait.jumlah_stok < data['jumlah']:
                raise serializers.ValidationError("Stok tidak cukup untuk melakukan transaksi keluar!")
        return data

    # UPDATE STOK OTOMATIS
    def create(self, validated_data):
        # Simpan data riwayat ke database
        transaksi = RiwayatTransaksi.objects.create(**validated_data)

        # 2. Ambil barang terkait
        barang = transaksi.barang

        # 3. Update stok berdasarkan jenis transaksi
        if transaksi.jenis == 'MASUK':
            barang.jumlah_stok += transaksi.jumlah
        else: 
            barang.jumlah_stok -= transaksi.jumlah
        
        # 4. Simpan perubahan stok barang
        barang.save()

        return transaksi