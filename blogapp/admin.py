from django.contrib import admin

# Register your models here.
from blogapp.models import article, category, author, Comment


class authorModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__", "details"]

    class Meta:
        Model = author


admin.site.register(author, authorModel)


class articleModel(admin.ModelAdmin):
    list_display = ["__str__", "posted_on"]
    search_fields = ["__str__", "details"]
    list_filter = ["posted_on", "category"]
    list_per_page = 10

    class Meta:
        Model = article


admin.site.register(article, articleModel)


class categoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__", "name"]
    list_per_page = 10

    class Meta:
        Model = category


admin.site.register(category, categoryModel)


class CommentModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__", "name"]
    list_per_page = 10

    class Meta:
        Model = Comment

admin.site.register(Comment, CommentModel)