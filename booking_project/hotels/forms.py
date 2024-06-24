from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django import forms


class HotelFilterForm(forms.Form):
    name = forms.CharField(label='Название', required=False)
    location = forms.CharField(label='Местоположение', required=False)
    price_per_night = forms.IntegerField(label='Цена за ночь', required=False)
    city = forms.CharField(label='Город', required=False)
    rating = forms.IntegerField(label='Рейтинг', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                'Фильтры',
                'name',
                'location',
                'price_per_night',
                'city',
                'rating'
            ),
            Submit('submit', 'Применить фильтр', css_class='btn btn-primary')
        )
