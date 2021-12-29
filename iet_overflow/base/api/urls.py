from django.urls import path
from . import view

urlpatterns = [
    path('', view.getRoutes),
    path('rooms/', view.getRooms),
    path('rooms/<str:id>/', view.getRoom),
]
