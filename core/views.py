from .models import Pagina, Produto, Pedido
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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

        if senha != senha2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "core/cadastro.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já está em uso.")
            return render(request, "core/cadastro.html")

        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Email já está cadastrado.")
            return render(request, "core/cadastro.html")

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
    busca = request.GET.get("busca", "")
    produtos = Produto.objects.filter(nome__icontains=busca)
    return render(request, "core/produtos.html", {
        "produtos": produtos,
        "busca": busca
    })





@login_required
def pedido(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == "POST":
        quantidade = int(request.POST.get("quantidade"))

        if quantidade > produto.estoque:
            return render(request, "core/pedido.html", {
                "produto": produto,
                "erro": "Quantidade acima do estoque disponível."
            })

        total = Decimal(produto.preco) * quantidade

        pedido = Pedido.objects.create(
            usuario=request.user,
            produto=produto,
            quantidade=quantidade,
            total=total
        )

        produto.estoque -= quantidade
        produto.save()

        return redirect("perfil")

    return render(request, "core/pedido.html", {"produto": produto})


def sobre(request):
    pagina = Pagina.objects.first()
    return render(request, "core/sobre.html", {
        "pagina": pagina
    })
