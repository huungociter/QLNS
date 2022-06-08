from django.shortcuts import render, redirect
from .forms import CreateUserForm
from .forms import CreateBook
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from .utils import *
from django.http import HttpResponse, JsonResponse
from .decorators import unauthenticated_user, allowed_users
import math, json
from .filters import BookFilter
from collections import defaultdict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Trang chủ
def home(request):
    if request.user.is_authenticated:
        kh = request.user.person
        chd = list(filter(lambda x: x.da_tra - x.tong_tien == -1 ,HoaDon.objects.filter(khach_hang = kh)))
        if len(chd) <= 0:

            newid_hd = len(HoaDon.objects.all())+1
            if int(newid_hd) <= 9:
                newid_hd = '0'+ str(newid_hd)
            newid_hd = 'HD_0'+ str(newid_hd)
            hd = HoaDon.objects.create(khach_hang = kh, id_HD=newid_hd, da_tra=-1, tong_tien=0)
        else:  
            hd = HoaDon.objects.get(khach_hang = kh, da_tra=-1, tong_tien=0)
        cartItems = hd.get_cart_items
        # print('ID HOA DON: ',hd.id_HD, hd.da_tra, hd.tong_tien)
    else:
        cartItems = 0
    # sach = Sach.objects.all()
    
    
    sach = Sach.objects.order_by('ten_sach')
    myFilter = BookFilter(request.GET,  queryset=sach)
    sach = myFilter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(sach, 12)
   
    try:
        sach = paginator.page(page)
    except PageNotAnInteger:
        sach = paginator.page(1)
    except EmptyPage:
        sach = paginator.page(paginator.num_pages)
    context = {'sach': sach, 'cartItems': cartItems, 'myFilter': myFilter}

    return render(request, 'book/home.html', context)

@login_required(login_url='login')
def cart(request):
    cart_info = get_cart_info(request)
    context = {'mat_hang': cart_info['mat_hang'], 'hd': cart_info['hd'], 'cartItems':cart_info['cartItems']}

    return render(request, 'book/cart.html', context)

@login_required(login_url='login')
def checkout(request):
    ########### Kiệt ###########
    # form = InvoiceForm()
    # if request.method == "POST":
    #     form = InvoiceForm(request.POST)
    #     if form.is_valid():
    #         form.save()
        
    # if request.user.is_authenticated:
    #     kh = request.user.person
    #     if len(HoaDon.objects.filter(khach_hang = kh)) == 0:
    #         newid_hd = len(HoaDon.objects.all())+1
    #         if int(newid_hd) <= 9:
    #             newid_hd = '0'+ str(newid_hd)
    #         newid_hd = 'HD_0'+ str(newid_hd)
    #         hd = HoaDon.objects.create(khach_hang = kh, id_HD=newid_hd)
    #     else:
    #         hd = HoaDon.objects.get(khach_hang = kh)
    #     mat_hang = hd.chitiethoadon_set.all()
    #     cartItems = hd.get_cart_items
    # else:
    #     mat_hang = []
    #     hd = {'get_cart_total': 0, 'get_cart_item': 0}
    #     cartItems = hd.get_cart_items
    # context = {'mat_hang': mat_hang, 'hd': hd, 'cartItems': cartItems}
    ############ Hạ ##############
    cart_info = get_cart_info(request)
    context = {'mat_hang': cart_info['mat_hang'], 'hd': cart_info['hd'], 'cartItems':cart_info['cartItems']}

    return render(request, 'book/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    bookId = data['bookId']
    action = data['action']
    kh = request.user.person
    sach = Sach.objects.get(id=bookId)
    hd = HoaDon.objects.get(khach_hang = kh, da_tra=-1, tong_tien=0)
    mat_hang, created = ChiTietHoaDon.objects.get_or_create(hoa_don=hd, sach=sach)

    if action == 'add':
        if mat_hang.so_luong > mat_hang.sach.get_book_quantity:
            pass
        else:
            mat_hang.so_luong = (mat_hang.so_luong + 1)
            sach.so_luong -= 1
        

    elif action == 'remove':
        mat_hang.so_luong = (mat_hang.so_luong - 1)
        sach.so_luong += 1

    elif action == 'add-amount':
        mat_hang.so_luong = (mat_hang.so_luong + int(data['quantity']))
        sach.so_luong -= int(data['quantity'])

    mat_hang.save()
    sach.save()

    if action == 'clear':
        sach.so_luong += mat_hang.so_luong
        sach.save()
        mat_hang.delete()
    if mat_hang.so_luong <= 0:
        mat_hang.delete()

    return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
def customer_info(request):
    customer = request.user.person
    form = CustomerInfo(instance=customer)
    
    if request.method == "POST":
        form = CustomerInfo(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            print(form.cleaned_data['profile_pic'])
            form.save()
    
    context = {'form': form}
    return render(request, 'book/customer_info.html', context)

@login_required(login_url='login')
def listInvoice(request):
    user = request.user.person
    
    invoices = HoaDon.objects.filter(khach_hang__id=user.id)
    print(invoices)

    context = {'invoices': invoices}
    return render(request, 'book/list_invoice.html', context)

@login_required(login_url='login')
def reviewInvoice(request, pk):
    invoice = HoaDon.objects.get(id_HD=pk)
    details = ChiTietHoaDon.objects.filter(hoa_don=invoice)
    remain = invoice.tong_tien - invoice.da_tra
    context = {'invoice': invoice, 'remain': remain, 'details': details}
    return render(request, 'book/invoice.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            #Create Customer have been taken care of (in signals)
            messages.success(request, 'Account was created for '+ username)
            return redirect('login')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")

    context = {'form': form}
    return render(request, 'book/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username Or Password is incorrect')
    return render(request, 'book/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=['thủ kho'])
def book_entry(request):
    tk = request.user.person
    sach = Sach.objects.all()
    
    form = CreateBook()
    if request.method == "POST":
        form = CreateBook(request.POST, request.FILES)
        form.nguoi_nhap = request.user.person
        if form.is_valid():
            for s in sach :
                if s.ten_sach == form.cleaned_data.get('ten_sach') :
                    
                    if  (form.cleaned_data.get('so_luong') <= 150) | (s.so_luong >= 300) :
                        return redirect('book_entry')
                        
                        # messages.info(request, 'Number of book add must be higher 150 and Book in inventory must have lower 300 :')
                    else :
                        s.ten_sach = form.cleaned_data.get('ten_sach')
                        s.ngay_nhap = form.cleaned_data.get('ngay_nhap')
                        s.the_loai = form.cleaned_data.get('the_loai') 
                        s.tac_gia = form.cleaned_data.get('tac_gia')
                        s.don_gia = form.cleaned_data.get('don_gia')
                        s.gia_ban = form.cleaned_data.get('gia_ban')
                        s.nha_xuat_ban = form.cleaned_data.get('nha_xuat_ban')
                        s.nam_xuat_ban = form.cleaned_data.get('nam_xuat_ban')
                        s.mo_ta = form.cleaned_data.get('mo_ta')
                        s.so_luong += form.cleaned_data.get('so_luong')
                        s.save()
                        return redirect('book_entry')

            if  form.cleaned_data.get('so_luong') <= 150 :
                print(form.cleaned_data.get('so_luong'))
                # messages.info(request, 'Number of book add must be higher 150')
            else :
                print('bcd')
                form.ten_sach = form.cleaned_data.get('ten_sach')
                form.ngay_nhap = form.cleaned_data.get('ngay_nhap')
                form.the_loai = form.cleaned_data.get('the_loai') 
                form.tac_gia = form.cleaned_data.get('tac_gia')
                form.don_gia = form.cleaned_data.get('don_gia')
                form.gia_ban = form.cleaned_data.get('gia_ban')
                form.nha_xuat_ban = form.cleaned_data.get('nha_xuat_ban')
                form.nam_xuat_ban = form.cleaned_data.get('nam_xuat_ban')
                form.mo_ta = form.cleaned_data.get('mo_ta')
                form.so_luong = form.cleaned_data.get('so_luong')
                form.save()
                return redirect('home')
        else:
            print(form.errors.as_data())

    context = {'form': form, 'sach': sach}
    return render(request, 'book/book_entry.html', context)

# Tạo một cuốn sách mới
@login_required(login_url='login')
@allowed_users(allowed_roles=['thủ kho'])
def createBook(request, ):
    # if request.method == "POST":
        # if formset.is_valid():
        #     formset.save()
        #     return redirect('/')

    context = {}

    return render(request, 'book/book_form.html', context)

# Cập nhật một cuốn sách
@login_required(login_url='login')
@allowed_users(allowed_roles=['thủ kho'])
def updateBook(request):
    # if request.method == "POST":
        # if form.is_valid() :
        #     form.save()
        #     return redirect('/')

    context = {}
    return render(request, 'book/book_form.html', context)

# Xóa một cuốn sách
@login_required(login_url='login')
@allowed_users(allowed_roles=['thủ kho'])
def deleteBook(request):

    # if request.method == "POST":
    #     book.delete()
    #     return redirect('/')

    context = {}
    return render(request, 'book/delete_book.html', context)

def book_details(request, pk):
    if request.user.is_authenticated:
        book = Sach.objects.get(id=pk) # truy vấn sách có mã pk từ csdl
        cart_info = get_cart_info(request)
        
    context = {'book': book, 'cartItems':cart_info['cartItems']}

    return render(request, 'book/book.html', context= context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['thủ kho'])
def debt_report(request):
    # advance: lấy thời điểm hiện tại
    current_year, current_month = 2022, 5
    hd_month = HoaDon.objects.filter(ngay_lap_HD__year=current_year, 
                                    ngay_lap_HD__month=current_month)
    
    # nợ đầu: accumulate từ tháng current_month-1 trở về trước
    debt_users = defaultdict(int)
    for i in range(1, current_month):
        hd_month_i = HoaDon.objects.filter(ngay_lap_HD__year=current_year, ngay_lap_HD__month= i)
        for hd in hd_month_i:
            if hd.tong_tien - hd.da_tra != 0:
                debt_users[hd.khach_hang] += (hd.tong_tien - hd.da_tra)
    
    # với những khách nợ, coi thử tháng current_month có phát sinh (nợ) thêm j ko
    incur_user = defaultdict(int)
    for user in debt_users.keys():
        hd_cur_month = HoaDon.objects.filter(khach_hang = user,
                                             ngay_lap_HD__year= current_year, ngay_lap_HD__month= current_month)
        # print('kiem tra: ', hd_cur_month[0].tong_tien)
        try:
            phat_sinh = hd_cur_month[0].tong_tien - hd_cur_month[0].da_tra 
            # if hd_cur_month[0].da_tra == -1: để sửa giỏ hàng, chưa test
            #     phat_sinh = 0
        except:
            phat_sinh = 0
        incur_user[user] += phat_sinh
        
    # biến các debt_users thành các instance thuộc model Debt
    list_debt = []
    for kh, no_dau in debt_users.items():
        debt_user = Debt(khach_hang = kh, no_dau = no_dau, phat_sinh = incur_user[kh])
        list_debt.append(debt_user)
    
    if request.method == "POST":
        month = request.POST.get('month')
        year = request.POST.get('year')
        hd_month = HoaDon.objects.filter(ngay_lap_HD__year=year, 
                                         ngay_lap_HD__month=month)
        
    context = {'hd_month': hd_month, 'list_debt': list_debt}
    return render(request, 'book/debt_report.html', context= context)

@login_required(login_url='login')
def inventory_report(request):
    #book = Sach.objects.get(id=pk) # truy vấn sách có mã pk từ csdl
    
    context = {}
    return render(request, 'book/inventory_report.html', context= context)
