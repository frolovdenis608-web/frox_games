from django import forms
from .models import PromoCode

class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['code', 'discount_type', 'value', 'valid_from', 'valid_to', 'active']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local', 'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local', 'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['valid_from', 'valid_to']:
                field.widget.attrs.update({
                    'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'
                })