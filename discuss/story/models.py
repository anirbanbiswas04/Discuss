from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    body = models.TextField(blank=False)
    number_of_votes = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='stories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'stories'
    
    def __str__(self):
        return '%s' % self.title
    
    def up_vote(self):
        self.number_of_votes += 1
        self.save()

    def down_vote(self):
        self.number_of_votes -= 1
        self.save()


VOTE_TYPE = (
    ("up_vote", "Up Vote"),
    ("down_vote", "Down Vote"),
)

class Vote(models.Model):
    story = models.ForeignKey(Story, related_name='votes', on_delete=models.CASCADE)
    vote_by = models.ForeignKey(User, related_name='vote', on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPE)

    def __str__(self):
        return f'{self.story.title} - {self.vote_by.username}'


class Comment(models.Model):
    story = models.ForeignKey(Story, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']