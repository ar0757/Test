from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import hospital_profiles, hospitalform
from .models import hospital_profiles
from django.core.paginator import Paginator
from django.db.models import Q

def addhospital(request):

    form = hospitalform()
    if request.method == "POST":
        form = hospitalform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("hospital:index"))
    return render(request,"hospital/add.html",{"form":form})

def index(request):
    chk = request.GET.get('search')
    hospitals = hospital_profiles.objects.all().order_by('-id')
    if chk:
        if chk.isdigit():
            hospitals = hospitals.filter(
                Q(phone_number__contains=chk)
            )
        else:
                hospitals = hospitals.filter(
                    Q(hospital_name__icontains=chk) |
                    Q(hospital_address__icontains=chk)
                )
    q = Paginator(hospitals,10)
    page = request.GET.get('page')
    vols = q.get_page(page)
    return render(request,"hospital/index.html",{"hospitals":hospitals,'vols':vols})

def update_view(request,pk):
    object = get_object_or_404(hospital_profiles,pk=pk)  # Use the passed pk argument instead of hardcoding it
    if request.method == "POST":
        form = hospitalform(request.POST, request.FILES, instance=object)
        if form.is_valid():
            form.save()
            return redirect(reverse("hospital:index"))
    else:
        form = hospitalform(instance=object)
    return render(request,"hospital/update.html", {"form": form, "object": object})

'''def globally_view_volunteers(request):
    q = Paginator(volunteers,10)
    page = request.GET.get('page')
    vols = q.get_page(page)
    return render(request,"volunteers/volunteersglobalview.html",{"volunteers":volunteers,'vols':vols})'''