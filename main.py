import xml.etree.ElementTree as ET
from models.Room import Room
from View import View

tree = ET.parse('adventure.xml') # le o arquivo
root = tree.getroot()

rooms = []

for room in root:
  sala = Room(room)
  rooms.append(sala)

view = View(rooms)

