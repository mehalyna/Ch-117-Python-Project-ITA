from django.forms import CharField, EmailField, Form, PasswordInput, TextInput


class RegistrationForm(Form):
    firstname = CharField(label='Firstname', max_length=100,
                          widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}))
    lastname = CharField(label='Lastname', max_length=100,
                         widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Wick'}))
    email = EmailField(label='Email', max_length=100,
                       widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}))
    login = CharField(label='Login', max_length=100,
                      widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'johny_1234'}))
    password = CharField(label='Password', max_length=100, widget=PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = CharField(label='Confirm password', max_length=100,
                                 widget=PasswordInput(attrs={'class': 'form-control'}))
