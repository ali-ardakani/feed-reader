from django.contrib import admin
from .models import Source, Category, Feed, CategoryName

admin.site.register(Source)
admin.site.register(CategoryName)
admin.site.register(Category)
admin.site.register(Feed)
