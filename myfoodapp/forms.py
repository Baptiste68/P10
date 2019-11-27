from django import forms


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput)


class NewUserForm(forms.Form):
    first_name = forms.CharField(label="Prénom", max_length=30)
    last_name = forms.CharField(label="Nom", max_length=30)
    email = forms.EmailField()
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput)


class ChangePwd(forms.Form):
    old_password = forms.CharField(label="Mot de passe actuel",
                               widget=forms.PasswordInput)
    new_password = forms.CharField(label="Nouveau mdp",
                               widget=forms.PasswordInput)
    new_password_b = forms.CharField(label="Rettaper mdp",
                               widget=forms.PasswordInput)
