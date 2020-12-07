import requests
spaceShips = requests.get("https://swapi.dev/api/starships/").json()
ships = []


class Starship():
    def __init__(self, name, pilots):
        self.name = name
        self.pilots = pilots

    def printStats(self):
        print(self.name)
        for name in self.pilots:
            reseacrh_pilot =requests.get(name).json()
            print(reseacrh_pilot['name'],reseacrh_pilot['height'])
           

for ship in spaceShips['results']:
    currentShip = len(ships)
    ships.append('a')
    ships[currentShip] = Starship(ship['name'], ship['pilots'])
    ships[currentShip].printStats()
    print("\n")
    