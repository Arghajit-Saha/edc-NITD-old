from django.shortcuts import render
from .models import *
from esummit.models import Year_Detail
import datetime
from json import dumps
from datetime import timezone

def event(request):
    day = datetime.datetime.now()
    tdelta = datetime.timedelta(days=45)
    now = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)

    ongoing_event = Event.objects.filter(start_date__lte=now, end_date__gte=now)
    upcoming_event = Event.objects.filter(start_date__gt=now, start_date__lte=now+tdelta).exclude(start_date__lte=now, end_date__gte=now)
    all_event = Event.objects.all()
    next_oe = Event.objects.filter(start_date__gte=now).order_by('start_date')
    next_ue = Event.objects.filter(start_date__gte=now+tdelta).order_by('start_date')

    try:
        for item in next_oe:
            if item.start_date > now:
                next_oe = item.start_date
                break
    except:
        next_oe = 0

    try:
        for item in next_ue:
            if item.start_date > now:
                next_ue = item.start_date - tdelta
                break
    except:
        next_ue = 0

    oe_count = 0
    ue_count = 0
    ae_count = 0

    if Event.objects.filter(start_date__lte=now, end_date__gte=now).count() > 0:
        oe_count = 1

    if Event.objects.filter(start_date__gte=now, start_date__lte=now+tdelta).exclude(start_date__lte=now, end_date__gte=now).count() > 0:
        ue_count = 1

    if Event.objects.count() > 0:
        ae_count = 1

    timerJSON = dumps({'next_oe': next_oe,
                       'next_ue': next_ue,
                       'oe': oe_count,
                       'ue': ue_count,
                      }, default=str)
    context = {'ue': upcoming_event, 'oe': ongoing_event, 'ae': all_event, 'ae_count': ae_count, 'ue_count': ue_count, 'oe_count': oe_count, 'timer': timerJSON}

    year = Year_Detail.objects.all().order_by("-year")
    context['years'] = year
    max_year = 0
    max_id = 0
    for y in Year_Detail.objects.all():
        if y.year > max_year:
            max_year = y.year
            max_id = y.id
    context['latest'] = max_id
    context['latest_year'] = max_year % 100
    return render(request, 'events/event_page.html', context)


def eventdetails(request, id):
    if request.method == "POST":
        event = Event.objects.get(pk=id)
        images = EventImages.objects.filter(event=event)
        timeline = Timeline.objects.filter(event=event)
        prize = Prize.objects.filter(event=event)

        length = len(timeline)
        number_of_images = len(images)

        tdelta = datetime.timedelta(days=45)
        now = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
        ongoing_event = Event.objects.filter(start_date__lte=now, end_date__gte=now)
        upcoming_event = Event.objects.filter(start_date__gt=now, start_date__lte=now+tdelta).exclude(start_date__lte=now, end_date__gte=now)

        context = {'event': event, 'images': images, 'timeline': timeline, 'prize': prize, 'length': length, 'number': number_of_images, 'ue': upcoming_event, 'oe': ongoing_event}
        return render(request, 'events/eventdetails.html', context)
