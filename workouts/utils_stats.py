def e1rm(weight, reps):
    if not weight or not reps:
        return 0
    return round(weight * (1 + reps / 30), 1)


def top_set(sets):
    """
    Best set by estimated 1RM (tie-break weight, then reps).
    SetEntry uses weight_lb, not weight.
    """
    best = None
    best_score = -1

    for s in sets:
        w = float(getattr(s, "weight_lb", 0) or 0)
        r = getattr(s, "reps", 0) or 0
        score = e1rm(w, r)

        if score > best_score:
            best = s
            best_score = score

    return best


def progression_hint(all_sets, target_low=8, target_high=10):
    reps = [(s.reps or 0) for s in all_sets if s.reps is not None]
    if not reps:
        return "Log reps next time"
    if all(r >= target_high for r in reps):
        return "Increase weight next time"
    if any(r < target_low for r in reps):
        return "Keep weight, aim for 8+ reps"
    return "Keep weight, add reps"


# Temporary mapping (no model change needed)
MUSCLE_MAP = {
    # Chest
    "Bench Press": "chest",
    "Incline Dumbbell Bench Press": "chest",
    "Incline Bench Press": "chest",
    "Chest Press Machine": "chest",
    "Smith Machine Bench Press": "chest",
    "Pec Deck / Fly Machine": "chest",
    "Close-Grip Machine Press": "chest",

    # Back
    "Lat Pulldown (Wide / Neutral / Close)": "back",
    "Seated Row Machine (Weight Stack)": "back",
    "Cable Row (Various Attachments)": "back",
    "Chest-Supported Row (Machine)": "back",

    # Arms
    "Bicep Curl": "arms",
    "Cable Curl (Various Attachments)": "arms",
    "Cable Triceps Pushdown": "arms",

    # Legs
    "Leg Press (Machine)": "legs",
    "Leg Extension (Machine)": "legs",
    "Leg Curl (Hamstrings)": "legs",
    "Standing Calf Raise (Machine)": "legs",
    "Hip Abduction Machine (Outer)": "legs",
    "Hip Adduction Machine (Inner)": "legs",

    # Core
    "Hanging Leg Raise (Tower)": "core",
    "Crunch kick": "core",
    "Crunch": "core",
    "Heel Touches": "core",
}

def muscle_for(exercise_name):
    return MUSCLE_MAP.get(exercise_name, "other")
