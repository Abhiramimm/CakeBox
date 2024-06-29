from django.urls import path

from api import views


urlpatterns=[

    path("cakes/",views.CakeListView.as_view()),

]