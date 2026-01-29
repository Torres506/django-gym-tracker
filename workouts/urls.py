from django.urls import path
from . import views

urlpatterns = [
    path("", views.workout_list, name="workout_list"),
    path("new/", views.workout_create, name="workout_create"),
    path("<int:pk>/", views.workout_detail, name="workout_detail"),
    path("<int:pk>/add-exercise/", views.workout_add_exercise, name="workout_add_exercise"),
    path("exercise/<int:pk>/", views.workout_exercise_detail, name="workout_exercise_detail"),
    path("item/<int:pk>/sets/new/", views.set_create, name="set_create"),
    path("sets/<int:pk>/delete/", views.set_delete, name="set_delete"),
    path("sets/<int:pk>/edit/", views.set_edit, name="set_edit"),
    path("<int:pk>/edit/", views.workout_edit, name="workout_edit"),
    path("<int:pk>/delete/", views.workout_delete, name="workout_delete"),
    path("stats/", views.workout_stats, name="workout_stats"),
    path("exercise/<int:pk>/delete/", views.workout_exercise_delete, name="workout_exercise_delete"),

]
