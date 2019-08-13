from .models import Comment
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from .models import Vendor


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'theme': 'clean', 'data-callback': "enableBtn"}), label='Проверка, что вы настоящий человек', required=True)

    class Meta:
        model = Comment
        fields = ('name', 'body', 'positiv', 'negativ')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder': 'Введите ваше имя'}),
            'body': forms.Textarea(attrs={'class': 'form-control ',
                                          'rows': '4'}),
            'positiv': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Ваши позитивные впечатления',
                                             'rows': '3'}),
            'negativ': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Ваши негативные впечатления',
                                             'rows': '3'})
        }
        labels = {
            'name': 'Имя',
            'body': 'Ваш отзыв',
            'positiv': 'Достоинства',
            'negativ': 'Недостатки',
        }


class FilterForm(forms.Form):
    brand = forms.ModelMultipleChoiceField(queryset=Vendor.objects.none(), widget=forms.CheckboxSelectMultiple(attrs={'onchange': "document.getElementById('filter_form').submit()"}), required=False)
    min_price = forms.IntegerField(label='от', required=False, widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control mb-2", "placeholder": "от:"
    }))
    max_price = forms.IntegerField(label='до', required=False, widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control mb-2", "placeholder": "до:"
    }))
    ordering = forms.ChoiceField(label="сортировка", required=False, choices=[
        ["-views", "ПО ПОПУЛЯРНОСТИ"],
        ["prices__price", "ДЕШЕВЫЕ СВЕРХУ"],
        ["-prices__price", "ДОРОГИЕ СВЕРХУ"]
    ], widget=forms.Select(attrs={'class': 'short-select', 'onchange': "document.getElementById('filter_form').submit()"}))