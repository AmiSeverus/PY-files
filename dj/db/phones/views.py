from django.shortcuts import render

from phones.models import Phone


def show_catalog(request):
    sort = request.GET.get('sort', '').lower().strip()
    context = {}
    if sort == 'name':
        phones = list(Phone.objects.order_by('name').values())
    elif sort == 'price_asc':
        phones = list(Phone.objects.order_by('price').values())
    elif sort == 'price_desc':
        phones = list(Phone.objects.order_by('price').reverse().values())
    else:
        phones = list(Phone.objects.values())
    template = 'catalog.html'
    context['phones'] = phones
    context['sort'] = sort
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {}
    phone = list(Phone.objects.filter(slug=slug).values())
    if len(phone) > 0:
        phone = phone[0]
        context['phone'] = phone
    return render(request, template, context)
