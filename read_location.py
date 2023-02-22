"""
Module that read file
"""
def read_file(filename):
    with open(filename, 'r') as file:
        films = []
        for line in file:
            if line.startswith('"'):
                film = line.replace('"', '').replace("(interior scwnes)", '').split('(')
                film_name = film[0].strip()
                year = film[1].split(')')[0]
                address = line.split('\t')[-1].strip()
                films.append([film_name, year, address])
    return films