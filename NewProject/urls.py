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
from django.urls import path, include
from scrumapp import views
from django.contrib.auth import views as views1
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', views.Dashboard.as_view(), name='index'),
    # path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('new_board/', views.NewBoardView.as_view(), name='new_board'),
    path('board/<int:pk>', views.BoardDetailView.as_view(), name='board'),
    path('new_column/', views.NewColumnView.as_view(), name='new_column'),
    path('new_card/<int:pk>', views.NewCardView.as_view(), name='new_card'),
    path('new_user/<int:pk>', views.ModifyIdUser.as_view(), name='new_user'),
    path('user_confirm_delete/<int:pk>/<int:id_b>', views.user_confirm_delete_view, name='user_confirm_delete'),
    path('add_user_confirm/<int:pk>/<int:id_b>', views.add_user_confirm, name='add_user_confirm'),
    path('modify_column/<int:pk>', views.modify_column_view, name='modify_column'),
    path('update_column/<int:pk>', views.UpdateColumn.as_view(), name='update_column'),
    path('delete_column/<int:pk>', views.DeleteColumnView.as_view(), name='delete_column'),
    path('delete_card/<int:pk>', views.DeleteCard.as_view(), name='delete_card'),
    path('add_card_to_column/<int:pk>/<int:id_c>', views.add_card_to_column, name='add_card_to_column'),
    path('modify_card/<int:pk>', views.modify_card_view, name='modify_card'),
    path('update_card/<int:pk>', views.UpdateCard.as_view(), name='update_card'),
    path('update_sp_card/<int:pk>', views.UpdateCardSP.as_view(), name='update_sp_card'),
    path('update_id_column/<int:pk>', views.UpdateIdColumn.as_view(), name='update_id_column'),
    path('burndown/<int:pk>', views.burndown, name='burndown'),
    path('delete_user_from_card/<int:pk>/<int:id_c>', views.delete_user_from_card_view,
         name='delete_user_from_card'),
    path('add_user_to_card/<int:pk>/<int:id_c>', views.add_user_to_card,
         name='add_user_to_card'),
]

# path('NewCard/<int:pk>', views.NewCard.as_view(), name='NewCard'),
# path('login/', auth_views.login, name='login'),
# path('login/', login_view, name='login'),
# path('register/', register_view, name='register'),
# path('logout/', logout_view, name='logout'),

# path('dashboard/', views.dashboard_view, name='dashboard'),
# path('nuova_board/', views.nuova_board_view, name='nuova_board')
# path('aggiungi_utente/<int:pk>', views.aggiungi_utente_view.as_view(), name='aggiungi_utente'),
# path('aggiungi_utente/', views.aggiungi_utente_view.as_view(), name='aggiungi_utente'),

#<a href="{% url 'NewCard' col.id %}">Aggiungi una nuova card alla colonna</a>