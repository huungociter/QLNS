from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomerInfo(ModelForm):
    class Meta:
        model = Person
        fields = ['ho_ten', 'so_dien_thoai', 'email', 'profile_pic']

class CreateBook(ModelForm):
    class Meta:
        model = Sach
        fields = ['ten_sach', 'ngay_nhap', 'so_luong', 'the_loai', 'tac_gia', 'don_gia', 'gia_ban', 'nha_xuat_ban', 'nam_xuat_ban', 'anh_sach', 'mo_ta']
