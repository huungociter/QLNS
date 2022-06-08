from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('update_item/', views.updateItem, name='update_item'),
    path('customer_info/', views.customer_info, name='information'),

    
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),


    # path('user/', views.userPage, name='user-page'),

    # path('account/', views.accountSetting, name='account'),

    path('book/<str:pk>/', views.book_details, name='book'), # xem chi tiết sách
    # path('customer/<str:pk_test>', views.customer, name='customer'),

    path('book_entry/', views.book_entry, name='book_entry'),
    # path('create_book/<str:pk>', views.createBook, name='create_Book'),
    # path('update_book/<str:pk>', views.updateBook, name='update_Book'),
    # path('delete_book/<str:pk>', views.deleteBook, name='delete_Book'),

    path('review_invoice/<str:pk>/', views.reviewInvoice, name='review_invoice'),

    path('list_invoice/', views.listInvoice, name='list_invoice'),

    path('debt_report/', views.debt_report, name='debt_report'),
    path('inventory_report/', views.inventory_report, name='inventory_report'),
]
