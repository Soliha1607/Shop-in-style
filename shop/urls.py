from django.urls import path
from shop import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('product-detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products-of-category/<int:category_id>/', views.index, name='products_of_category'),
    path('product-create/', views.product_create, name='product_create'),
    path('product-update/<int:product_id>/', views.product_update, name='product_update'),
    path('product-delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('comment-view/<int:pk>/', views.comment_view, name='comment_view'),
    path('order-view/<int:pk>/', views.order_view, name='order_view'),
]