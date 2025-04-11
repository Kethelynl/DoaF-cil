from .models import ProductD
from recebidorform.models import PedidoForm
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin


# criação de formulário para Doador
class ProductCreateD(LoginRequiredMixin, CreateView):
    model = ProductD
    fields = ['name','quantity', 'category', 'photo', 'content']
    template_name = 'doar/form_doar.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# ve os detalhes do produto
class ProductCreateDDetail(LoginRequiredMixin, DetailView):
    model = ProductD
    template_name = 'doar/detail_product.html'
    context_object_name = 'object'

# lista os produtos
class ListProductD(LoginRequiredMixin, ListView):
    model = ProductD
    template_name = 'doador_profile.html'
    context_object_name = 'products'

    def get_queryset(self):
        return ProductD.objects.filter(author=self.request.user).order_by('-date_post')
    
# lista os produtos
class ListProductDAll(LoginRequiredMixin, ListView):
    model = ProductD
    template_name = 'doar/list_product.html'
    context_object_name = 'products'

    def test_func(self):
        return self.request.user.groups.filter(name='Receber Doação').exists()
    
class DeleteProduct(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProductD

    template_name = 'doar/confirm_delete.html'
    
    def get_success_url(self):
        return reverse('user-profile', kwargs={'user_id': self.request.user.id})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

@login_required
def btn_to_give_an_order(request, product_id):
    product = get_object_or_404(PedidoForm, id=product_id)
    receiver = product.author # dono do pedido
    donor = request.user # Usuário logado (doador)

    if not donor.groups.filter(name='Doador').exists():
        messages.error(request, "Apenas doadores podem conceber pedidos")
        return redirect('profile', user_id=receiver.id)
    
    # enviando o email
    send_mail(
        subject ="Alguém deseja doar para você!",
        message=f'Olá {receiver.username}, o/a {donor.username} deseja doar para você!\nEntre em contato com ele/a pelo e-mail: {donor.email}',
        from_email="kethcavalari@gmail.com'",
        recipient_list=[receiver.email],
        fail_silently=False,
    )

    messages.success(request, "E-mail enviado com sucesso! ")
    return redirect('user-profile', user_id=receiver.id)

def home(request):
    return render(request, 'base.html')