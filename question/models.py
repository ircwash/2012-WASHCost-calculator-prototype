from django.db import models
from project.models import Project

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField()
    
    def __unicode__(self):
        return self.name
    
    def status(self):
        answers = self.question_set.filter(answer__isnull=False).count()
        if answers == None or answers == 0:
            return 'not_completed'            
        elif answers == self.question_set.count():
            return 'completed'
        else:
            return 'started'
    
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('id',)


class Question(models.Model):
    OPEN = 1
    CHOICE_YES_NO = 2
    CHOICE_SINGLE = 3
    CHOICE_MULTIPLE = 4
    OPEN_CONDITIONAL = 5

    QUESTION_TYPE_CHOICES = (
        (OPEN, 'open question'),
        (CHOICE_YES_NO, 'yes or no'),
        (CHOICE_SINGLE, 'single choice'),
        (CHOICE_MULTIPLE, 'multiple choice'),
        (OPEN_CONDITIONAL, 'conditional yes/no')
    )

    TARGET = 1
    GROW_RATE = 2
    OP_EXP = 3
    COC_SOL = 4
    COC_IRD = 5
    COC_IRI = 6
    COC_D = 7
    COC_ATR = 8
    EXP_DS = 9
    EXP_IDS = 10
    EXP_YI = 11
    EXP_POP = 12
    CAP_HW = 13
    CAP_SW = 14
    CAP_MNT = 15
    EXP_BGN = 16
    ACC_IMPR = 17
    ACC_BAS = 18
    ACC_LIM = 19
    USE_IMPR = 20
    USE_BAS = 21
    REL = 22
    ENV = 23
    CUR = 24
    COM_HS = 27


    FORMULA_VAR_CHOICES = (
        (TARGET, 'intervention target'),
        (GROW_RATE, 'predicted grow rate'),
        (OP_EXP,'Operational Expenditure'),
        (COC_SOL,'Cost of Capital - size of loan'),
        (COC_IRD,'Cost of Capital - interest rate direct'),
        (COC_IRI,'Cost of Capital - interest rate indirect'),
        (COC_D,'Cost of Capital - dividends'),
        (COC_ATR,'Cost of Capital - average time of repayment'),
        (EXP_DS,'Expenditure Direct Support'),
        (EXP_IDS,'Expenditure Indirect Support'),
        (EXP_YI,'Interval/years of expenditure'),
        (EXP_BGN,'Expenditure begin'),
        (EXP_POP,'Population covered by expenditure'),
        (CAP_HW,'Capital Expenditure - hardware'),
        (CAP_SW,'Capital Expenditure - software'),
        (CAP_MNT,'Capital Maintenance Expenditure'),
        (ACC_IMPR,'sls - accessibility improved'),
        (ACC_BAS,'sls - accessibility basic'),
        (ACC_LIM,'sls - accessibility limited'),
        (USE_IMPR,'sls - use improved'),
        (USE_BAS,'sls - use basic'),
        (REL,'sls - reliability'),
        (ENV,'sls - environmental'),
        (COM_HS,'hard and software components'),
        (CUR,'currency conversion')
    )

    
    question = models.TextField()
    default_answer = models.TextField(blank=True,null=True)
    number = models.IntegerField()
    formula_variable = models.IntegerField(choices=FORMULA_VAR_CHOICES,blank=True,null=True)
    category = models.ForeignKey(Category)
    question_type = models.IntegerField(choices=QUESTION_TYPE_CHOICES)
    is_required = models.BooleanField()
    has_actors = models.BooleanField(default=False)
    info_question = models.TextField(blank=True,null=True)
    conditional_question = models.TextField(blank=True)
    
    def has_next(self):
        try:
            Question.objects.get(category=self.category, number=self.number+1)
            return True;
        except Question.DoesNotExist:
            return False;
    
    def next(self):
        return Question.objects.get(category=self.category, number=self.number+1)
    
    def choices(self):
        return self.choice_set.values_list('value', 'choice')

    def get_var_name(self):
        return self.get_formula_variable_display()
    
    def __unicode__(self):
        return self.question
    

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.choice
    

class Answer(models.Model):
    project = models.ForeignKey(Project)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=255, blank=True)
    
    def __unicode__(self):
        return self.answer
