from django.urls import path
from . import views


# Starting URL:    http://127.0.0.1:8000/api/

urlpatterns = [
    path("profiles", views.getUsers),
    path("bonds", views.getBonds),
    path("bonds/<str:pk>", views.getBond),
    path("create-bond", views.createBond),
    path("edit-bond/<str:pk>", views.editBond),
    path("delete-bond/<str:pk>", views.deleteBond),
    path("buy-bond/<str:pk>", views.buyBond),
    path("view-in-usd", views.viewInUSD),
]
