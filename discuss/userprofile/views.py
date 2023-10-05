from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from story.models import Story


def account(request):
    user = get_object_or_404(get_user_model(), id=int(request.GET.get('userid', request.user.id)))
    voted_stories = Story.objects.filter(votes__vote_by=user).select_related('created_by')
    own_stories = user.stories.all()

    context = {
        'username':user.username,
        'own_stories' : own_stories,
        'voted_stories': voted_stories
    }

    return render(request, 'account.html', context)

