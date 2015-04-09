from django.db import models

# Create your models here.
class Question(models.Model):
    def __unicode__(self):
        return self.translations.get(language__code='es').title


class TranslatedQuestion(models.Model):
    question = models.ForeignKey(Question, related_name='translations')
    language = models.ForeignKey('manga.Language')
    title = models.CharField(max_length=256)
    answer = models.TextField()
    
    def __unicode__(self):
        return self.title
