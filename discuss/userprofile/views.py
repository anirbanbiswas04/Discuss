from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from story.models import Story


@login_required
def my_account(request):
    own_stories = Story.objects.filter(created_by=request.user)
    name = request.user
    votes = name.vote.all()

    voted_stories = []

    for vote in votes:
        voted_stories.append(vote.story)

    context = {
        'name': name,
        'own_stories': own_stories,
        'voted_stories': voted_stories
    }

    return render(request, 'account.html', context)


def else_account(request, username):
    user = get_object_or_404(User, username=username)
    own_stories = Story.objects.filter(created_by=user)
    votes = user.vote.all()

    voted_stories = []

    for vote in votes:
        voted_stories.append(vote.story)

    context = {
        'name': username,
        'own_stories': own_stories,
        'voted_stories': voted_stories
    }
    
    return render(request, 'account.html', context)
