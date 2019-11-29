"""NewProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import scrumapp
from accounts.views import login_view, register_view, logout_view
from scrumapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', views.dashboard_view.as_view(), name='dashboard'),
    #path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('nuova_board/', views.nuova_board_view, name='nuova_board')
    path('aggiungi_board/', views.nuova_board_view.as_view(), name='aggiungi_board'),
    #path('aggiungi_utente/<int:pk>', views.aggiungi_utente_view.as_view(), name='aggiungi_utente'),
    #path('aggiungi_utente/', views.aggiungi_utente_view.as_view(), name='aggiungi_utente'),
    path('board/<int:pk>', views.board_view.as_view(), name='board'),
    path('crea_colonna', views.nuova_colonna_view.as_view(), name='crea_colonna'),
    path('crea_card', views.nuova_card_view.as_view(), name='crea_card'),
    path('nuovo_utente/<int:pk>', views.new_user_view.as_view(), name='nuovo_utente'),
    path('delete_user/<int:pk>', views.user_delete_view, name='delete_user'),
    path('user_confirm_delete/<int:pk>/<int:id_b>', views.user_confirm_delete_view, name='user_confirm_delete'),
    path('add_user_confirm/<int:pk>/<int:id_b>', views.add_user_confirm, name='add_user_confirm'),
    path('add_user/<int:pk>', views.add_user_view, name='add_user'),
    path('modify_column/<int:pk>', views.modify_column_view, name='modify_column'),
    path('UpdateColumn/<int:pk>', views.UpdateColumn.as_view(), name='UpdateColumn'),
    path('delete_column/<int:pk>', views.delete_column.as_view(), name='delete_column'),
    path('DeleteCard/<int:pk>', views.DeleteCard.as_view(), name='DeleteCard'),
    path('NewCard/<int:pk>', views.NewCard.as_view(), name='NewCard'),
    path('modify_card/<int:pk>', views.modify_card_view, name='modify_card'),
    path('UpdateCard/<int:pk>', views.UpdateCard.as_view(), name='UpdateCard'),
    path('UpdateCardSP/<int:pk>', views.UpdateCardSP.as_view(), name='UpdateCardSP'),
    path('UpdateIdColumn/<int:pk>', views.UpdateIdColumn.as_view(), name='UpdateIdColumn'),
    path('burndown/<int:pk>', views.burndown, name='burndown'),
    path('delete_user_from_card/<int:pk>/<int:id_c>', views.delete_user_from_card_view,
         name='delete_user_from_card'),
    path('add_user_to_card/<int:pk>/<int:id_c>', views.add_user_to_card,
         name='add_user_to_card'),
]

