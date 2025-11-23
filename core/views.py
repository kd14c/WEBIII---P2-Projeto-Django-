from .models import Pagina, Produto, Pedido

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Produto, Pedido

from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Contato
from django.contrib import messages

from decimal import Decimal

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
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senha2 = request.POST.get("senha2")

        # validações
        if senha != senha2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "core/cadastro.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já está em uso.")
            return render(request, "core/cadastro.html")

        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Email já está cadastrado.")
            return render(request, "core/cadastro.html")

        # criar usuário
        User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )

        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect("login")

    return render(request, "core/cadastro.html")

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
    produtos = Produto.objects.all()
    return render(request, "core/produtos.html", {"produtos": produtos})


def produto(request, id):
    item = get_object_or_404(Produto, id=id)
    pagina = Pagina.objects.first()

    return render(request, 'core/produto.html', {
        'produto': item,
        'pagina': pagina
    })

@login_required
def pedido(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == "POST":
        quantidade = int(request.POST.get("quantidade"))

        # verificar estoque
        if quantidade > produto.estoque:
            return render(request, "core/pedido.html", {
                "produto": produto,
                "erro": "Quantidade acima do estoque disponível."
            })

        # calcular total corretamente
        total = Decimal(produto.preco) * quantidade

        # criar pedido
        pedido = Pedido.objects.create(
            usuario=request.user,
            produto=produto,
            quantidade=quantidade,
            total=total
        )

        # atualizar estoque
        produto.estoque -= quantidade
        produto.save()

        # redirecionar para o perfil
        return redirect("perfil")

    return render(request, "core/pedido.html", {"produto": produto})