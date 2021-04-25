from django.shortcuts import render, redirect
from app.models import Event, Business
from django.contrib.auth.models import User
from app.forms import EditProfileForm, EditEventForm, Register
import folium


# Create your views here.
def index(request):
    return render(request, "index.html", {})

def register(request):
    if request.method == 'POST':
        form = Register(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=form.username, password=form.password, email=form.email)
            user.save()
            return render(request, "auth.html", {'message':{'type':"success", 'body':'Utilizador criado com sucesso.'}})
    else:
        form = Register()

    return render(request, "auth.html", {'auth_signup':True, 'form':form, 'message':{'type':"success", 'body':'Utilizador criado com sucesso.'}})

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
    context = {'my_map': m, 'name': id}

    return render(request, 'search.html', context)


def dashboard_home(request):
    events = Event.objects.all()
    tparams = {'events': events}
    return render(request, "dash_home.html")


def dashboard_event(request, num):
    if request.method == 'POST':
        form = EditEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            return redirect(request, "dash_home.html")
        else:
            event = Event.objects.get(id=num)
            form = EditProfileForm(initial={'name': event.name, 'location': event.location, 'datetime': event.datetime, 'type': event.type,'theme': event.theme, 'min_age': event.min_age, 'organization': event.organization, 'dress_code': event.dress_code})
            return render(request, "dash_event.html", {'form': form, 'error': True})
    else:
        event = Event.objects.get(id=num)
        form = EditProfileForm(initial={'name': event.name, 'location': event.location, 'datetime': event.datetime, 'type': event.type, 'theme':event.theme, 'min_age':event.min_age, 'organization':event.organization, 'dress_code':event.dress_code})
    return render(request, "dash_event.html", {'form': form, 'error': False})


def dashboard_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            return render(request, "dash_home.html")
    else:
        current_account = Business.objects.get(id=1)    #substituir por current user
        form = EditProfileForm(initial={'name': current_account.name, 'location': current_account.location, 'type': current_account.type, 'company_name':current_account.company_name, 'contact_phone':current_account.contact_phone, 'contact_email':current_account.contact_email, 'opening_hours':current_account.opening_hours})
    return render(request, "dash_profile.html", {'form': form})