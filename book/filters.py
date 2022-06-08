import django_filters
from django.forms.widgets import TextInput
from .models import Sach

class BookFilter(django_filters.FilterSet):
    ten_sach = django_filters.CharFilter(field_name='ten_sach', 
            lookup_expr='icontains', label='', widget=TextInput(attrs={'placeholder': "Tìm kiếm sách mong muốn ...", "class":"form-control w-75"})) #mr-sm-2 
    # gia_ban = django_filters.NumberFilter(field_name='gia_ban',lookup_expr='lt', label='Giá sách (tối đa)')

    class Meta:
        model = Sach
        fields = {}

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['ten_sach'].widget
