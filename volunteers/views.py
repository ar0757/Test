from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import volunteer_profiles, volunteerform
from .models import volunteer_profiles,TimelineEvent
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def addvolunteer(request):

    form = volunteerform()
    if request.method == "POST":
        form = volunteerform(request.POST,request.FILES)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.user = request.user
            volunteer.save()
            return redirect(reverse("volunteers:index"))
    return render(request,"volunteers/add.html",{"form":form})

@login_required
def index(request):
    chk = request.GET.get('search')
    volunteers = volunteer_profiles.objects.all().order_by('-id')
    if chk:
        if chk.isdigit():
            volunteers = volunteers.filter(
                Q(age=chk) |
                Q(phone_number=chk)
            )
        else:
            if chk.lower() == 'male':
                volunteers = volunteers.filter(gender='MALE')
            elif chk.lower() == 'female':
                volunteers = volunteers.filter(gender='FEMALE')
            elif chk.lower() == 'other':
                volunteers = volunteers.filter(gender='OTHER')
            else:
                volunteers = volunteers.filter(
                    Q(first_name__icontains=chk) |
                    Q(last_name__icontains=chk) |
                    Q(ngo_association__icontains=chk) |
                    Q(area_of_operation__icontains=chk) 
                )
    q = Paginator(volunteer_profiles.objects.all(),10)
    page = request.GET.get('page')
    vols = q.get_page(page)
    return render(request,"volunteers/index.html",{"volunteers":volunteers,'vols':vols})

@login_required
def update_view(request,pk):
    object = get_object_or_404(volunteer_profiles,pk=pk)  # Use the passed pk argument instead of hardcoding it
    if request.method == "POST":
        form = volunteerform(request.POST, request.FILES, instance=object)
        if form.is_valid():
            form.save()
            return redirect(reverse("volunteers:index"))
    else:
        form = volunteerform(instance=object)
    return render(request,"volunteers/update.html", {"form": form, "object": object})

@login_required
def remove_volunteer(request, pk):
    volunteer = get_object_or_404(volunteer_profiles, pk=pk)
    title = f"Volunteer removed: {volunteer.first_name} {volunteer.last_name}"
    description = f"Phone No: {volunteer.phone_number}"
    TimelineEvent.objects.create(title=title, description=description)
    volunteer.delete()
    return redirect(reverse("volunteers:index"))