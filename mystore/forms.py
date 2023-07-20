from django import forms


class PriceFilterForm(forms.Form):
    min_price = forms.DecimalField(decimal_places=2)
    max_price = forms.DecimalField(decimal_places=2)