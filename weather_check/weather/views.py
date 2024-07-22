from django.shortcuts import render
from .forms import CityForm
from .utils import get_weather


def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST or None)
        if form.is_valid():
            city = form.cleaned_data["city_name"]
            print(city)
            table = get_weather(city)
            context = {
                'city': city,
                'table': table,
                'form': form,
            }
            return render(request, 'weather/index.html', context)
    form = CityForm()
    return render(request, 'weather/index.html', {'form': form})
