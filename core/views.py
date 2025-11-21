from django.shortcuts import render
from .models import Pagina, Produto

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Produto, Pedido

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Contato
from django.contrib import messages

def index(request):
    pagina = Pagina.objects.first()
    produtos = Produto.objects.all()

    return render(request, 'core/index.html', {
        'pagina': pagina,
        'produtos': produtos
    })


@login_required
def comprar(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade'))

        # Validação de estoque
        if quantidade < 1:
            messages.error(request, "Quantidade inválida.")
            return redirect('comprar', id=id)

        if quantidade > produto.estoque:
            messages.error(request, "Quantidade maior que o estoque disponível.")
            return redirect('comprar', id=id)

        total = quantidade * produto.preco

        # Atualiza estoque
        produto.estoque -= quantidade
        produto.save()

        # Cria pedido
        Pedido.objects.create(
            usuario=request.user,
            produto=produto,
            quantidade=quantidade,
            total=total
        )

        messages.success(request, "Pedido realizado com sucesso!")
        return redirect('perfil')

    return render(request, 'core/pedido.html', {
        'produto': produto
    })


@login_required
def perfil(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data')

    return render(request, 'core/perfil.html', {
        'pedidos': pedidos,
    })


def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'core/cadastro.html', {'form': form})

def contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')

        Contato.objects.create(
            nome=nome,
            email=email,
            mensagem=mensagem
        )

        messages.success(request, 'Mensagem enviada com sucesso!')

        return redirect('contato')

    return render(request, 'core/contato.html')


def produtos(request):
    lista = Produto.objects.all()
    pagina = Pagina.objects.first()

    return render(request, 'core/produtos.html', {
        'produtos': lista,
        'pagina': pagina
    })


def produto(request, id):
    item = get_object_or_404(Produto, id=id)
    pagina = Pagina.objects.first()

    return render(request, 'core/produto.html', {
        'produto': item,
        'pagina': pagina
    })
