from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import TimelineEvent

def global_timeline(request):
    events = TimelineEvent.objects.order_by('-date')
    return render(request, 'timeline/global_timeline.html', {'events': events})
