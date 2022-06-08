from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your models here.
class Person(models.Model):
    class Meta:
        verbose_name_plural = 'Thành viên'
        
    # list_chucvu = (
	# 		('nhân viên', 'nhân viên'),
	# 		('thủ kho', 'thủ kho'),
    #         ('chủ nhà sách', 'chủ nhà sách'),
    #         ('khách hàng', 'khách hàng')
	# 		) 
    id = models.CharField(max_length=100, primary_key=True, editable=True)
    ho_ten = models.CharField('Họ tên', max_length=100, null=True)
    ngay_sinh = models.DateField('Ngày sinh', null=True, editable=True)
    so_dien_thoai = models.CharField('Số điện thoại', max_length=13, null=True)
    dia_chi = models.CharField('Địa chỉ', max_length=1000, null=True)
    email = models.CharField('Email', max_length=50, null=True)
    # chuc_vu = models.CharField('Chức vụ', max_length=100, null=True, choices=list_chucvu)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE) # a user can have 1 customer, a customer have a user
    
    def __str__(self):
        return self.id

    @property
    def get_group_name(self):
        query_set = Group.objects.filter(user = self.user)
        if not query_set:
            query_set = ''
        else:
            query_set = query_set[0].name.capitalize()
            if query_set == 'Khách hàng':
                query_set = ''

        return query_set

# class TheLoai(models.Model):
    
class Sach(models.Model):
    # id = models.CharField(max_length=100, primary_key=True) # PK: id và ngay_nhap
    ten_sach = models.CharField(max_length=100, null=True)
    ngay_nhap = models.DateField(null=True, editable=True)
    so_luong = models.PositiveIntegerField(null=True)
    the_loai = models.CharField(max_length=100, null=True)
    tac_gia = models.CharField(max_length=100, null=True)
    don_gia = models.PositiveBigIntegerField(null=True)
    gia_ban = models.PositiveBigIntegerField(null=True)
    nha_xuat_ban = models.CharField(max_length=100, null=True)
    nam_xuat_ban = models.PositiveIntegerField(null=True)
    nguoi_nhap = models.ForeignKey(Person, null=True, on_delete=models.PROTECT) 
    anh_sach = models.ImageField(default="static/placeholder.png",null=True, blank=True)
    mo_ta = models.TextField("Mô tả ngắn", max_length=1000, null=True, blank=True)
    # ton_dau = 
    # phat_sinh = 
    # ton_cuoi = 
    
    def __str__(self):
        return f'{self.ten_sach}_{self.ngay_nhap}'
    
    def get_absolute_url(self):
        return f"/book/{self.id}/" 
    
    # def clean(self):
    #     if self.nguoi_nhap.chuc_vu != 'thủ kho':
    #         raise ValidationError('người nhập phải là thủ kho!')

    @property
    def imageURL(self):
        try:
            url = self.anh_sach.url
        except:
            url = ''
        return url
        
    class Meta: # vì django ko cho tạo PK 2 thuộc tính nên làm cách này
        unique_together = ('id', 'ngay_nhap',)
        verbose_name_plural = "Sách"

class HoaDon(models.Model):
    class Meta:
        verbose_name_plural = 'Hóa đơn'
        
    pttt = (
            ('Thẻ ngân hàng', 'Thẻ ngân hàng'),
            ('Tiền mặt', 'Tiền mặt'),
            )
    id_HD = models.CharField('Mã hóa đơn', max_length=100, primary_key=True, default= 'HD_', editable=True)
    ngay_lap_HD = models.DateTimeField(null=True)
    tong_tien = models.FloatField(null=True)
    nguoi_lap_HD = models.ForeignKey(Person, verbose_name='Nhân viên', null=True, blank=True, related_name="nhan_vien", on_delete=models.PROTECT)
    khach_hang = models.ForeignKey(Person, verbose_name='Khách hàng', null=True, blank=True, related_name="khach_hang", on_delete=models.PROTECT)
    phuong_thuc_thanh_toan = models.CharField('Phương thức thanh toán', max_length=100, null=False, choices=pttt)
    da_tra = models.FloatField(null=True)
    
    def __str__(self):
        return self.id_HD
    
    def clean(self):
        # constraint: khách hàng phải có chuc_vu='khách hàng'
        # if self.khach_hang.chuc_vu != 'khách hàng':
        #     raise ValidationError('nhân viên không hợp lệ')
        # # constraint: người lập HD phải là nhân viên
        # if self.nguoi_lap_HD.chuc_vu != 'nhân viên':
        #     raise ValidationError('người lập hóa đơn phải là nhân viên!')
        # constraint: chỉ nợ tối đa 20.000d
        # if self.tong_tien - self.da_tra > 20000:
        #     raise ValidationError('khách hàng chỉ được phép nợ tối đa 20.000d')
        pass

    @property 
    def get_cart_total(self):
        cac_mat_hang = self.chitiethoadon_set.all()
        tong_tien = sum([mh.get_total for mh in cac_mat_hang])
        return tong_tien

    @property
    def get_cart_items(self):
        cac_mat_hang = self.chitiethoadon_set.all()
        total = sum([mh.so_luong for mh in cac_mat_hang])
        return total

class ChiTietHoaDon(models.Model): # 1 lần nhập 1 sách
    # cthd của hóa đơn nào
    hoa_don = models.ForeignKey(HoaDon, verbose_name='Hóa đơn', on_delete=models.PROTECT)
    # khach_hang = models.ForeignKey(Person, verbose_name='Khách hàng', on_delete=models.PROTECT)
    sach = models.ForeignKey(Sach, verbose_name='Sản phẩm', on_delete=models.PROTECT)
    so_luong = models.PositiveIntegerField(null=True, default=0, editable=True)
    # giá bán 1 sản phẩm
    # gia_ban = models.FloatField(null=True)
    
    def __str__(self):
        return self.hoa_don.id_HD

    # def clean(self):
    #     # constraint: sách sau khi bán vẫn còn ít nhất 20 cuốn trong kho Sach   
    @property
    def get_total(self):
        total = self.sach.don_gia * self.so_luong
        return total

    class Meta:
        verbose_name_plural = 'Chi tiết hóa đơn'