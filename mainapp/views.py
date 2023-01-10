from django.shortcuts import render

# Create your views here.
def index(request):
    # subjects = Subject.objects.all()

    context = {
        # 'subjects':subjects,
    }
    return render(request, 'mainapp/index.html', context)