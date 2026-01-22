from django import forms

from .models import Workout, WorkoutExercise, SetEntry, Exercise, EquipmentType

# Display-only cleanup so exercise dropdown doesn't feel duplicated
EQUIPMENT_PREFIXES = (
    "Dumbbell ",
    "Barbell ",
    "Machine ",
    "Cable ",
    "Smith ",
    "Bodyweight ",
    "Cardio ",
)


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["date", "title", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"


class WorkoutExerciseForm(forms.ModelForm):
    # extra dropdown (not in the model) used to filter exercises
    category = forms.ChoiceField(
        choices=[("", "---------")] + Exercise.CATEGORY_CHOICES,
        required=False,
        label="Muscle group",
    )

    class Meta:
        model = WorkoutExercise
        fields = ["category", "exercise", "equipment"]

    def __init__(self, *args, **kwargs):
        selected_category = kwargs.pop("selected_category", "")
        super().__init__(*args, **kwargs)

        # Bootstrap styling
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"

        # Optional: blank choice at top for equipment
        self.fields["equipment"].choices = [("", "---------")] + list(EquipmentType.choices)

        # Filter exercises by selected muscle group
        qs = Exercise.objects.filter(is_active=True).order_by("name")
        if selected_category:
            qs = qs.filter(category=selected_category)

        self.fields["exercise"].queryset = qs

        # Display-only: cleaner exercise names in dropdown (optional)
        self.fields["exercise"].label_from_instance = self._label_exercise

        # Pre-fill category dropdown if provided
        if selected_category:
            self.initial["category"] = selected_category

    def _label_exercise(self, ex: Exercise) -> str:
        """
        Display-only cleanup to reduce 'Dumbbell X' + Equipment 'Dumbbell' feeling.
        Does NOT rename anything in the database.
        """
        name = (ex.name or "").strip()
        for prefix in EQUIPMENT_PREFIXES:
            if name.lower().startswith(prefix.lower()):
                return name[len(prefix):].strip()
        return name


class SetEntryForm(forms.ModelForm):
    class Meta:
        model = SetEntry
        fields = ["set_number", "reps", "weight_lb"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"
