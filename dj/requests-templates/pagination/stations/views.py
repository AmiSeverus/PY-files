from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

import csv

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):

    page_number = 1;

    if is_int(request.GET.get('page', 1)) and int(request.GET.get('page', 1)) > 1:
            page_number = int(request.GET.get('page', 1))

    per_page = 10;

    if is_int(request.GET.get('per_page', 10)) and int(request.GET.get('per_page', 10)) > 10:
        per_page = int(request.GET.get('per_page', 10))


    with open("data-398-2018-08-30.csv", encoding='utf-8') as r_file:    
        DATA = list(csv.DictReader(r_file))

    paginator = Paginator(DATA,per_page)

    page = paginator.get_page(page_number)

    # # получите текущую страницу и передайте ее в контекст
    # # также передайте в контекст список станций на странице

    context = {
    #     'bus_stations': ..., не нужно всё в page
        'page': page,
    }
    return render(request, 'stations/index.html', context)

def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
