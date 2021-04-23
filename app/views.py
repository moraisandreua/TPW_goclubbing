from django.shortcuts import render
import folium


# Create your views here.
def index(request):
    return render(request, "index.html", {})

def register(request):
    return render(request, "auth.html", {})

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


