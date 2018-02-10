from django.contrib import admin

from .models import Book, Reader


# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3
# #admin.site.register(Question)


class BookAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ('Question description', {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date']}),
    # ]
    # inlines = [ChoiceInline]
    list_display = ('name', 'author', 'for_age', 'language')
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Book, BookAdmin)
admin.site.register(Reader)
# Register your models here.
