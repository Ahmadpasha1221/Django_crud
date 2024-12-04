from django.urls import path
from django.conf.urls import handler404,handler500
from .views import custom_404_view,custom_500_view
from . import views

urlpatterns = [
    path('',views.login_view,name="login_view"),
    path('signup',views.signup_view,name="signup_view"),
    path('home',views.home_page,name="home_page"),
    path("post/<int:id>/",views.post_detail,name='post_detail'),
    path('post/new',views.create_post,name='create_post'),
    path('post/<int:id>/edit',views.edit_post,name="edit_post"),
    path('post/<int:id>/delete',views.delete_post,name="delete_post"),
    path('logout',views.logout_view,name="logout_view")
]


handler404 = custom_404_view

handler500 = custom_500_view