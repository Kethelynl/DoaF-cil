from .models import UserAddress
from geopy.geocoders import Nominatim
from doadorform.models import ProductD
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.gis.measure import D  # Para cálculos de distância
from django.contrib.gis.geos import Point
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.urls import reverse

from recebidorform.models import PedidoForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm, DesignProfileForm, UpdateUserForm, UserAddressForm

from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            group_choises = form.cleaned_data['group'] #pega a escolha do usuário

            if group_choises == 'Doador':
                group = Group.objects.get(name='Doador')
            else:
                group = Group.objects.get(name='Receber Doação')


            user.groups.add(group) # associa o usuário a escolha
            return redirect('login')
    
    else:
        form = RegisterUserForm()
    
    return render(request, 'cadastro.html', {'form': form })

@login_required
def profile(request, user_id=None):
    # Se um user_id for passado, busca esse usuário; senão, usa o usuário logado
    perfil = get_object_or_404(User, id=user_id) if user_id else request.user  


    context = {
        'perfil': perfil,
        'is_owner': request.user == perfil,  # Verifica se o usuário logado é o dono do perfil
    }

    if perfil.groups.filter(name='Doador').exists():
        context['products'] = ProductD.objects.filter(author=perfil)
        return render(request, 'doador_profile.html', context)
    elif perfil.groups.filter(name='Receber Doação').exists():
        context['products'] = PedidoForm.objects.filter(author=perfil)
        return render(request, 'recebidor_profile.html', context)

    return render(request, 'profile.html', context)

def photo(request):
    if request.method == "POST":
        form_img = DesignProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if form_img.is_valid():
            form_img.save()
            return redirect('profile')
    else:
        form_img = DesignProfileForm(instance=request.user.profile)
    
    return render(request, 'form_photo.html', {'form':form_img})

@login_required
def update_form_user(request):
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
        
    else:
        form = UpdateUserForm(instance=request.user)
    
    return render(request, 'update_form.html', {'form':form})

@login_required
def address_form(request):
    try:
        address = UserAddress.objects.get(user=request.user)  
    except UserAddress.DoesNotExist:
        address = None

    if request.method == "POST":
        form = UserAddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user

            # Adicionando prints para debug
            print(f"Rua: {address.rua}")
            print(f"Número: {address.numero}")
            print(f"Cidade: {address.cidade}")
            print(f"Estado: {address.estado}")

            # Construindo o endereço para o Nominatim
            endereco_formatado = f"{address.rua}, {address.numero}, {address.cidade}, {address.estado}, Brasil"
            print(f"Endereço formatado: {endereco_formatado}")

            # Tentando obter coordenadas
            geolocator = Nominatim(user_agent="doacao_app")
            location = geolocator.geocode(endereco_formatado)
            print(f"Resultado do Nominatim: {location}")

            if location:
                address.latitude = location.latitude
                address.longitude = location.longitude

                address.save()
                messages.success(request, "Endereço salvo com sucesso!")
                return redirect('profile')
            else:
                messages.error(request, "Endereço não encontrado. Tente outro formato ou outro endereço.")
                print("⚠️ Nominatim retornou None!")
    else:

        form = UserAddressForm(instance=address)

    return render(request, 'address_form.html', {'form': form})

@login_required
def nearby_users(request):
    try:
        user_address = UserAddress.objects.get(user=request.user)
        user_location = Point(user_address.longitude, user_address.latitude)

        # Definir um raio de 10 km (ajuste conforme necessário)
        nearby_users = UserAddress.objects.exclude(user=request.user).filter(
            latitude__isnull=False,
            longitude__isnull=False
        )

        user_data = [
            {
                "username": user.user.username,
                "group": user.user.groups.first().name,
                "latitude": user.latitude,
                "longitude": user.longitude,
                "address": f"{user.rua}, {user.cidade}"
            }
            for user in nearby_users
        ]

        return JsonResponse({"users": user_data})

    except UserAddress.DoesNotExist:
        return JsonResponse({"error": "Endereço não encontrado"}, status=404)
    
@login_required
def map_view(request):
    return render(request, 'map.html')

@api_view(['GET'])
def search_users(request):
    query = request.GET.get('q', '')

    if query:
        users = User.objects.filter(username__icontains=query)
        addresses = UserAddress.objects.filter(
            Q(rua__icontains=query) | Q(cidade__icontains=query)
        )

        # Adiciona o link do perfil na resposta JSON
        user_results = [{
            'id': u.id, 
            'username': u.username, 
            'profile_url': reverse('user-profile', args=[u.id]),  # URL dinâmica do perfil
            'group': u.groups.first().name,
            'image_url': u.profile.image.url if hasattr(u, 'profile') and u.profile.image else '/media/profile_pics/default.jpg'
            
        } for u in users]

        address_results = [{
            'id': a.user.id, 
            'username': a.user.username, 
            'rua': a.rua, 
            'cidade': a.cidade
        } for a in addresses]

        return Response({'users': user_results, 'addresses': address_results})

    return Response({'users': [], 'addresses': []})

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    context = {
        'user_profile': user,  # Renomeamos para evitar conflito com request.user
        'form_img': DesignProfileForm(instance=user.profile),
    }

    if user.groups.filter(name='Doador').exists():
        products = ProductD.objects.filter(author=user)
        context['products'] = products
        return render(request, 'doador_profile.html', context)

    elif user.groups.filter(name='Receber Doação').exists():
        products = PedidoForm.objects.filter(author=user)
        context['products'] = products
        return render(request, 'recebidor_profile.html', context)

    return render(request, 'profile.html', context)
