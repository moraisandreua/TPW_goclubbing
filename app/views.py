from django.shortcuts import render
from app.forms import Register
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from app.models import Business
from django.shortcuts import redirect

import folium


# Create your views here.
def index(request):
    return render(request, "index.html", {})

def register(request):
    if request.method == 'POST':
        form = Register(request.POST)

        if form.is_valid():
            try:
                user = User.objects.create_user(username=form.cleaned_data["username"], password=form.cleaned_data["password"], email=form.cleaned_data["email"])
                business = Business(name=form.cleaned_data["name"], location=form.cleaned_data["location"], type=form.cleaned_data["type"], company_name=form.cleaned_data["company"], contact_email=form.cleaned_data["email"], contact_phone=form.cleaned_data["phone"], user=user)
                user.save()
                business.save()
            except:
                return render(request, "auth.html", {'auth_signup':True, 'form':form, 'message': {'type': "error", 'body': 'Utilizador já existe!'}})

            return redirect('/login', message={'type': "success", 'body': 'Utilizador criado com sucesso!'})
    else:
        form = Register()

    return render(request, "auth.html", {'auth_signup':True, 'form':form})

def search(request):
    f = folium.Figure(width=1000, height=1000)
    m = folium.Map([41.120736, -8.611354], zoom_start=25).add_to(f)
    folium.TileLayer('cartodbpositron').add_to(m)

    pp = folium.Html("<a onclick='javascript:parent.myfunction();' style='cursor:pointer;'>Bar do Fred</a>", script=True)
    popup = folium.Popup(pp, max_width=2650)
    folium.Marker(location=[41.120736, -8.611354], popup=popup).add_to(m)
    # depois aqui coloca-se os vários markers da base de dados
    m = m._repr_html_()
    context = {'my_map': m}

    return render(request, 'search.html', context)


def searchName(request, id):
    f = folium.Figure(width=1000, height=1000)
    m = folium.Map([41.120736, -8.611354], zoom_start=25).add_to(f)
    folium.TileLayer('cartodbpositron').add_to(m)
    pp = folium.Html('<a id="openmodals" onclick="openModal()">' + 'Bar do Fred' + '</a>', script=True)
    popup = folium.Popup(pp, max_width=2650)
    folium.Marker(location=[41.120736, -8.611354], popup=popup).add_to(m)
    # depois aqui coloca-se os vários markers da base de dados
    m = m._repr_html_()
    context = {'my_map': m, 'name':id}

    return render(request, 'search.html', context)


def dashboard(request):
    return render(request, "dashboard.html")


def dashboard_profile(request):
    return render(request, "dash_profile.html")


def dashboard_home(request):
    return render(request, "dash_home.html")


