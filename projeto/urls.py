"""
URL configuration for projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('comprar/<int:id>/', views.comprar, name='comprar'),
    path('perfil/', views.perfil, name='perfil'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='core/login.html',
            redirect_authenticated_user=True,
            next_page='perfil'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='index'),
        name='logout'
    ),

    path('cadastro/', views.cadastro, name='cadastro'),

    path('contato/', views.contato, name='contato'),
    path('produtos/', views.produtos, name='produtos'),

    path('produto/<int:id>/', views.produto, name='produto'),
    path("pedido/<int:produto_id>/", views.pedido, name="pedido"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

