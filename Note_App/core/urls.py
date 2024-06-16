from django.urls import path
from . import views

urlpatterns = [
    # Frontend URls
    #-----------------------------------#
    path('home/', views.home, name="Home"),
    path('', views.login_page, name="login_page"),
    path('register/', views.register_page, name="register_page"),
    path('logout/', views.logout_page, name="logout_page"),
    path('about/', views.about, name='about'),

    # Backend URls
    #-----------------------------------#
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('note/new/', views.note_create, name='note_create'),
    path('note/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),

]
