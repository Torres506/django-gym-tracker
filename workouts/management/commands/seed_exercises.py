from django.core.management.base import BaseCommand
from workouts.models import Exercise

SEED = [
    # Legs
    ("Leg Extension (Machine)", "legs", "machine"),
    ("Leg Press (Machine)", "legs", "machine"),
    ("Leg Curl (Hamstrings)", "legs", "machine"),
    ("Hack Squat (Machine)", "legs", "machine"),
    ("Smith Machine Squat", "legs", "smith"),
    ("Smith Machine Romanian Deadlift", "legs", "smith"),
    ("Hip Abduction Machine (Outer)", "legs", "machine"),
    ("Hip Adduction Machine (Inner)", "legs", "machine"),
    ("Standing Calf Raise (Machine)", "legs", "machine"),

    # Chest
    ("Chest Press Machine", "chest", "machine"),
    ("Dumbbell Bench Press", "chest", "dumbbell"),
    ("Incline Dumbbell Bench Press", "chest", "dumbbell"),
    ("Pec Deck / Fly Machine", "chest", "machine"),
    ("Smith Machine Bench Press", "chest", "smith"),

    # Back
    ("Seated Row Machine (Weight Stack)", "back", "machine"),
    ("Iso-Lateral Plate-Loaded Row (Independent Arms)", "back", "machine"),
    ("Chest-Supported Row (Machine)", "back", "machine"),
    ("Lat Pulldown (Wide / Neutral / Close)", "back", "machine"),
    ("Assisted Pull-Up Machine", "back", "machine"),
    ("Cable Row (Various Attachments)", "back", "cable"),
    ("Straight-Arm Pulldown (Cable)", "back", "cable"),
    ("One-Arm Dumbbell Row", "back", "dumbbell"),

    # Triceps
    ("Cable Triceps Pushdown", "triceps", "cable"),
    ("Overhead Dumbbell Triceps Extension", "triceps", "dumbbell"),
    ("Close-Grip Machine Press", "triceps", "machine"),
    ("Smith Machine Close-Grip Bench Press", "triceps", "smith"),

    # Biceps
    ("Dumbbell Curl (Standing / Alternating)", "biceps", "dumbbell"),
    ("Incline Dumbbell Curl", "biceps", "dumbbell"),
    ("Hammer Curl (Long Head)", "biceps", "dumbbell"),
    ("Concentration Curl", "biceps", "dumbbell"),
    ("Barbell Curl", "biceps", "barbell"),
    ("EZ-Bar Curl", "biceps", "barbell"),
    ("EZ-Bar Preacher Curl", "biceps", "barbell"),
    ("Cable Curl (Various Attachments)", "biceps", "cable"),
    ("Single-Arm High Cable Curl", "biceps", "cable"),

    # Shoulders
    ("Machine Shoulder Press", "shoulders", "machine"),
    ("Dumbbell Shoulder Press", "shoulders", "dumbbell"),
    ("Dumbbell Lateral Raise", "shoulders", "dumbbell"),
    ("Cable Lateral Raise", "shoulders", "cable"),
    ("Rear Delt Fly (Machine)", "shoulders", "machine"),
    ("Face Pull (Cable)", "shoulders", "cable"),

    # Core / Cardio
    ("Hanging Leg Raise (Tower)", "core", "bodyweight"),
    ("Treadmill", "cardio", "cardio"),
    ("StairMaster", "cardio", "cardio"),
]


class Command(BaseCommand):
    help = "Seed the Exercise library with a starter list."

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for name, category, default_equipment in SEED:
            obj, was_created = Exercise.objects.update_or_create(
                name=name,
                defaults={
                    "category": category,
                    "default_equipment": default_equipment,
                    "is_active": True,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Created: {created}, Updated: {updated}."
            )
        )
