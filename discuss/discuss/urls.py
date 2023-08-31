from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from story.views import submit, story, up_vote, down_vote
from core.views import frontpage, newest, search, signup

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('newest/', newest, name='newest'),
    path('search/', search, name='search'),

    path('signup/', signup, name='signup'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    path('submit/', submit, name='submit'),
    path('s/<int:story_id>/up_vote/', up_vote, name='up_vote'),
    path('s/<int:story_id>/down_vote/', down_vote, name='down_vote'),
    path('s/<int:story_id>/', story, name='story'),
    path('user/', include('userprofile.urls')),

    path('admin/', admin.site.urls),
]