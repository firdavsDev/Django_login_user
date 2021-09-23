from django import forms
from django.forms import fields, widgets
from django.forms.forms import Form

from django.contrib.auth import authenticate, get_user_model


User = get_user_model()

class UserLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Bunday foydalanuvchi yuq')
            if not user.check_password(password):
                raise forms.ValidationError('Parol xato')
            if not user.is_active:
                raise forms.ValidationError('Bun foydalanuvchi foal emas')
        return super(UserLogin,self).clean(*args, **kwargs)


class UserRegister(forms.ModelForm):
    email = forms.EmailField(label='Email manzil')
    email2 = forms.EmailField(label='Email manzil tasdiqlag')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]
    def clean(self,*args,**kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError('Emailar bir xil emas')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('Bu email allaqachon ruyxatda o\'tkazilgan ')
        return super(UserRegister,self).clean(*args,**kwargs)
