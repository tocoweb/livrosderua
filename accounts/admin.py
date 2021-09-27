from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    repeat_senha = forms.CharField(
        label='Repetir senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'nome', 'cpf', 'telefone',
                  'rua', 'numero', 'bairro')

    def clean_repeat_senha(self):
        # Check that the two password entries match
        senha = self.cleaned_data.get("senha")
        repeat_senha = self.cleaned_data.get("repeat_senha")
        if senha and repeat_senha and senha != repeat_senha:
            raise ValidationError("As senhas não combinam")
        return repeat_senha

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["senha"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    senha = ReadOnlyPasswordHashField(label=('Senha'), help_text=(
        "As senhas brutas não são armazenadas, portanto, não há como "
        "ver a senha deste usuário, mas você pode alterar a senha usando <a href=\"../password/\">esse formulário</a>."))

    class Meta:
        model = User
        fields = ('email', 'senha', 'nome', 'cpf', 'telefone', 'rua',
                  'numero', 'bairro', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'nome', 'is_active', 'is_admin')
    list_filter = ('bairro', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'senha')}),
        ('Dados pessoais', {
         'fields': ('nome', 'cpf', 'telefone', 'rua', 'numero', 'bairro')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'cpf', 'telefone', 'rua', 'numero', 'bairro', 'senha', 'repeat_senha'),
        }),
    )
    search_fields = ('email', 'nome')
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
