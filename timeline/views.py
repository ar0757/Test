from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from django.shortcuts import render
from .models import TimelineEvent

def global_timeline(request):
    query = request.GET.get('q')
    date = request.GET.get('date')

    events = TimelineEvent.objects.all()

    if query:
        events = events.filter(Q(title__icontains=query))

    if date:
        events = events.filter(date__date=date)

    events = events.order_by('-date')

    return render(request, 'timeline/global_timeline.html', {'events': events, 'query': query, 'date': date})

    