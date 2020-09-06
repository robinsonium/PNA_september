from django.urls import path,include
from . import views

urlpatterns = [
    path('all_recipes',views.all_recipes),
    path('detail/<int:id>',views.detail),
    path('logout',views.logout),
    path('login',views.login),
    path('register',views.register),
    path('', views.index),
    path('create',views.create),
    path('review/<int:id>',views.review),
    path('edit_account/<int:id>',views.edit_account),
    path('edit_recipe/<int:id>',views.edit_recipe),
    path('delete_recipe/<int:id>',views.delete_recipe),
]