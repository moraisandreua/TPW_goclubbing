from django.shortcuts import render, redirect
from app.models import Event, Business, Advertisement, Comment
from django.contrib.auth.models import User
from app.forms import EditProfileForm, AddEventForm, EditEventForm, AddAdvertForm, EditAdvertForm, Register
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from app.models import Business
from django.shortcuts import redirect

import folium
import geocoder


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
    api_key = '0p7iGyKlT41Pu8b0SQsqxGDpTDNLoQNu'

    f = folium.Figure(width=1000, height=1000)
    m = folium.Map([41.120736, -8.611354], zoom_start=25).add_to(f)
    folium.TileLayer('cartodbpositron').add_to(m)

    pp = folium.Html("<a onclick='javascript:parent.myfunction();' style='cursor:pointer;'>Bar do Fred</a>", script=True)
    popup = folium.Popup(pp, max_width=2650)
    folium.Marker(location=[41.120736, -8.611354], popup=popup).add_to(m)
    # depois aqui coloca-se os vários markers da base de dados

    businesses = Business.objects.all()
    for business in businesses:
        if business.lat is None or business.lng is None:
            geo = geocoder.mapquest(business.location, key=api_key)
            latlng = geo.latlng
            business.lat = latlng[0]
            business.lng = latlng[1]
            business.save()
        folium.Marker(location=[business.lat, business.lng]).add_to(m)

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
    ads = Advertisement.objects.all()
    comments = Comment.objects.all()
    business = Business.objects.get(user_id=request.user.id)
    tparams = {'events': events, 'ads': ads, 'comments': comments, 'self': business}
    return render(request, "dash_home.html", tparams)


def dashboard_newevent(request):
    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            return redirect(request, "dash_home.html")
        else:
            return render(request, "dash_new_event.html", {'form': form, 'error': True})
    else:
        form = AddEventForm(request.POST)
        return render(request, "dash_new_event.html", {'form': form})


def dashboard_event(request, num):
    event = Event.objects.get(id=num)
    if request.method == 'POST':
        form = EditEventForm(request.POST)
        if form.is_valid():
            return render(request, "dash_home.html")
        else:
            form = EditEventForm(initial={'name': event.name, 'location': event.location, 'datetime': event.datetime, 'theme': event.theme, 'min_age': event.min_age, 'organization': event.organization, 'dress_code': event.dress_code})
            return render(request, "dash_event.html", {'form': form, 'error': True, 'eventid': num})
    else:
        form = EditEventForm(initial={'name': event.name, 'location': event.location, 'datetime': event.datetime, 'theme': event.theme, 'min_age': event.min_age, 'organization': event.organization, 'dress_code': event.dress_code})
    return render(request, "dash_event.html", {'form': form, 'error': False, 'eventid': num})


def dashboard_newad(request):
    if request.method == 'POST':
        form = AddAdvertForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            return redirect(request, "dash_home.html")
        else:
            return render(request, "dash_new_ad.html", {'form': form, 'error': True})
    else:
        form = AddAdvertForm(request.POST)
        return render(request, "dash_new_ad.html", {'form': form})


def dashboard_ad(request, num):
    if request.method == 'POST':
        form = EditAdvertForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            return redirect(request, "dash_home.html")
        else:
            event = Event.objects.get(name="test")
            form = EditAdvertForm(initial={'name': event.name, 'location': event.location, 'datetime': event.datetime, 'theme': event.theme, 'min_age': event.min_age, 'organization': event.organization, 'dress_code': event.dress_code})
            return render(request, "dash_ad.html", {'form': form, 'error': True})
    else:
        event = Event.objects.get(id=num)
        form = EditAdvertForm(initial={'name': event.name, 'location': event.location, 'datetime': event.datetime, 'theme':event.theme, 'min_age':event.min_age, 'organization':event.organization, 'dress_code':event.dress_code})
    return render(request, "dash_ad.html", {'form': form, 'error': False})


def dashboard_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            return render(request, "dash_home.html")
    else:
        current_account = Business.objects.get(user_id=request.user.id)
        form = EditProfileForm(initial={'name': current_account.name, 'location': current_account.location, 'type': current_account.type, 'company_name':current_account.company_name, 'contact_phone':current_account.contact_phone, 'contact_email':current_account.contact_email, 'opening_hours':current_account.opening_hours})
    return render(request, "dash_profile.html", {'form': form})


def dashboard_my_events(request):
    events = Event.objects.all()
    business = Business.objects.get(user_id=request.user.id)
    tparams = {'events': events, 'self': business}
    return render(request, "see_events.html", tparams)


def dashboard_my_ads(request):
    ads = Advertisement.objects.all()
    business = Business.objects.get(user_id=request.user.id)
    tparams = {'ads': ads, 'self': business}
    return render(request, "see_ads.html", tparams)


def dashboard_my_comments(request):
    comments = Comment.objects.all()
    business = Business.objects.get(user_id=request.user.id)
    tparams = {'comments': comments, 'self': business}
    return render(request, "see_comments.html", tparams)
    return None


def dashboard_delete(request, num):
    return None
