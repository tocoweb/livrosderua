from typing import BinaryIO
from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # nome=nome,
            # cpf=cpf,
            # telefone=telefone,
            # rua=rua,
            # numero=numero,
            # bairro=bairro,
            # senha=senha,
            # repeat_senha=repeat_senha,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    nome = models.CharField(blank=False, null=False,
                            verbose_name="Nome: ", max_length=250)
    cpf = models.CharField(blank=False, null=False,
                           verbose_name="CPF: ", max_length=15)
    telefone = models.CharField(
        blank=False, null=False, verbose_name="Telefone: ", max_length=15)
    rua = models.CharField(blank=False, null=False,
                           verbose_name="Rua: ", max_length=250)
    numero = models.CharField(blank=False, null=False,
                              verbose_name="Número: ", max_length=6)
    bairro = models.CharField(blank=False, null=False,
                              verbose_name="Bairro: ", max_length=250)
    cidade = models.CharField(blank=False, null=False,
                              verbose_name="Cidade: ", max_length=250)
    email = models.EmailField(blank=False, null=False,
                              verbose_name="E-mail: ", max_length=250, unique=True)
    # senha = models.CharField(blank=False, null=False, verbose_name = "Senha: ", max_length = 250)
    # repeat_senha = models.CharField(blank=False, null=False, verbose_name="Repetir senha: ", max_length=250)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
