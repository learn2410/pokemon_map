import folium
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = localtime()
    current_pokemons = PokemonEntity.objects.select_related('pokemon').filter(
        appeared_at__lte=now,
        disappeared_at__gte=now)
    for pokemon_entity in current_pokemons:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            if pokemon_entity.pokemon.image else DEFAULT_IMAGE_URL
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(
                pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    requested_pokemon = {
        'pokemon_id': pokemon.id,
        'img_url': request.build_absolute_uri(pokemon.image.url)
        if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
    }
    if pokemon.previous_evolution:
        requested_pokemon.update({'previous_evolution': {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(
                pokemon.previous_evolution.image.url)
            if pokemon.previous_evolution.image else DEFAULT_IMAGE_URL,
        }
        })
    next_pokemon = pokemon.next_evolutions.first()
    if next_pokemon:
        requested_pokemon.update({'next_evolution': {
            'title_ru': next_pokemon.title,
            'pokemon_id': next_pokemon.id,
            'img_url': request.build_absolute_uri(
                next_pokemon.image.url)
            if next_pokemon.image else DEFAULT_IMAGE_URL
        }
        })

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = localtime()
    current_pokemons = pokemon.entities.filter(
        appeared_at__lte=now,
        disappeared_at__gte=now,
    )

    for pokemon_entity in current_pokemons:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            if pokemon_entity.pokemon.image else DEFAULT_IMAGE_URL
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
