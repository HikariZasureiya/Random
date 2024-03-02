from django import forms

class signinform(forms.Form):
    username = forms.CharField(max_length=100,
            initial='',
            widget=forms.TextInput(attrs={'id': 'id_username', 'class': 'inputclass', 'placeholder': 'Enter username'}
        ))
    
    email = forms.EmailField(initial='',
    
    widget=forms.EmailInput(attrs={'id': 'id_email', 'class': 'inputclass', 'placeholder': 'Enter email'}
        ))

    
    password = forms.CharField(initial='',
        widget=forms.PasswordInput(attrs={'id': 'id_password', 'class': 'inputclass', 'placeholder': 'Enter password'})
        )

class loginform(forms.Form):
    username = forms.CharField(max_length=100,initial='',
            widget=forms.TextInput(attrs={'id': 'id_username', 'class': 'inputclass', 'placeholder': 'Username'}
        ))
    
    password = forms.CharField(initial='',
                widget=forms.PasswordInput(attrs={'id': 'id_password', 'class': 'inputclass', 'placeholder': 'Enter password'})
        )

    
