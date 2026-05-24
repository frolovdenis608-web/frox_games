from django import forms
from .models import Game, Genre


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'slug', 'description', 'price', 'discount_percent', 'age_rating', 'release_date', 'developer', 'genres', 'cover_image', 'is_active']
        widgets = {

            'genres': forms.CheckboxSelectMultiple(attrs={'style': 'margin-right: 5px; color: white;'}),
            'age_rating': forms.Select(),
            'release_date': forms.DateInput(attrs={'type': 'date', 'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'}),
            'description': forms.Textarea(attrs={'rows': 4, 'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name not in ['release_date', 'description', 'genres']:
                field.widget.attrs.update({
                    'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'
                })

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'
            })