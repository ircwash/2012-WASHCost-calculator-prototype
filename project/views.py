from django.views.generic import ListView
from project.models import Project
from django.views.generic.detail import DetailView, BaseDetailView
from question.models import Category, Answer, Question
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.base import TemplateView, View
from project.forms import ChangeTitleForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from question.widgets import ComponentWidget, MultiActorWidget
import csv
from django.utils.datetime_safe import datetime
import itertools
from project.templatetags.calculations import yearly_growth
from django.shortcuts import get_object_or_404
from subprocess import Popen, PIPE
import os
from washcost.settings import rel
from django.conf import settings

class UserMixin(object):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class ProjectListView(UserMixin, ListView):
    model = Project
    
    def get(self, request, *args, **kwargs):
        response = super(ProjectListView, self).get(request, *args, **kwargs)
        if not self.object_list.exists():
            return HttpResponseRedirect(reverse('create'))
        return response


class ProjectDetailView(UserMixin, DetailView):
    model = Project
    
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['category_list'] = self.get_categories()
        context['change_title_form'] = ChangeTitleForm(instance=self.object)
        return context
    
    def get_categories(self):
        categories = Category.objects.filter(is_active=True)
        answers = Answer.objects.filter(project=self.object)
        for category in categories:
            count = answers.filter(question__category=category).exclude(answer='').count()
            questions = category.question_set.count()
            
            if count > 0:
                category.percentage = '%.0f' % (min(1.0 * count / questions * 100, 100))
            else:
                category.percentage = 0
                
        return categories


class NewProjectView(View):
    def post(self, request, *args, **kwargs):
        project = Project.objects.create(
            owner = request.user,
            title = 'Untitled'
        )
        return HttpResponseRedirect(project.get_absolute_url())


class ProjectAnswerView(TemplateView):
    template_name = 'project/project_answers.html'

    def get(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.filter(owner=self.request.user), id=self.kwargs['project'])
        self.category = Category.objects.get(id=self.kwargs.get('category', 1))
        self.answer_list_all = self.project.answer_set.all()

        return super(ProjectAnswerView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectAnswerView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.filter(is_active=True)
        context['answer_list'] = self.project.answer_set.filter(question__category=self.category)
        context['project'] = self.project
        context['category'] = self.category
        context['answers'] = self.get_answers()
        context['components'] = self.get_components()
        context['component_labels'] = ComponentWidget.label
        
        # fixes empty answers
        a = context['answers']
        for i in dict(Question.FORMULA_VAR_CHOICES).keys():
            if i not in a:
                if i in [1, 2, 17, 18, 19, 20, 21, 22, 23]:
                    a[i] = 0
                else:
                    a[i] = [0, 0, 0]
            
        pop_size = yearly_growth(a[1], a[2])
        pop_growth = [0] + [pop_size[i] - pop_size[i-1] for i in range(1, len(pop_size))]

        mod_opex = [0.02 * sum(a[13]) * pop for pop in pop_size]
        components = [ComponentWidget.parse(answer.answer) for answer in self.project.answer_set.filter(question__category__name='Hardware & Software')]
        comp_sum = sum(c['Cost'] / c['Lifespan'] / c['Expected number of users'] for c in components)
        mod_capmanex = [pop * comp_sum for pop in pop_size]
        coc_HOU = [(a[4][2]-(i)*a[4][2]/a[8][2])*(a[5][2]/100.0+a[6][2]/100.0)/a[12][2]*a[1] for i in range(int(a[8][2]))]
        while len(coc_HOU)<=20:coc_HOU.append(0.0)
        coc_NGO = [(a[4][0]-(i)*a[4][0]/a[8][0])*(a[5][0]/100.0+a[6][0]/100.0)/a[12][0]*a[1] for i in range(int(a[8][0]))]
        while len(coc_NGO)<=20:coc_NGO.append(0.0)
        coc_GOV = [(a[4][1]-(i)*a[4][1]/a[8][1])*(a[5][1]/100.0+a[6][1]/100.0)/a[12][1]*a[1] for i in range(int(a[8][1]))]
        while len(coc_GOV)<=20:coc_GOV.append(0.0)
        # use izip itertools instead

        HOU_serie_part = [(a[13][2] + a[14][2] + a[15][2] + a[3][2] + a[9][2] + a[10][2]) * pop for pop in pop_size]
        NGO_serie_part = [(a[13][0] + a[14][0] + a[15][0] + a[3][0] + a[9][0] + a[10][0]) * pop_size[0] for i in range(20)] # seems odd
        GOV_serie_part = [(a[13][1] + a[14][1] + a[15][1] + a[3][1] + a[9][1] + a[10][1]) * pop for pop in pop_size]

        
        #context['NGO_serie'] = [(a[13][0] + a[14][0] + a[15][0] + a[3][0]) * pop for pop in pop_size]
        #context['HOU_serie'] = [(a[13][2] + a[14][2] + a[15][2] + a[3][2]) * pop for pop in pop_size]
        #context['GOV_serie'] = [(a[13][1] + a[14][1] + a[15][1] + a[3][1]) * pop for pop in pop_size]

        # calculate NGO_serie cumulative
        #NGO_serie = [i+j for i,j in zip(NGO_serie_part,coc_NGO)]
        #context['NGO_serie'] = [sum(NGO_serie[:n]) for n in range(-19,0)]
        #context['NGO_serie'].append(sum(NGO_serie))
        context['NGO_serie'] = NGO_serie_part

        # calculate HOU_serie cumulative
        HOU_serie = [i+j for i,j in zip(HOU_serie_part,coc_HOU)]
        #context['HOU_serie'] = [sum(HOU_serie[:n]) for n in range(-19,0)]
        #context['HOU_serie'].append(sum(HOU_serie))
        context['HOU_serie'] = HOU_serie

        # calculate GOV_serie cumulative
        GOV_serie = [i+j for i,j in zip(GOV_serie_part,coc_GOV)]
        context['GOV_serie'] = [sum(GOV_serie[:n]) for n in range(-19,0)]
        context['GOV_serie'].append(sum(GOV_serie))

        # calculate COC cumulative
        COC = [cocngo+cochou+cocgov for cocngo,cochou,cocgov in zip(coc_NGO,coc_HOU,coc_GOV)]
        context['COC'] = [sum(COC[:n]) for n in range(-19,0)]
        context['COC'].append(sum(COC))

        # service level sanitation formulas
        context['acc_no'] = 100.0 - a[17] - a[18] - a[19]
        context['use_no'] = 100.0 - a[20] - a[21]
        if a[22] == 'No':
            context['rel_no'] = 100.0
        else:
            context['rel_impr'] = 100.0 - a[22]
        if a[23] == 'No':
            context['env_no'] = 100.0
        else:
            context['env_impr'] = 100.0 - a[23]
        # check values validation hack
        if context['acc_no'] < 0:
            context['check_acc_no'] = "Please check your input values accessibility!"
        if context['use_no'] < 0:
            context['check_use_no'] = "Please check your input values use!"
        if a[22] > 100 and a[22] != "No":
            context['check_rel_impr'] = "Please check your input values reliability!"
        elif a[22] == "No":
            context['check_rel_impr'] = ""
        if a[23] > 100 and a[23] != "No":
            context['check_env_impr'] = "Please check your input values environmental protection!"
        elif a[23] == "No":
            context['check_env_impr'] = ""


        # currency convertor NOTE: current db values are wrong, should be relative to USD
        # eg: USD = 1, BDT 2008 = 0.5
        if a[24] == 1.00:
            context['currency_symbol'] = 'USD'
        else:
            context['currency_symbol'] = 'BDT'

        conversion = a[24]

        context['cap_shortfall'] = mod_opex[-1] - sum(a[3]) * pop_size[-1] + mod_capmanex[-1] - sum(a[15]) * pop_size[-1]
        #context['unalloc_serie'] = [p_growth * ((sum(a[13]) + sum(a[14])) * p_size ) for p_growth, p_size in zip(pop_growth, pop_size)]

        # calculate unalloc_serie cumulative
        unalloc_serie = [p_growth * ((sum(a[13]) + sum(a[14]))) for p_growth in pop_growth]
        context['unalloc_serie'] = [sum(unalloc_serie[:n]) for n in range(-19,0)]
        context['unalloc_serie'].append(sum(unalloc_serie))

        cum_capexhrd = [sum(a[13]) * pop for pop in pop_size]
        #context['cum_capexhrd'] = [sum(cum_capexhrd[:n]) for n in range(-19,0)]
        #context['cum_capexhrd'].append(sum(cum_capexhrd))
        context['cum_capexhrd'] = cum_capexhrd

        cum_capopex = [sum(a[15]) * pop for pop in pop_size]
        context['cum_capopex'] = [sum(cum_capopex[:n]) for n in range(-19,0)]
        context['cum_capopex'].append(sum(cum_capopex))

        cum_capexpids = [sum(a[10]) * pop for pop in pop_size]
        context['cum_capexpids'] = [sum(cum_capexpids[:n]) for n in range(-19,0)]
        context['cum_capexpids'].append(sum(cum_capexpids))

        cum_capexsft = [sum(a[14]) * pop for pop in pop_size]
        #context['cum_capexsft'] = [sum(cum_capexsft[:n]) for n in range(-19,0)]
        #context['cum_capexsft'].append(sum(cum_capexsft))
        context['cum_capexsft'] = cum_capexsft

        cum_capmanex = [sum(a[3]) * pop for pop in pop_size]
        context['cum_capmanex'] = [sum(cum_capmanex[:n]) for n in range(-19,0)]
        context['cum_capmanex'].append(sum(cum_capmanex))

        cum_capexpds = [sum(a[9]) * pop for pop in pop_size]
        context['cum_capexpds'] = [sum(cum_capexpds[:n]) for n in range(-19,0)]
        context['cum_capexpds'].append(sum(cum_capexpds))


        # calculate mod_opex_capman cumulative
        y = [modopex + modcapmanex for modopex, modcapmanex in zip(mod_opex, mod_capmanex)]
        x = [ a-c-d for a,c,d in zip(y, cum_capopex, cum_capmanex)]
        context['mod_opex_capman'] = [sum(x[:n]) for n in range(-19,0)]
        context['mod_opex_capman'].append(sum(x))


        context['cap_shortfall'] =  sum(x)*conversion


        return context

    def get_components(self):
        raw_components = self.project.answer_set.filter(question__category=Category.objects.get(name='Hardware & Software'))
        answers = []
        for raw_component in raw_components:
            answers.append(raw_component.answer[3:-2].split("', u'"))
                
        return answers


    def get_answers(self):
        answers = dict(self.project.answer_set.values_list(
            'question__formula_variable', 'answer'))
        for k, v in answers.items():
            if v[3:-2].split("', u'") != ['']:
                answers[k] = [parse_value(i) for i in v[3:-2].split("', u'")]
            else:
                answers[k] = parse_value(answers[k])
        return answers


class ProjectAnswerViewPDF(ProjectAnswerView):
    template_name = 'project/project_answers_pdf.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProjectAnswerViewPDF, self).get_context_data(**kwargs)
        context['BASE_URL'] = settings.BASE_URL
        return context
    
    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
        
        html = super(ProjectAnswerView, self).render_to_response(context, **response_kwargs).rendered_content
        wkhtmltopdf = os.path.join(rel('../bin/wkhtmltopdf-i386'))
        p = Popen([wkhtmltopdf, '--page-size', 'A4', '-', '-'], stdin=PIPE, stdout=PIPE)
        response.write(p.communicate(html.encode('utf-8'))[0])
        
        return response

def parse_value(v):
    try:
        return float(v)
    except ValueError:
        return v

class ProjectDetailCSVView(UserMixin, BaseDetailView):
    model = Project
    
    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = ('attachment; filename=%s.csv' %
            self.object.title
        )
    
        writer = csv.writer(response)
        
        name = '%s %s' % (self.request.user.first_name,
                          self.request.user.last_name)
        
        
        writer.writerow([self.object.title, name , datetime.now().date()])
        writer.writerow([])
        
        answers = self.object.answer_set.order_by('question__category')
        for category, answers in itertools.groupby(answers, lambda answer: answer.question.category.name):
            answers = sorted(answers, key=lambda answer: answer.question.id)
            writer.writerow([])

            if category == 'Life-cycle costs':
                writer.writerow([category, 'Answer'] + MultiActorWidget.ACTORS.values())
            else:
                writer.writerow([category, 'Answer'])
                
            for answer in answers:
                subanswers = MultiActorWidget.parse(answer.answer)
                
                if isinstance(subanswers, unicode):
                    row  = [answer.question, subanswers]
                else:
                    row = [answer.question, ''] + subanswers
                
                writer.writerow(row)
            writer.writerow([])
            
        
        
        return response
         

class ProjectDeleteView(UserMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')


class ProjectChangeTitleView(UserMixin, UpdateView):
    model = Project
    form_class = ChangeTitleForm
    
    def get_success_url(self):
        return reverse('project_detail', kwargs=dict(pk=self.object.id))
    

class DeactivateUserView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.is_active = False
        user.save()
        
        return HttpResponseRedirect(reverse('home'))
