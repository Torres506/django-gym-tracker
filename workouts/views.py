from decimal import Decimal
from datetime import date, timedelta

from django.db.models import Sum, Count, F, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404

from .models import Workout, WorkoutExercise, SetEntry
from .forms import WorkoutForm, WorkoutExerciseForm, SetEntryForm

from django.shortcuts import get_object_or_404, redirect

def workout_exercise_delete(request, pk):
    we = get_object_or_404(WorkoutExercise, pk=pk)
    workout_id = we.workout.id
    we.delete()
    return redirect("workout_detail", pk=workout_id)


def workout_list(request):
    workouts = Workout.objects.all()
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
        form = WorkoutExerciseForm(
            selected_category=selected_category,
            initial={"category": selected_category},
        )

    return render(
        request,
        "workouts/workout_add_exercise.html",
        {"workout": workout, "form": form, "selected_category": selected_category},
    )


def workout_exercise_detail(request, pk):
    item = get_object_or_404(WorkoutExercise, pk=pk)
    return render(request, "workouts/workout_exercise_detail.html", {"item": item})


def set_create(request, pk):
    item = get_object_or_404(WorkoutExercise, pk=pk)

    if request.method == "POST":
        form = SetEntryForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.workout_exercise = item
            s.save()
            return redirect("workout_detail", pk=item.workout.pk)
    else:
        next_num = (item.sets.count() or 0) + 1
        form = SetEntryForm(initial={"set_number": next_num})

    return render(request, "workouts/set_form.html", {"item": item, "form": form})


def set_delete(request, pk):
    s = get_object_or_404(SetEntry, pk=pk)
    workout_pk = s.workout_exercise.workout.pk

    if request.method == "POST":
        s.delete()
        return redirect("workout_detail", pk=workout_pk)

    return render(request, "workouts/set_confirm_delete.html", {"s": s})


def set_edit(request, pk):
    s = get_object_or_404(SetEntry, pk=pk)
    workout_pk = s.workout_exercise.workout.pk

    if request.method == "POST":
        form = SetEntryForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect("workout_detail", pk=workout_pk)
    else:
        form = SetEntryForm(instance=s)

    return render(
        request,
        "workouts/set_form.html",
        {"item": s.workout_exercise, "form": form, "editing": True},
    )


def workout_edit(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workout_detail", pk=workout.pk)
    else:
        form = WorkoutForm(instance=workout)

    return render(
        request,
        "workouts/workout_form.html",
        {"form": form, "editing": True, "workout": workout},
    )


def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == "POST":
        workout.delete()
        return redirect("workout_list")

    return render(request, "workouts/workout_confirm_delete.html", {"workout": workout})


def workout_stats(request):
    today = date.today()
    last_7 = today - timedelta(days=7)
    last_30 = today - timedelta(days=30)

    # DecimalField * IntegerField => must declare output_field
    volume_expr = ExpressionWrapper(
        F("weight_lb") * F("reps"),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )

    total_workouts = Workout.objects.count()
    workouts_7 = Workout.objects.filter(date__gte=last_7).count()
    workouts_30 = Workout.objects.filter(date__gte=last_30).count()

    total_items = WorkoutExercise.objects.count()
    total_sets = SetEntry.objects.count()

    total_reps = SetEntry.objects.aggregate(
        reps=Coalesce(Sum("reps"), 0)
    )["reps"]

    # Use Decimal("0") so Coalesce doesn't mix Decimal and int
    total_volume = (
        SetEntry.objects.exclude(weight_lb__isnull=True)
        .aggregate(vol=Coalesce(Sum(volume_expr), Decimal("0")))["vol"]
    )

    top_by_volume = (
        SetEntry.objects.exclude(weight_lb__isnull=True)
        .values("workout_exercise__exercise__name")
        .annotate(
            volume=Coalesce(Sum(volume_expr), Decimal("0")),
            sets=Count("id"),
            reps=Coalesce(Sum("reps"), 0),
        )
        .order_by("-volume")[:5]
    )

    top_by_reps = (
        SetEntry.objects.values("workout_exercise__exercise__name")
        .annotate(
            reps=Coalesce(Sum("reps"), 0),
            sets=Count("id"),
        )
        .order_by("-reps")[:5]
    )

    ctx = {
        "today": today,
        "total_workouts": total_workouts,
        "workouts_7": workouts_7,
        "workouts_30": workouts_30,
        "total_items": total_items,
        "total_sets": total_sets,
        "total_reps": total_reps,
        "total_volume": total_volume,
        "top_by_volume": top_by_volume,
        "top_by_reps": top_by_reps,
    }
    return render(request, "workouts/workout_stats.html", ctx)
