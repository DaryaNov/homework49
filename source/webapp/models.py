from django.db import models
from django.utils import timezone

STATUS_CHOICES = [
    ('new', 'Новая'),
    ('in_progress', 'В процессе'),
    ('done', 'Сделано')
]

TYPES_CHOICES = [
    ('Task', 'задача'),
    ('Bug','ошибка'),
    ('Enhancement', 'улучшение')
]



class Article(models.Model):

    description = models.CharField(max_length=2000, null=False, blank=False, verbose_name='Описание')
    maxdescription = models.TextField(max_length=2000,null=True,blank=False,verbose_name='Подробное описание')
    type = models.ForeignKey('Type',related_name='type_key',
                                on_delete=models.CASCADE, verbose_name='Тип')
    status = models.ForeignKey('Status',related_name='status_key',
                                on_delete=models.CASCADE, verbose_name='Статус')
    publish_at = models.DateTimeField(verbose_name="Время публикации", blank=True, default=timezone.now)


    def __str__(self):
        return "{}. {}".format(self.pk, self.description)


    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'



class Type(models.Model):
    type = models.CharField(max_length = 30, choices = TYPES_CHOICES, default = 'task', verbose_name = 'Тип')


    def __str__(self):
        return self.type[:20]

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Status(models.Model):
    status = models.CharField(max_length=30,choices=STATUS_CHOICES, default='new',verbose_name='Статус')


    def __str__(self):
        return self.status[:20]

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'