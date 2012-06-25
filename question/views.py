# Create your views here.
from django.forms.models import modelformset_factory, BaseModelFormSet,\
    inlineformset_factory, BaseInlineFormSet
from django.forms.widgets import HiddenInput, Select, CheckboxSelectMultiple,\
    RadioSelect, TextInput
from django.views.generic.edit import ProcessFormView, FormMixin
from question.models import Answer, Category, Question
from django.http import HttpResponseRedirect
from project.models import Project
from django.views.generic.base import TemplateResponseMixin
from question.widgets import MultiActorWidget, ComponentWidget
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.forms.fields import BooleanField


class BaseAnswerFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super(BaseAnswerFormSet, self).add_fields(form, index)
        
        try:
            question = form.instance.question
        except Question.DoesNotExist:
            question = Question.objects.get(id=form.initial['question'])
        
        form.fields['question'].widget = HiddenInput()
        form.fields['project'].widget = HiddenInput()
        form.fields['answer'].widget = self.get_answer_widget(form, question)
        
        answer = form.initial.get('answer', None)
        if answer == 'No':
            initial = False
        elif answer == None:
            initial = None
        else:
            initial = True
        
        if question.question_type == question.OPEN_CONDITIONAL:
            form.fields.insert(0, 'conditional', BooleanField(
                    required=False, 
                    widget=RadioSelect(choices=((False, 'No'), (True,'Yes'))),
                    initial=initial
                )
            )
        
    
    def get_answer_widget(self, form, question):
        if question.question_type == question.CHOICE_YES_NO:
            widget = RadioSelect(choices=[
                ('', '----------'), 
                ('Yes', 'Yes'),
                ('No', 'No')
            ])
        elif question.question_type == question.CHOICE_SINGLE:
            widget = Select(choices=question.choices())
        elif question.question_type == question.CHOICE_MULTIPLE:
            widget = CheckboxSelectMultiple(choices=question.choices()),
        else:
            widget = TextInput()
            
        if question.has_actors:
            return MultiActorWidget(widgets=[widget] * 3)
        else:
            return widget


class QuestionView(TemplateResponseMixin, FormMixin, ProcessFormView):
    template_name = 'question/answer_form.html'
    
    def get_initial(self):
        return [
            dict(project=self.project.id, question=question.id) for
            question in
            self.category.question_set.exclude(
                answer__in=self.project.answer_set.all()
            ).order_by('number')
        ]
    
    def get_form_class(self):
        form_class = modelformset_factory(
            Answer,
            formset=BaseAnswerFormSet,
            max_num=self.category.question_set.count(),
            extra=self.category.question_set.count()
        )
        return form_class
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        else:
            kwargs.update({
                'queryset': self.project.answer_set.filter(question__category=self.category).order_by('question__number'),
            })
        return kwargs
    
    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.filter(owner=request.user), pk=kwargs.get('project'))
        self.category = Category.objects.get(pk=kwargs.get('category'))
        
        if self.category.name == 'Hardware & Software':
            return HttpResponseRedirect(reverse('hardware-software', kwargs=dict(project=self.project.id)))
        
        return super(QuestionView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if 'later' in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(QuestionView, self).post(self, request, *args, **kwargs)
    
    def form_valid(self, form):
        form.save()
#        form = form.save(commit=False)
#        for subform in form:
#            if subform.answer == 'No' and subform.question.question_type == subform.question.OPEN_CONDITIONAL:
#                subform.answer = ''
#            subform.save()
        return super(QuestionView, self).form_valid(form)
    
    def get_success_url(self):
        return ''
    
    def get_context_data(self, **kwargs):
        context = super(QuestionView, self).get_context_data(**kwargs)
        context['project']= self.project
        context['category'] = self.category
        context['questions'] = self.get_questions()
        
        forms = []
        for form in context['form'].forms:
            try:
                form.instance.question
            except:
                form.instance.question = Question.objects.get(id=form.initial['question'])
            forms.append(form)
        forms = sorted(forms, key=lambda form: form.instance.question.number)
        context['form'].forms = forms
        
        return context
    
    def get_questions(self):
        questions = Question.objects.filter(category=self.category).order_by('number')
        for question in questions:
            question.pixels = (question.number - 1) * -990
        
        answers = Answer.objects.filter(project=self.project)
        
        for question in questions:
            if answers.filter(question=question).exclude(answer='').count() == 0:
                question.status = 'unanswered'
            else:
                question.status = 'answered'
                
        # adds category-colors for Life-cycle costs
        if self.category.name == 'Life-cycle costs':
            categories = {
                1 : None,
                2 : None,
                3 : 'CapEx',
                4 : 'CapEx',
                5 : 'OpEx',
                6 : 'CapManEx',
                7 : 'CoC',
                8 : 'CoC',
                9 : 'CoC',
                10 : 'CoC',
                11 : 'CoC',
                12 : 'ExpDS',
                13 : 'ExpIDS',
            }
            for question in questions:
                cat = categories[question.number]
                if cat:
                    question.status += ' cat-' + cat
        
        return questions


class BaseComponentFormSet(BaseInlineFormSet):   
    def add_fields(self, form, index):
        super(BaseComponentFormSet, self).add_fields(form, index)
        form.fields['answer'].widget = ComponentWidget()


class ComponentView(TemplateResponseMixin, FormMixin, ProcessFormView):
    success_url = '.'
    template_name = 'question/component_form.html'
    form_class = inlineformset_factory(Project, Answer, exclude='question',
                                       formset=BaseComponentFormSet, extra=1)
    
    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.filter(owner=request.user), pk=kwargs.get('project'))
        self.category = Category.objects.get(name='Hardware & Software')
        self.question = self.category.question_set.get(number=1)
        
        return super(ComponentView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form = form.save(commit=False)
        for subform in form:
            subform.question = self.question
            subform.save()
        
        return super(ComponentView, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(ComponentView, self).get_form_kwargs()
        kwargs['instance'] = self.project
        kwargs['queryset'] = Answer.objects.filter(question__category=self.category)
        
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(ComponentView, self).get_context_data(**kwargs)
        context['project'] = self.project
        context['question'] = self.question
        context['category'] = self.category
        context['formset'] = context['form']
        del context['form']
        
        return context