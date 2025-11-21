from core.models import Pagina

def pagina_context(request):
    return {
        'pagina_global': Pagina.objects.first()
    }
