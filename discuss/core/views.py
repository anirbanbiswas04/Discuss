from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from story.models import Story


def frontpage(request):
    stories = Story.objects.all().order_by('-number_of_votes')[:20].select_related('created_by')

    return render(request, 'frontpage.html', {'stories': stories})

def newest(request):
    stories = Story.objects.all()[0:100].select_related('created_by')

    return render(request, 'newest.html', {'stories': stories})

def search(request):
    query = request.GET.get('query', None)
    stories = []

    if query:
        stories = Story.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))

    context = {
        'stories': stories, 
        'query': query
        }

    return render(request, 'search.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})