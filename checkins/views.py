from django.shortcuts import render, redirect
from .models import CheckIn
from .forms import CheckInForm
from django.shortcuts import get_object_or_404

def checkin_list(request):
    checkins = CheckIn.objects.order_by("-date")

    latest = checkins.first()
    previous = checkins[1] if checkins.count() > 1 else None

    def delta(current, prev):
        if current is None or prev is None:
            return None
        return current - prev

    weight_delta = None
    waist_delta = None

    if latest and previous:
        weight_delta = delta(latest.weight_lb, previous.weight_lb)
        waist_delta = delta(latest.waist_in, previous.waist_in)

    context = {
        "checkins": checkins,
        "latest": latest,
        "previous": previous,
        "weight_delta": weight_delta,
        "waist_delta": waist_delta,
    }
    return render(request, "checkins/checkin_list.html", context)

def checkin_create(request):
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('checkin_list')
    else:
        form = CheckInForm()


    return render(request, 'checkins/checkin_form.html', {'form': form})

def checkin_edit(request, pk):
    checkin = get_object_or_404(CheckIn, pk=pk)

    if request.method == 'POST':
        form = CheckInForm(request.POST, instance=checkin)
        if form.is_valid():
            form.save()
            return redirect('checkin_list')
    else:
        form = CheckInForm(instance=checkin)

    return render(request, 'checkins/checkin_form.html', {'form': form})

def checkin_delete(request, pk):
    checkin = get_object_or_404(CheckIn, pk=pk)

    if request.method == 'POST':
        checkin.delete()
        return redirect('checkin_list')

    return render(request, 'checkins/checkin_confirm_delete.html', {'checkin': checkin})
