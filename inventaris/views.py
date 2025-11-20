from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import BarangForm, RiwayatForm
from rest_framework import viewsets
from .models import Barang, RiwayatTransaksi
from .serializers import BarangSerializer, RiwayatTransaksiSerializer

class BarangListView(ListView):
    model = Barang
    template_name = 'inventaris/index.html'
    context_object_name = 'barang_list'
    ordering = ['-tanggal_masuk']

class BarangCreateView(CreateView):
    model = Barang
    form_class = BarangForm
    template_name = 'inventaris/form_barang.html'
    success_url = reverse_lazy('daftar_barang')

class BarangUpdateView(UpdateView):
    model = Barang
    form_class = BarangForm
    template_name = 'inventaris/form_barang.html'
    success_url = reverse_lazy('daftar_barang')

class BarangDeleteView(DeleteView):
    model = Barang
    template_name = 'inventaris/confirm_delete.html' 
    success_url = reverse_lazy('daftar_barang')
    
    # Delete tanpa halaman konfirmasi (Direct Delete dari tombol)
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
# --- VIEW RIWAYAT ---
class RiwayatListView(ListView):
    model = RiwayatTransaksi
    template_name = 'inventaris/riwayat_list.html'
    context_object_name = 'riwayat_list'
    ordering = ['-tanggal'] 

class RiwayatCreateView(CreateView):
    model = RiwayatTransaksi
    form_class = RiwayatForm
    template_name = 'inventaris/form_riwayat.html'
    success_url = reverse_lazy('daftar_riwayat')

    # UPDATE STOK DI WEBSITE
    def form_valid(self, form):
        # 1. Simpan data transaksi
        transaksi = form.save(commit=False)
        
        # 2. Ambil barang yang dipilih
        barang = transaksi.barang
        
        # 3. Cek Validasi Stok untuk Barang Keluar
        if transaksi.jenis == 'KELUAR' and barang.jumlah_stok < transaksi.jumlah:
            form.add_error('jumlah', 'Stok tidak cukup untuk transaksi keluar!')
            return self.form_invalid(form)

        # 4. Update Stok
        if transaksi.jenis == 'MASUK':
            barang.jumlah_stok += transaksi.jumlah
        else:
            barang.jumlah_stok -= transaksi.jumlah
            
        barang.save()     
        transaksi.save() 
        return redirect(self.success_url)

class BarangViewSet(viewsets.ModelViewSet):
    queryset = Barang.objects.all().order_by('-tanggal_masuk')
    serializer_class = BarangSerializer
    
class RiwayatTransaksiViewSet(viewsets.ModelViewSet):
    queryset = RiwayatTransaksi.objects.all().order_by('-tanggal')
    serializer_class = RiwayatTransaksiSerializer
    filterset_fields = ['jenis', 'barang']