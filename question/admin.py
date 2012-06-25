from django.contrib import admin
from question.models import Question, Category, Answer, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    
    fieldsets = (
        (None, {
            'fields' : (('choice', 'value'),)
        }),
    )


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'question', 'question_type', 'category','formula_variable')
    list_display_links = ('question',)
    list_editable = ('number',)
    list_filter = ('category', 'question_type')
    ordering = ('category', 'number',)
    inlines = [
        ChoiceInline,
    ]
    fieldsets = (
        (None, {
            'fields' : (
                ('question', 'number'),
                ('is_required', 'has_actors'),
            )
        }),
        ('Conditional question', {
            'fields' : (
                ('conditional_question'),
            ),
            'classes' : ['collapse'],
        }),
        (None, {
            'fields' : (
                ('category', 'question_type','formula_variable'),
            )
        }),
        (None, {
            'fields' : (
                ('info_question'),
            ),
        }),
    )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'category', 'project',)
    ordering = ('project', 'question__category', 'question__number',)
    list_filter = ('project__title',)
    
    def category(self, answer):
        return answer.question.category

admin.site.register(Question, QuestionAdmin)
admin.site.register(Category)
admin.site.register(Answer, AnswerAdmin)
