from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StoryForm, CommentForm
from .models import Story, Vote


def story(request, story_id):
    story = get_object_or_404(Story.objects.prefetch_related('comments')
                              .prefetch_related('comments__created_by')
                              .select_related('created_by'), pk=story_id)
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

            return redirect('story', story.pk)
    else:
        form = StoryForm()

    return render(request, 'submit.html', {'form': form})


@login_required
def up_vote(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    if story.created_by != request.user:

        instance, created = Vote.objects.get_or_create(story=story, vote_by=request.user)        
        
        if created:
            story.number_of_votes += 1
        
        if not created:
            if instance.vote_type == Vote.DOWN_VOTE:
                instance.vote_type = Vote.UP_VOTE
                story.number_of_votes += 2
                instance.save()

            else:
                instance.delete()
                story.number_of_votes -= 1

        story.save()
    
        return redirect('story', story.pk)
    

@login_required
def down_vote(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    if story.created_by != request.user:

        instance, created = Vote.objects.get_or_create(story=story, vote_by=request.user)

        if created:
            instance.vote_type = Vote.DOWN_VOTE
            story.number_of_votes -= 1
            instance.save()
        
        if not created:
            if instance.vote_type == Vote.UP_VOTE:
                instance.vote_type = Vote.DOWN_VOTE
                story.number_of_votes -= 2
                instance.save()

            else:
                instance.delete()
                story.number_of_votes += 1

        story.save()

        return redirect('story', story.pk)