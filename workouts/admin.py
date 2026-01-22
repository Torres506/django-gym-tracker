from django.contrib import admin
from django.db.models import Max

from .models import Exercise, Workout, WorkoutExercise, SetEntry


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "default_equipment", "is_active")
    list_filter = ("category", "default_equipment", "is_active")
    search_fields = ("name",)


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1
    fields = ("exercise", "equipment",)
    autocomplete_fields = ("exercise",)  # nice if you have many exercises
    show_change_link = True

    def save_new_instance(self, form, commit=True):
        obj = super().save_new_instance(form, commit=False)
        if obj.order == 0:
            max_order = (
                WorkoutExercise.objects
                .filter(workout=obj.workout)
                .aggregate(m=Max("order"))["m"] or 0
            )
            obj.order = max_order + 1
        if commit:
            obj.save()
        return obj


class SetEntryInline(admin.TabularInline):
    model = SetEntry
    extra = 1


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("date", "title")
    search_fields = ("title",)
    inlines = [WorkoutExerciseInline]
