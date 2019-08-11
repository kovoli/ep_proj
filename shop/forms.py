from .models import Comment
from django import forms
from captcha.fields import ReCaptchaField
from .models import Vendor


class CommentForm(forms.ModelForm):
    #captcha = ReCaptchaField(label='Проверка, что вы настоящий человек',
                             #attrs={'theme': 'clean', 'callback': "enableBtn"}, required=True, )

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