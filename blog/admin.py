from django.contrib import admin

from .models import Post, Visita


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'publicado', 'creado', 'visitas_totales')
    list_filter = ('publicado', 'creado', 'autor')
    search_fields = ('titulo', 'resumen', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'creado'
    readonly_fields = ('creado', 'actualizado')

    @admin.display(description='Visitas')
    def visitas_totales(self, obj):
        return obj.visitas.count()


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('post', 'fecha', 'ip')
    list_filter = ('fecha',)
    search_fields = ('post__titulo', 'ip')
    readonly_fields = ('post', 'fecha', 'ip', 'user_agent')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
