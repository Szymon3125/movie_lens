from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import InlineCheckboxes

from userview.models import Movie, User, Genre


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    username = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'class': 'bg-dark link-light',
            },
        ),
    )

    email = forms.EmailField(
        widget = forms.TextInput(
            attrs = {
                'class': 'bg-dark link-light',
            },
        ),
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'bg-dark link-light',
            },
        ),
    )

    confirm_password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'bg-dark link-light',
            },
        ),
    )
    


class LoginForm(forms.Form):
    class Meta:
        fields = ['username', 'password']
    
    username = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'class': 'bg-dark link-light',
            },
        ),
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'bg-dark link-light',
            },
        ),
    )


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'imageURL']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'title',
            'description',
            InlineCheckboxes('genres'),
            'imageURL',
        )
        print(self.helper.layout.fields)

    def save(self, commit=True):
        movie = super().save(commit=False)
        if commit:
            movie.save()
        movie.genres.set(self.cleaned_data['genres'])
        return movie
    
    title = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'class': 'bg-dark link-light',
            },
        ),
    )

    description = forms.CharField(
        required = False,
        widget = forms.Textarea(
            attrs = {
                'class': 'bg-dark link-light',
            },
        ),
    )

    genres = forms.MultipleChoiceField(
        choices = Genre.objects.all().values_list('id', 'name'),
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )

    imageURL = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'bg-dark link-light',
            },
        ),
    )

