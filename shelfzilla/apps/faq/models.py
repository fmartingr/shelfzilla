# coding: utf-8

# django
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _


class QuestionAnswerCategory(models.Model):
    name_es = models.CharField(max_length=32)

    class Meta:
        ordering = ('name_es', )
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name
        
    @property
    def name(self):
        return getattr(self, u'name_{}'.format(get_language()), u'')

    
class QuestionAnswer(models.Model):
    category = models.ForeignKey(QuestionAnswerCategory,
                                 related_name='questions')
    ord = models.PositiveIntegerField(default=1)
    
    # Spanish
    title_es = models.CharField(max_length=256)
    answer_es = models.TextField()
    
    class Meta:
        ordering = ('ord', )
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
    
    def __unicode__(self):
        return self.title
   
    @property
    def title(self):
        return getattr(self, u'title_{}'.format(get_language()), u'')

    @property
    def answer(self):
        return getattr(self, u'answer_{}'.format(get_language()), u'')
