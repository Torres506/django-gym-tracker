from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Workout, WorkoutExercise, SetEntry
from .forms import WorkoutForm, WorkoutExerciseForm, SetEntryForm


# --------------------------------------------------
# WORKOUT CRUD
# --------------------------------------------------

def workout_list(request):
    workouts = Workout.objects.all().order_by("-date")
    return render(request, "workouts/workout_list.html", {"workouts": workouts})


def workout_create(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save()
            return redirect("workout_detail", pk=workout.pk)
    else:
        form = WorkoutForm()
    return render(request, "workouts/workout_form.html", {"form": form})


def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    items = workout.items.select_related("exercise").prefetch_related("sets").all()
    return render(request, "workouts/workout_detail.html", {"workout": workout, "items": items})


def workout_edit(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workout_detail", pk=workout.pk)
    else:
        form = WorkoutForm(instance=workout)
    return render(request, "workouts/workout_form.html", {"form": form, "editing": True, "workout": workout})


def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if request.method == "POST":
        workout.delete()
        return redirect("workout_list")
    return render(request, "workouts/workout_confirm_delete.html", {"workout": workout})


# --------------------------------------------------
# WORKOUT EXERCISES + SETS
# --------------------------------------------------

def workout_add_exercise(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    selected_category = request.GET.get("category", "")

    if request.method == "POST":
        selected_category = request.POST.get("category", selected_category)
        form = WorkoutExerciseForm(request.POST, selected_category=selected_category)
        if form.is_valid():
            we = form.save(commit=False)
            we.workout = workout
            we.save()
            return redirect("workout_detail", pk=workout.pk)
    else:
        form = WorkoutExerciseForm(selected_category=selected_category, initial={"category": selected_category})

    return render(request, "workouts/workout_add_exercise.html", {
        "workout": workout,
        "form": form,
        "selected_category": selected_category,
    })


def workout_exercise_detail(request, pk):
    item = get_object_or_404(WorkoutExercise, pk=pk)
    return render(request, "workouts/workout_exercise_detail.html", {"item": item})


def workout_exercise_delete(request, pk):
    we = get_object_or_404(WorkoutExercise, pk=pk)
    workout_id = we.workout_id
    we.delete()
    return redirect("workout_detail", pk=workout_id)


def set_create(request, pk):
    item = get_object_or_404(WorkoutExercise, pk=pk)
    if request.method == "POST":
        form = SetEntryForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.workout_exercise = item
            s.save()
            return redirect("workout_detail", pk=item.workout_id)
    else:
        next_num = item.sets.count() + 1
        form = SetEntryForm(initial={"set_number": next_num})
    return render(request, "workouts/set_form.html", {"item": item, "form": form})


def set_edit(request, pk):
    s = get_object_or_404(SetEntry, pk=pk)
    workout_pk = s.workout_exercise.workout_id
    if request.method == "POST":
        form = SetEntryForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect("workout_detail", pk=workout_pk)
    else:
        form = SetEntryForm(instance=s)
    return render(request, "workouts/set_form.html", {"item": s.workout_exercise, "form": form, "editing": True})


def set_delete(request, pk):
    s = get_object_or_404(SetEntry, pk=pk)
    workout_pk = s.workout_exercise.workout_id
    if request.method == "POST":
        s.delete()
        return redirect("workout_detail", pk=workout_pk)
    return render(request, "workouts/set_confirm_delete.html", {"s": s})


# --------------------------------------------------
# PROGRESSIVE OVERLOAD (DOUBLE PROGRESSION)
# --------------------------------------------------

def workout_stats(request):
    today = date.today()

    total_workouts = Workout.objects.count()
    workouts_7 = Workout.objects.filter(date__gte=today - timedelta(days=7)).count()
    workouts_30 = Workout.objects.filter(date__gte=today - timedelta(days=30)).count()

    progress_data = []

    exercise_ids = SetEntry.objects.values_list(
        "workout_exercise__exercise_id",
        flat=True
    ).distinct()

    for ex_id in exercise_ids:

        dates = (
            SetEntry.objects
            .filter(workout_exercise__exercise_id=ex_id)
            .values_list("workout_exercise__workout__date", flat=True)
            .distinct()
            .order_by("-workout_exercise__workout__date")
        )

        if len(dates) < 2:
            continue

        last_date = dates[0]
        prev_date = dates[1]

        last_best = (
            SetEntry.objects
            .filter(workout_exercise__exercise_id=ex_id,
                    workout_exercise__workout__date=last_date)
            .exclude(weight_lb__isnull=True)
            .order_by("-weight_lb", "-reps")
            .first()
        )

        prev_best = (
            SetEntry.objects
            .filter(workout_exercise__exercise_id=ex_id,
                    workout_exercise__workout__date=prev_date)
            .exclude(weight_lb__isnull=True)
            .order_by("-weight_lb", "-reps")
            .first()
        )

        if not last_best or not prev_best:
            continue

        # DOUBLE PROGRESSION LOGIC
        if last_best.weight_lb > prev_best.weight_lb:
            improvement = "up"
            change = f"+{last_best.weight_lb - prev_best.weight_lb} lb"
        elif last_best.weight_lb == prev_best.weight_lb and last_best.reps > prev_best.reps:
            improvement = "up"
            change = f"+{last_best.reps - prev_best.reps} reps"
        elif last_best.weight_lb == prev_best.weight_lb and last_best.reps == prev_best.reps:
            improvement = "same"
            change = "0"
        else:
            improvement = "down"
            if last_best.weight_lb < prev_best.weight_lb:
                change = f"-{prev_best.weight_lb - last_best.weight_lb} lb"
            else:
                change = f"-{prev_best.reps - last_best.reps} reps"

        pr_set = (
            SetEntry.objects
            .filter(workout_exercise__exercise_id=ex_id)
            .exclude(weight_lb__isnull=True)
            .order_by("-weight_lb", "-reps")
            .first()
        )

        exercise_name = (
            SetEntry.objects
            .filter(workout_exercise__exercise_id=ex_id)
            .values_list("workout_exercise__exercise__name", flat=True)
            .first()
        )

        progress_data.append({
            "exercise": exercise_name,
            "last_date": last_date,
            "prev_date": prev_date,
            "last_weight": last_best.weight_lb,
            "last_reps": last_best.reps,
            "prev_weight": prev_best.weight_lb,
            "prev_reps": prev_best.reps,
            "improvement": improvement,
            "change": change,
            "pr_weight": pr_set.weight_lb if pr_set else None,
            "pr_reps": pr_set.reps if pr_set else None,
        })

    return render(request, "workouts/workout_stats.html", {
        "today": today,
        "total_workouts": total_workouts,
        "workouts_7": workouts_7,
        "workouts_30": workouts_30,
        "progress_data": progress_data,
    })
