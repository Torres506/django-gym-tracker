from django.db import models


class EquipmentType(models.TextChoices):
    MACHINE = "MACHINE", "Machine"
    BARBELL = "BARBELL", "Barbell"
    DUMBBELL = "DUMBBELL", "Dumbbell"
    CABLE = "CABLE", "Cable"
    BODYWEIGHT = "BODYWEIGHT", "Bodyweight"


class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ("legs", "Legs"),
        ("back", "Back"),
        ("chest", "Chest"),
        ("shoulders", "Shoulders"),
        ("biceps", "Biceps"),
        ("triceps", "Triceps"),
        ("core", "Core"),
        ("cardio", "Cardio"),
        ("full", "Full Body"),
    ]

    EQUIPMENT_CHOICES = [
        ("machine", "Machine"),
        ("dumbbell", "Dumbbell"),
        ("barbell", "Barbell"),
        ("cable", "Cable"),
        ("smith", "Smith Machine"),
        ("bodyweight", "Bodyweight"),
        ("cardio", "Cardio Machine"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="full")
    default_equipment = models.CharField(max_length=20, choices=EQUIPMENT_CHOICES, default="other")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} {self.title}".strip()


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="items")
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    equipment = models.CharField(max_length=20, choices=EquipmentType.choices)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.workout.date} - {self.exercise.name}"


class SetEntry(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name="sets")
    set_number = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight_lb = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ["set_number"]

    def __str__(self):
        return f"{self.workout_exercise.exercise.name} Set {self.set_number}"
