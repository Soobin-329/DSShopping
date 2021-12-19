from django.shortcuts import render
from mall.models import Product, Category

# Create your views here.
def landing(request):
    recent_products = Product.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html',
                  {'recent_products' : recent_products})

def about_me(request):
    labels = []
    data = []

    queryset = Category.objects.all()

    for label in queryset:
        labels.append(label.name)
        data.append(Product.objects.filter(category=label).count())

    return render(request, 'single_pages/about_me.html', {
        'labels': labels,
        'data': data,
    })