from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    # path('register/', views.register, name='register'), ## url d'inscription
    # path('login/', views.login, name='login'),  ## url de connexion
    # path('logout/', views.logout, name='logout'),   ## url de deconnexion


    # path('dashboard/', views.dashboard, name='dashboard'),   ## url de deconnexion
    # path('', views.dashboard, name='dashboard'), ## permet de mettre que account dans l'url pour etre renvoyer sur la pager du dashboard


    # path('activate/<uidb64>/<token>/', views.activate, name = 'activate'),  ## Pour email de configuration on recupere l'id cripté et le token
    # ## c'est url envoyé dans le lien à l'user


    # path('forgotPassword/', views.forgotPassword, name = 'forgotPassword'),
    # path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name = 'resetpassword_validate'),
    # path('resetPassword/', views.resetPassword, name = 'resetPassword'),

    # path('my_orders/', views.my_orders, name="my_orders"), ## url de recap des commandes effecté par l'user
    # path('edit_profile/', views.edit_profile, name='edit_profile'),  ## Permet de modifier l'userProfile dans le dashboard
    # path('change_password/', views.change_password, name='change_password'),  ## Permet de modifier le mot de passe dans le dashboard
    # path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),  ## Permet d'avoir accées au detail de la commande dans le dashboard 



]