from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def stock_master(request):
    return render(request, 'outbound/outbound.html')  # Renders the base template
