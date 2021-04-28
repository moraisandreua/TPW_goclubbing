from django.shortcuts import render, redirect
from app.models import Event, Business, Advertisement, Comment
from django.contrib.auth.models import User
from app.forms import EditProfileForm, AddEventForm, EditEventForm, AddAdvertForm, EditAdvertForm, Register, Login
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from app.models import Business, BusinessPhoto, Event
from django.shortcuts import redirect
from django.contrib.auth import authenticate

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

            return redirect('/login/', message={'type': "success", 'body': 'Utilizador criado com sucesso!'})
    else:
        form = Register()

    return render(request, "auth.html", {'auth_signup':True, 'form':form})


def search(request):

    api_key = '0p7iGyKlT41Pu8b0SQsqxGDpTDNLoQNu'

    query = request.GET.get('query', False)

    if query:
        geo = geocoder.mapquest(query, key=api_key)
        startPoint = geo.latlng
        zoom_start = 12
    else:
        geo = geocoder.mapquest("Portugal", key=api_key)
        startPoint = geo.latlng
        zoom_start = 7

    f = folium.Figure(width=1000, height=1000)
    m = folium.Map(startPoint, zoom_start=zoom_start).add_to(f)
    folium.TileLayer('cartodbpositron').add_to(m)

    # depois aqui coloca-se os vários markers da base de dados

    businesses = Business.objects.all()
    for business in businesses:
        if business.lat is None or business.lng is None:
            geo = geocoder.mapquest(business.location, key=api_key)
            latlng = geo.latlng
            business.lat = latlng[0]
            business.lng = latlng[1]
            business.save()

        pp = folium.Html("<a href='/search/"+str(business.id)+"' target='_parent'>"+business.name+"</a>",
                         script=True)
        popup = folium.Popup(pp, max_width=2650)
        folium.Marker(location=[business.lat, business.lng], popup=popup).add_to(m)

    m = m._repr_html_()

    types=[]

    for x in Business.objects.all():
        if x.type.lower()[0].upper() + x.type.lower()[1:] not in types:
            types.append(x.type.lower()[0].upper() + x.type.lower()[1:])

    context = {'my_map': m, 'types':types}

    return render(request, 'search.html', context)


def searchName(request, id):
    business = Business.objects.filter(id=id).get()

    api_key = '0p7iGyKlT41Pu8b0SQsqxGDpTDNLoQNu'

    f = folium.Figure(width=1000, height=1000)
    m = folium.Map([business.lat, business.lng], zoom_start=17).add_to(f)
    folium.TileLayer('cartodbpositron').add_to(m)

    # depois aqui coloca-se os vários markers da base de dados

    businesses = Business.objects.all()
    for bus in businesses:
        if bus.lat is None or bus.lng is None:
            geo = geocoder.mapquest(bus.location, key=api_key)
            latlng = geo.latlng
            bus.lat = latlng[0]
            bus.lng = latlng[1]
            bus.save()

        pp = folium.Html("<a href='/search/" + str(bus.id) + "' target='_parent'>" + bus.name + "</a>",
                         script=True)
        popup = folium.Popup(pp, max_width=2650)
        folium.Marker(location=[bus.lat, bus.lng], popup=popup).add_to(m)

    m = m._repr_html_()


    businessPhoto = BusinessPhoto.objects.filter(business=business)
    photoUrls = []
    for photo in businessPhoto:
        photoUrls.append(photo.path.url)
    events = Event.objects.filter(business=business)
    businessType = business.type

    types=[]
    for x in Business.objects.all():
        if x.type.lower()[0].upper() + x.type.lower()[1:] not in types:
            types.append(x.type.lower()[0].upper() + x.type.lower()[1:])

    context = {
        'my_map': m,
        'businessName': business.name,
        'businessProfilePhoto': business.profilePhoto,
        'businessPhoto': photoUrls,
        'events': events,
        'businessType': businessType,
        'type':types
    }

    return render(request, 'businessSideCard.html', context)


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
