from django.shortcuts import render
from app.models import Event, Business, Advertisement, Comment
from django.contrib.auth.models import User
from app.forms import EditProfileForm, EventForm, AdvertForm, Register
from app.models import Business, BusinessPhoto, Event
from django.shortcuts import redirect
import logging

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
                user = User.objects.create_user(username=form.cleaned_data["username"],
                                                password=form.cleaned_data["password"],
                                                email=form.cleaned_data["email"])
                business = Business(name=form.cleaned_data["name"], location=form.cleaned_data["location"],
                                    type=form.cleaned_data["type"], company_name=form.cleaned_data["company"],
                                    contact_email=form.cleaned_data["email"], contact_phone=form.cleaned_data["phone"],
                                    user=user)
                user.save()
                business.save()
            except:
                return render(request, "auth.html", {'auth_signup': True, 'form': form,
                                                     'message': {'type': "error", 'body': 'Utilizador já existe!'}})

            return redirect('/login/', message={'type': "success", 'body': 'Utilizador criado com sucesso!'})
    else:
        form = Register()

    return render(request, "auth.html", {'auth_signup': True, 'form': form})


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

        pp = folium.Html("<a href='/search/" + str(business.id) + "' target='_parent'>" + business.name + "</a>",
                         script=True)
        popup = folium.Popup(pp, max_width=2650)
        folium.Marker(location=[business.lat, business.lng], popup=popup).add_to(m)

    m = m._repr_html_()

    types = []

    for x in Business.objects.all():
        if x.type.lower()[0].upper() + x.type.lower()[1:] not in types:
            types.append(x.type.lower()[0].upper() + x.type.lower()[1:])

    context = {'my_map': m, 'types': types}

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

    types = []
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
        'types': types
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
        form = EventForm(request.POST)
        if form.is_valid():
            event = Event(name=form.cleaned_data["name"], location=form.cleaned_data["location"],
                          type=form.cleaned_data["type"], theme=form.cleaned_data["theme"],
                          datetime=form.cleaned_data["datetime"], organization=form.cleaned_data["organization"],
                          dress_code=form.cleaned_data["dress_code"], min_age=form.cleaned_data["min_age"],
                          business=request.user.business)
            event.save()

            events = Event.objects.all()
            ads = Advertisement.objects.all()
            comments = Comment.objects.all()
            tparams = {'events': events, 'ads': ads, 'comments': comments,
                       'self': Business.objects.get(user_id=request.user.id)}
            return render(request,"dash_home.html", tparams)
        else:
            #form = EventForm()
            return render(request, "dash_new_event.html", {'form': form, 'error': True})
    else:
        form = EventForm()
        return render(request, "dash_new_event.html", {'form': form, 'error': False})


def dashboard_event(request, num):
    current_event = Event.objects.get(id=num)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            current_event.name = form.cleaned_data["name"]
            current_event.location = form.cleaned_data["location"]
            current_event.type = form.cleaned_data["type"]
            current_event.theme = form.cleaned_data["theme"]
            current_event.datetime = form.cleaned_data["datetime"]
            current_event.organization = form.cleaned_data["organization"]
            current_event.dress_code = form.cleaned_data["dress_code"]
            current_event.min_age = form.cleaned_data["min_age"]
            current_event.save()

            events = Event.objects.all()
            ads = Advertisement.objects.all()
            comments = Comment.objects.all()
            tparams = {'events': events, 'ads': ads, 'comments': comments, 'self': Business.objects.get(user_id=request.user.id)}
            return render(request, "dash_home.html", tparams)
        else:
            form = EventForm(initial={'name': current_event.name, 'location': current_event.location, 'type': current_event.type, 'theme': current_event.theme, 'datetime': current_event.datetime, 'organization': current_event.organization, 'min_age': current_event.min_age, 'dress_code': current_event.dress_code})
            return render(request, "dash_event.html", {'num': num, 'eventid':num, 'form': form, 'error': True, 'message': bool(form.errors)})
    else:
        form = EventForm(initial={'name': current_event.name, 'location': current_event.location, 'type': current_event.type, 'theme': current_event.theme, 'datetime': current_event.datetime, 'organization': current_event.organization, 'min_age': current_event.min_age, 'dress_code': current_event.dress_code})
        return render(request, "dash_event.html", {'num': num, 'eventid': num,'form': form, 'error': False})


def dashboard_newad(request):
    if request.method == 'POST':
        form = AdvertForm(request.POST)
        if form.is_valid():
            ad = Advertisement(event=form.cleaned_data["event"], date=form.cleaned_data["date"], expire=form.cleaned_data["expire"], body=form.cleaned_data["body"])
            ad.save()

            events = Event.objects.all()
            ads = Advertisement.objects.all()
            comments = Comment.objects.all()
            tparams = {'events': events, 'ads': ads, 'comments': comments,
                       'self': Business.objects.get(user_id=request.user.id)}
            return render(request,"dash_home.html", tparams)
        else:
            return render(request, "dash_new_ad.html", {'form': form, 'error': True})
    else:
        form = AdvertForm()
        form.fields['event'].queryset = Event.objects.filter(business__user=request.user)
        return render(request, "dash_new_ad.html", {'form': form, 'error': False})


def dashboard_ad(request, num):
    current_ad = Advertisement.objects.get(id=num)
    if request.method == 'POST':
        form = AdvertForm(request.POST)
        if form.is_valid():
            current_ad.event = form.cleaned_data["event"]
            current_ad.date = form.cleaned_data["date"]
            current_ad.expire = form.cleaned_data["expire"]
            current_ad.body = form.cleaned_data["body"]
            current_ad.save()

            events = Event.objects.all()
            ads = Advertisement.objects.all()
            comments = Comment.objects.all()
            tparams = {'events': events, 'ads': ads, 'comments': comments,
                       'self': Business.objects.get(user_id=request.user.id)}
            return render(request, "dash_home.html", tparams)
        else:
            form = AdvertForm(initial={'event': current_ad.event, 'date': current_ad.date, 'expire': current_ad.expire, 'body': current_ad.body})
            return render(request, "dash_ad.html.html", {'num': num, 'form': form, 'error': True, 'message': form.errors})
    else:
        form = AdvertForm(initial={'event': current_ad.event, 'date': current_ad.date, 'expire': current_ad.expire,'body': current_ad.body})
        return render(request, "dash_ad.html", {'num': num, 'form': form, 'error': False})


def dashboard_profile(request):
    current_account = Business.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            current_account.name = form.cleaned_data["name"]
            current_account.location = form.cleaned_data["location"]
            current_account.address = form.cleaned_data["address"]
            current_account.type = form.cleaned_data["type"]
            current_account.company_name = form.cleaned_data["company_name"]
            current_account.opening_hours = form.cleaned_data["opening_hours"]
            current_account.contact_phone = form.cleaned_data["contact_phone"]
            current_account.contact_email = form.cleaned_data["contact_email"]
            #current_account.profilePhoto = request.FILES['file']
            current_account.save()

            events = Event.objects.all()
            ads = Advertisement.objects.all()
            comments = Comment.objects.all()
            tparams = {'events': events, 'ads': ads, 'comments': comments, 'self': current_account}
            return render(request, "dash_home.html", tparams)
        else:
            form = EditProfileForm(initial={'name': current_account.name, 'location': current_account.location, 'address': current_account.address,
                                            'type': current_account.type, 'company_name': current_account.company_name,
                                            'contact_phone': current_account.contact_phone,
                                            'contact_email': current_account.contact_email,
                                            'opening_hours': current_account.opening_hours})
            return render(request, "dash_profile.html",
                          {'form': form, 'error': True, 'message': bool(form.errors)})

    else:
        form = EditProfileForm(
            initial={'name': current_account.name, 'location': current_account.location, 'address': current_account.address, 'type': current_account.type,
                     'company_name': current_account.company_name, 'contact_phone': current_account.contact_phone,
                     'contact_email': current_account.contact_email, 'opening_hours': current_account.opening_hours})
    return render(request, "dash_profile.html", {'form': form, 'error': False})


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


def dashboard_delete(request, num):
    event = Event.objects.get(id=num).delete()
    events = Event.objects.all()
    ads = Advertisement.objects.all()
    comments = Comment.objects.all()
    business = Business.objects.get(user_id=request.user.id)
    tparams = {'events': events, 'ads': ads, 'comments': comments, 'self': business}
    return render(request, "dash_home.html", tparams)


def dashboard_ad_delete(request, num):
    ad = Advertisement.objects.get(id=num).delete()
    events = Event.objects.all()
    ads = Advertisement.objects.all()
    comments = Comment.objects.all()
    business = Business.objects.get(user_id=request.user.id)
    tparams = {'events': events, 'ads': ads, 'comments': comments, 'self': business}
    return render(request, "dash_home.html", tparams)


def dashboard_comment_delete(request, num):
    comment = Comment.objects.get(id=num).delete()
    events = Event.objects.all()
    ads = Advertisement.objects.all()
    comments = Comment.objects.all()
    business = Business.objects.get(user_id=request.user.id)
    tparams = {'events': events, 'ads': ads, 'comments': comments, 'self': business}
    return render(request, "dash_home.html", tparams)
