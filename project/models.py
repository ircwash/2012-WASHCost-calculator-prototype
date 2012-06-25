from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    title = models.TextField()
    description = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return u'%s. %s' % (self.owner, self.title)
    
    def status(self):
        from question.models import Question
        if self.answer_set.count() == Question.objects.filter(category__is_active=True).count():
            return 'completed'
        elif self.answer_set.count() > 0:
            return 'started'
        else:
            return 'not started'
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs=(dict(pk=self.pk)))




