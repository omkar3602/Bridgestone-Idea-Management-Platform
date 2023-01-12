from django.shortcuts import render
from .models import BusinessUnit
from django.http import HttpResponse

# Create your views here.
def index(request):
    bussiness_units = BusinessUnit.objects.all()

    context = {
        'bussiness_units':bussiness_units,
    }
    if request.user.is_authenticated:
        if request.user.is_admin:
            return render(request, 'mainapp/index.html', context)
        elif request.user.is_IC:
            return render(request, 'mainapp/index.html', context)
        else:
            return render(request, 'mainapp/ideator/home.html', context)
    else:
        return render(request, 'mainapp/index.html', context)

def new_submission(request):
    return HttpResponse("New submission")