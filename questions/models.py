import django.contrib.auth.models
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    info = models.TextField(verbose_name='Информация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # Имя модели в единственном числе
        verbose_name_plural = 'Категории'  # Имя модели во множественном числе

    def get_absolute_url(self):
        return reverse('categoryDetail', args=[str(self.id)])


class Question(models.Model):
    author = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.SET_NULL, verbose_name='Автор',
                               blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='questions', verbose_name='Категория')
    answer = models.OneToOneField('Answer', null=True, blank=True, on_delete=models.SET_NULL, related_name='question')
    text_of_question = models.TextField(verbose_name='Текст вопроса')
    is_published = models.BooleanField(verbose_name='Опубликовано?', default=False)

    def __str__(self):
        return self.text_of_question

    class Meta:
        verbose_name = 'Вопрос'  # Имя модели в единственном числе
        verbose_name_plural = 'Вопросы'  # Имя модели во множественном числе
        unique_together = (('author', 'text_of_question'), ('text_of_question', 'answer'))

        permissions = (('can_update_question', 'update_question'),
                       ('can_delete_question', 'delete_question'),
                       ('can_create_question', 'create_question'),
                       )

    def get_absolute_url(self):
        return reverse('questionDetail', args=[str(self.id)])

    def comment_exist(self):
        """ Проверка наличия комментов """
        return self.comments.exists()


class Comment(models.Model):
    author = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.SET_NULL, verbose_name='Автор',
                               blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments', verbose_name='Вопрос')
    text_of_comment = models.TextField(verbose_name='Текст комментария')

    def __str__(self):
        return self.text_of_comment

    class Meta:
        verbose_name = 'Комментарий'  # Имя модели в единственном числе
        verbose_name_plural = 'Комментарии'  # Имя модели во множественном числе

        permissions = (('can_update_comment', 'update_comment'),
                       ('can_delete_comment', 'delete_comment'),
                       ('can_create_comment', 'create_comment'),
                       )


class Answer(models.Model):
    author = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.SET_NULL, verbose_name='Автор',
                               blank=True, null=True)
    text_of_answer = models.TextField(verbose_name='Текст ответа')

    def __str__(self):
        return self.text_of_answer

    class Meta:
        verbose_name = 'Ответ'  # Имя модели в единственном числе
        verbose_name_plural = 'Ответы'  # Имя модели во множественном числе

        permissions = (('can_update_answer', 'update_answer'),
                       ('can_delete_answer', 'delete_answer'),
                       ('can_create_answer', 'create_answer'),
                       )