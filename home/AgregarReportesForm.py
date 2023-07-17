from django import forms
from .models import Producto_venado, Produccion_venado, Distribuciones_venado

class ProduccionDistribucionForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto_venado.objects.all())
    fecha_mensual = forms.DateField(
        input_formats=['%Y-%m'],
        widget=forms.DateInput(attrs={'type': 'month'}),
    )
    cantidad_produccion = forms.IntegerField()
    canal_horizontal = forms.IntegerField()
    canal_tradicional = forms.IntegerField()
    canal_moderno = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')

        # Verificar si el producto seleccionado existe
        if producto is not None:
            marca_producto = producto.marca_id
            cleaned_data['marca_producto'] = marca_producto
            cleaned_data['total_cantidad_distribucion'] = self.calcular_total_distribucion()

        return cleaned_data

    def calcular_total_distribucion(self):
        canal_horizontal = self.cleaned_data.get('canal_horizontal')
        canal_tradicional = self.cleaned_data.get('canal_tradicional')
        canal_moderno = self.cleaned_data.get('canal_moderno')

        return canal_horizontal + canal_tradicional + canal_moderno

