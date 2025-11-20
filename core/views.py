from django.shortcuts import render
from .models import Pagina, Produto

def index(request):
    pagina = Pagina.objects.first()
    produtos = Produto.objects.all()

    return render(request, 'core/index.html', {
        'pagina': pagina,
        'produtos': produtos
    })
