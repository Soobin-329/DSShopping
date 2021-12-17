from django.urls import path
from . import views

urlpatterns = [

#    path('search/<str:q>/', views.PostSearch.as_view()),
#    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
#    path('create_post/', views.PostCreate.as_view()),
    path('category/<str:slug>', views.category_page),   # 서버IP/mall/category/slug
#    path('<int:pk>/new_comment/', views.new_comment),
    path('<int:pk>/', views.ProductDetail.as_view()),
    path('', views.ProductList.as_view()),
]