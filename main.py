import read_location
import haversine
import argparse
import folium
from geopy.geocoders import Nominatim
from haversine import haversine, Unit
import requests, pandas


def filter(films:list[tuple], year:int) -> list[tuple]:
    """
    Filter list of films by year
    >>> filter([('#1 Single', '2006', 'Los Angeles, California, USA'),('#15SecondScare', \
'2015', '(interior scwnes)'),('#ATown', '2014', 'Texas Rowing Center, Austin, Texas, USA')], 2014)
    [('#ATown', '2014', 'Texas Rowing Center, Austin, Texas, USA')]
    """
    res = []
    for film in films:
        ################################### ТУТ РОЗГЛЯДАЄТЬСЯ ЛИШЕ 10. Я на них тестив. А всі не запускаються
        if len(res) > 10:
            return res
#####################################################################
        try:
            if int(film[1]) == year:
                res.append(film)
        except ValueError:
            continue
    return res

def coordinator(films:list[list]) -> list[list]:
    """
    Change addres to coordinates
    # >>> coordinator[['#1 Single', '2006', 'Los Angeles, California, USA'], ['#1 Single', '2006', 'New York City, New York, USA']]
    """
    for film in films:
        try:
            geolocator = Nominatim(user_agent="film_places")
            location = geolocator.geocode(film[-1])
            film[-1] = location.latitude
            film.append(location.longitude)
        except AttributeError:
            continue
    return films
def map_of_films(year, lat, lon, path):
    """
    create a map 
    """
    mapa = folium.Map(location=[lat, lon], zoom_start=10)
    counter = 0
    filtered_list_films = coordinator(filter(read_location.read_file(path), year))
    for film in filtered_list_films:
        print(film)
        try:
            try:
                lat_film, lon_film = float(film[-2]), float(film[-1])
            except ValueError:
                continue
            folium.Marker(location=[lat_film, lon_film],
                          popup=f'Title: {film[0]}\n\
                            Year: {film[1]}\
                                \n Distance:'
                                f' {round(haversine((lat, lon), (lat_film, lon_film)), 2)}',
                          icon=folium.Icon(color='blue')).add_to(mapa)
            counter += 1
        except IndexError:
            continue
        if counter > 10:
            break
    point = folium.FeatureGroup(name="Random point")
    point.add_child(folium.Marker(location=[35.8617, 104.1954],
                            popup="random point",
                            icon=folium.Icon(color = 'red')))
    mapa.add_child(point)
    mapa.save('Films.html')

def main():
    """
    MAIN FUNCTION
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("year" , help = "рік")
    parser.add_argument("latitude", help = "широта")
    parser.add_argument("longitude" , help = "довгота")
    parser.add_argument("path", help = "шлях до файлу")

    args = parser.parse_args()
    map_of_films(args.year, args.latitude, args.longitude, args.path)

main()

# map_of_films(2000, 49.83826, 24.02324, 'locations.list')
# print(coordinator([['#1 Single', '2006', 'Los Angeles, California, USA'], ['#1 Single', '2006', 'New York City, New York, USA']]))
# def nearest_point(lat, lon, films):
#     cords = (lat,lon)
#     nearest_coord = []
#     for film in films:
#         try:
#             if len(nearest_coord) > 10:
#                 return nearest_coord
#             nearest = min(films[film[-1]], key=lambda coord: haversine(cords, coord, unit=Unit.MILES))
#             if len(nearest) == 2:
#                 nearest_coord.append(nearest)
#                 film[-1].remove(nearest)
#         except TypeError:
#             continue
#     return nearest_coord
# print(nearest_point(49.83826, 24.02324, coordinator(filter(read_location.read_file('locations.list'), 2004))))
# print(coordinator(filter(read_location.read_file('locations.list'), 2004)))
# print(coordinator(filter(read_location.read_file('locations.list'),2004)))
# print(nearest_point(49.83826, 24.02324, [['#1 Single', '2006', 'Los Angeles, California, USA'], ['#1 Single', '2006', 'New York City, New York, USA']]))
# def map_of_films(year, lat, long, path):
#     filtered_list_films = coordinator(filter(read_location.read_file(path), year))
#     for film in filtered_list_films:
#         add
#     map = folium.Map()
#     map.save('Films.html')
#     pass

# map_of_films(1,2,3,4)
# if __name__ == "__main__":
#     import doctest
#     print(doctest.testmod())

    


    