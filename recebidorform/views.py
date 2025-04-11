from .models import PedidoForm, PedidoDoacao
from django.core.mail import send_mail
from doadorform.models import ProductD
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# criação de formulário para Doador
class PedidoCreateD(LoginRequiredMixin, CreateView):
    model = PedidoForm
    fields = ['name','quantity', 'category', 'photo', 'content']
    template_name = 'pedir/pedido_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# ve os detalhes do produto
class PedidoCreateDetail(LoginRequiredMixin, DetailView):
    model = PedidoForm
    template_name = 'pedir/pedido_detail.html'
    context_object_name = 'object'

# lista os produtos
class ListPedido( LoginRequiredMixin, ListView):
    model = PedidoForm
    template_name = 'recebidor_profile.html'
    context_object_name = 'products'

    def get_queryset(self):
        return PedidoForm.objects.filter(author=self.request.user).order_by('-date_product')
    
class ListPedidoAll( LoginRequiredMixin, ListView):
    model = PedidoForm
    template_name = 'pedir/lista_pedidos.html'
    context_object_name = 'pedidos'
    ordering = ['-date_product']

    def test_func(self):
        return self.request.user.groups.filter(name='Doar').exists()
    
class DeletePedido(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PedidoForm

    template_name = 'pedir/confirm_delete.html'
    
    def get_success_url(self):
        return reverse('user-profile', kwargs={'user_id': self.request.user.id})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

def request_donation(request, product_id):
    product = get_object_or_404(ProductD, id=product_id)
    donor = product.author # dono do produto
    receiver = request.user # usuário logado

    if not receiver.groups.filter(name='Receber Doação').exists():
        messages.error(request, "Apenas recebedores podem receber doação.")
        return redirect('profile', user_id=donor.id)
    
    

    send_mail(
        subject="Receber doação",
        message=f"Olá {donor.username}, a/o {receiver.username} deseja receber doação do seu produto! entre em contato {receiver.email}",
        from_email="kethcavalari@gmail.com",  
        recipient_list=[donor.email],
        fail_silently=False  
    )

    messages.success(request, "Pedido de doação enviado!")
    return redirect('user-profile', user_id=donor.id)

