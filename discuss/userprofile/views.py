from django.shortcuts import render
from story.models import Story


def account(request):
    user = request.GET.get('user', request.user)
    voted_stories = Story.objects.filter(votes__vote_by=user).select_related('created_by')
    own_stories = user.stories.all()

    context = {
        'username':user.username,
        'own_stories' : own_stories,
        'voted_stories': voted_stories
    }

    return render(request, 'account.html', context)

