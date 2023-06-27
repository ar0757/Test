from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import home_profiles, homeform
from .models import home_profiles,TimelineEvent
from django.core.paginator import Paginator
from django.db.models import Q

def addhome(request):
    form = homeform()
    if request.method == "POST":
        form = homeform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("home:index"))
    return render(request,"home/add.html",{"form":form})

def index(request):
    chk = request.GET.get('search')
    homes = home_profiles.objects.all().order_by('-id')
    if chk:
        if chk.isdigit():
            homes = homes.filter(
                Q(phone_number__contains=chk)
            )
        else:
                homes = homes.filter(
                    Q(home_name__icontains=chk) |
                    Q(home_address__icontains=chk) |
                    Q(contact_person__icontains=chk) |
                    Q(category__icontains=chk) 
                )
    q = Paginator(home_profiles.objects.all(),10)
    page = request.GET.get('page')
    vols = q.get_page(page)
    return render(request,"home/index.html",{"homes":homes,'vols':vols})

def update_view(request,pk):
    object = get_object_or_404(home_profiles,pk=pk)  # Use the passed pk argument instead of hardcoding it
    if request.method == "POST":
        form = homeform(request.POST, request.FILES, instance=object)
        if form.is_valid():
            form.save()
            return redirect(reverse("home:index"))
    else:
        form = homeform(instance=object)
    return render(request,"home/update.html", {"form": form, "object": object})

def remove_home(request, pk):
    homes = get_object_or_404(home_profiles, pk=pk)
    title = f"Home deleted: {homes.home_name}"
    description = f"Home Address: {homes.home_address} \n Contact Person: {homes.contact_person} \n Phone No: {homes.phone_number}"
    TimelineEvent.objects.create(title=title, description=description)
    homes.delete()
    return redirect(reverse("home:index"))