from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from .models import Barang, Supplier, Kategori

class TailwindFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_style = 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-accent outline-none transition'
        
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} {css_style}".strip()

class BarangForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Barang
        fields = '__all__'
        widgets = {
            'deskripsi': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_harga_satuan(self):
        harga = self.cleaned_data.get('harga_satuan')
        if harga < 0:
            raise ValidationError("Harga tidak boleh negatif.")
        return harga
