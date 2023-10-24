from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        value_list = []
        for form in self.forms:
            value = form.cleaned_data.get('is_main', False)
            value_list.append(value)
        count = sum(value_list)
        if count > 1:
            raise ValidationError('Основной тег может быть только 1')
        elif not count:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
