from django.urls import path

from . import views

app_name = "prediction"

urlpatterns = [
    path("", views.prediction_form_view, name="form"),
    path("result/<int:pk>/", views.result_view, name="result"),
    path("history/<int:pk>/", views.history_detail_view, name="history_detail"),
    path("history/<int:pk>/delete/", views.history_delete_view, name="history_delete"),
]
