from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Tag, Relation


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        has_one_main = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            if form.cleaned_data['is_main']:
                has_one_main += 1
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if has_one_main != 1:
            if has_one_main > 1:
                message = 'Основный тег должен быть только 1'
            else:
                message = 'Основной тег не выбран'
            raise ValidationError(message)
        return super().clean()  # вызываем базовый код переопределяемого метода

class RelationInline(admin.TabularInline):
    model = Relation
    formset = RelationshipInlineFormset
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at', 'image']
    inlines = [RelationInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic']

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['tag', 'article', 'is_main']