from django.conf.urls import patterns, include, url

from django.contrib import admin
from question.views import QuestionView, ComponentView

from project.views import ProjectListView, ProjectDetailView, NewProjectView,\
    ProjectAnswerView, ProjectChangeTitleView, DeactivateUserView,\
    ProjectDetailCSVView, ProjectDeleteView, ProjectAnswerViewPDF
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    # authentication
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^openid/login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
    url(r'^deactivate/$', login_required(DeactivateUserView.as_view()), name='deactivate_user'),
    url(r'^project/$', login_required(ProjectListView.as_view()), name='project_list'),
    url(r'^project/new/$', login_required(NewProjectView.as_view()), name='project_new'),
    url(r'^project/(?P<pk>\d+)/$', login_required(ProjectDetailView.as_view()),name='project_detail'),
    url(r'^project/(?P<pk>\d+)/delete/$', login_required(ProjectDeleteView.as_view()), name='project_delete'),
    url(r'^project/(?P<pk>\d+)/rename/$', login_required(ProjectChangeTitleView.as_view()),name='project_change_title'),
    url(r'^project/(?P<pk>\d+)/csv/$', login_required(ProjectDetailCSVView.as_view()),name='project_csv'),
    url(r'^project/(?P<project>\d+)/pdf/$', login_required(ProjectAnswerViewPDF.as_view()),name='project_pdf'),
    url(r'^project/(?P<project>\d+)/answers/$', login_required(ProjectAnswerView.as_view()),name='project_answers'),
    url(r'^project/(?P<project>\d+)/answers/(?P<category>\d+)/$', login_required(ProjectAnswerView.as_view()),name='project_answers'),
    url(r'^project/(?P<project>\d+)/hardware-software/$', login_required(ComponentView.as_view()), name='hardware-software'),
    url(r'^project/(?P<project>\d+)/(?P<category>\d+)/$', login_required(QuestionView.as_view()), name='answer_question'),
    url(r'^features/$',direct_to_template, {'template': 'features.html'},name='features'),
    url(r'^create/$',direct_to_template, {'template': 'create.html'},name='create'),
    url(r'^support/$',direct_to_template, {'template': 'support.html'},name='support'),
    url(r'^resources/$',direct_to_template, {'template': 'resources.html'},name='resources'),
)
