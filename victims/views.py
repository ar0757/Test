from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import AllProfileForm, VictimLifecycleEntryForm
from .models import All_profiles,TimelineEvent,VictimLifecycleEntry
from django.http import JsonResponse
from .serializers import All_profilesSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



@login_required
def addvictim(request):
    form = AllProfileForm()
    if request.method == "POST":
        form = AllProfileForm(request.POST, request.FILES)  # Add request.FILES parameter
        if form.is_valid():
            new_victim = form.save()
            title = f"New victim added: {new_victim.id}"
            descriptionn = f"Description: {new_victim.description}\n"
            descriptionn += f"Pickup Date: {new_victim.pickup_date}"
            TimelineEvent.objects.create(title=title, description=descriptionn, user=request.user)
            return redirect(reverse("victims:index"))
    return render(request, "victims/add.html", {"form": form})

@login_required
def index(request):
    victims = All_profiles.objects.all().order_by('-id') 
    p = Paginator(All_profiles.objects.all(),10)
    page = request.GET.get('page')
    victims_per_page = p.get_page(page)
    nums = "a" * victims_per_page.paginator.num_pages
    return render(request,"victims/index.html",{"victims":victims,'victims_per_page':victims_per_page,'nums': nums})

@login_required
def update_view(request, pk):
    obj = get_object_or_404(All_profiles, pk=pk)

    if request.method == "POST":
        form = AllProfileForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse("victims:index"))
    else:
        form = AllProfileForm(instance=obj)

    # Get the images associated with the object
    images = obj.image_set.all()

    return render(request, "victims/update.html", {"form": form, "object": obj, "images": images})

@login_required
def globally_view_victims(request):
    chk = request.GET.get('search')
    victims = All_profiles.objects.all().order_by('-id')
    if chk:
        if chk.isdigit():
            victims = victims.filter(
                Q(age=chk) |
                Q(memo_no=chk)
            )
        else:
            if chk.lower() == 'male':
                victims = victims.filter(gender='MALE')
            elif chk.lower() == 'female':
                victims = victims.filter(gender='FEMALE')
            elif chk.lower() == 'other':
                victims = victims.filter(gender='OTHER')
            else:
                victims = victims.filter(
                    Q(first_name__icontains=chk) |
                    Q(last_name__icontains=chk) |
                    Q(description__icontains=chk) |
                    Q(ngo_assigned__icontains=chk) |
                    Q(pickup_location__icontains=chk) 
                )
        try:
            search_date = datetime.strptime(chk, '%Y-%m-%d').date()
                # Calculate the next day to create a date range
            next_day = search_date + timedelta(days=1)
                # Filter by the datetime field (assuming it's a DateTimeField)
            victims = victims.filter(pickup_date__gte=search_date, pickup_date__lt=next_day)
        except ValueError:
            pass
    p = Paginator(victims, 10)
    page = request.GET.get('page')
    victims_per_page = p.get_page(page)
    nums = "a" * victims_per_page.paginator.num_pages
    
    return render(request, "victims/victimsglobalview.html", {"victims_per_page": victims_per_page, "nums": nums})

@api_view(['GET','POST'])
def victims_list(request):
    if request.method == 'GET':
        victims = All_profiles.objects.all()
        serializer = All_profilesSerializers(victims,many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        serializer = All_profilesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def victims_detail(request, id):

    try:
       victims = All_profiles.objects.get(pk=id)
    except All_profiles.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = All_profilesSerializers(victims)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = All_profilesSerializers(victims, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        victims.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@login_required
def viewvicts(request, pk):
    obj = get_object_or_404(All_profiles, pk=pk)
    images = obj.image_set.all()
    return render(request, "victims/viewvictim.html", {"object": obj, "images": images})

@login_required
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_victim_details(request, victim_id):
    try:
        victim = All_profiles.objects.get(id=victim_id)
        serializer = All_profilesSerializers(victim)
        return Response(serializer.data)
    except All_profiles.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)       

@login_required 
def victim_lifecycle_entry_view(request, pk):
    victim = get_object_or_404(All_profiles, pk=pk)
    entries = VictimLifecycleEntry.objects.filter(victim=victim).order_by('-entry_date')

    if request.method == 'POST':
        form = VictimLifecycleEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.victim = victim
            entry.save()
            return redirect('victims:victim_lifecycle_entry', pk=pk)
    else:
        form = VictimLifecycleEntryForm()

    return render(request, 'victims/victim_lifecycle_entry.html', {'victim': victim, 'entries': entries, 'form': form})


