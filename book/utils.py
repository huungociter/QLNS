from .models import *
from django.contrib.auth.models import Group

def get_cart_info(request):
    if request.user.is_authenticated:
        kh = request.user.person
        hd = HoaDon.objects.get(khach_hang = kh, da_tra=-1, tong_tien=0)
        mat_hang = hd.chitiethoadon_set.all()
        cartItems = hd.get_cart_items
    return {'mat_hang': mat_hang, 'hd':hd, 'cartItems': cartItems}