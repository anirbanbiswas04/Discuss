from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StoryForm, CommentForm
from .models import Story, Vote


def story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    try:
        vote_type = get_object_or_404(Vote, story=story, vote_by=request.user).vote_type
    except:
        vote_type = ''

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.created_by = request.user
            comment.save()

            return redirect('story', story_id=story_id)
    else:
        form = CommentForm()
    
    context = {
        'story': story, 
        'form': form,
        'vote_type': vote_type
        }

    return render(request, 'detail.html', context)


@login_required
def submit(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.created_by = request.user
            story.save()

            return redirect('frontpage')
    else:
        form = StoryForm()

    return render(request, 'submit.html', {'form': form})


@login_required
def up_vote(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    next_page = request.GET.get('next_page', '')

    if story.created_by != request.user:
        if not Vote.objects.filter(story=story).filter(vote_by=request.user):
            Story.up_vote(story)
            Vote.objects.create(story=story, vote_by=request.user, vote_type='up_vote')
        elif Vote.objects.filter(story=story).filter(vote_by=request.user).filter( vote_type='down_vote'):
            Story.up_vote(story)
            Story.up_vote(story)
            Vote.objects.filter(story=story).filter(vote_by=request.user).update(vote_type='up_vote')
        else:
            vote = Vote.objects.filter(story=story).filter(vote_by=request.user).filter(vote_type='up_vote')
            vote.delete()
            Story.down_vote(story)

    if next_page == 'story':
        return redirect('story', story_id=story_id)
    else:
        return redirect('frontpage')
    

@login_required
def down_vote(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    next_page = request.GET.get('next_page', '')

    if story.created_by != request.user:
        if not Vote.objects.filter(story=story).filter(vote_by=request.user):
            Story.down_vote(story)
            Vote.objects.create(story=story, vote_by=request.user, vote_type='down_vote')
        elif Vote.objects.filter(story=story).filter(vote_by=request.user).filter( vote_type='up_vote'):
            Story.down_vote(story)
            Story.down_vote(story)
            Vote.objects.filter(story=story).filter(vote_by=request.user).update(vote_type='down_vote')
        else:
            vote = Vote.objects.filter(story=story).filter(vote_by=request.user).filter(vote_type='down_vote')
            vote.delete()
            Story.up_vote(story)


    if next_page == 'story':
        return redirect('story', story_id=story_id)
    else:
        return redirect('frontpage')