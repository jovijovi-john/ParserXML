from models.Border import Border

class Controller:

  def __init__(self, rooms: list):
    self.map = self.createMap(rooms)
    self.keys = self.createListKeys()

  def createMap(self, rooms: list):
    map_rooms = {}

    for room in rooms:
      
      if (str(type(room.border)) == "<class 'list'>"):
        borders = room.border #array
        borders_obj = []

        for border in borders:
          border_obj = Border(border)
          borders_obj.append(border_obj)
        
        room.border = borders_obj
      else:
        border_obj = Border(room.border)
        room.border = border_obj

      map_rooms[room.name.text] = room
    return map_rooms

  def getRoom(self, name: str):
    return self.map[name]

  def createListKeys(self):
    list_keys = list(self.map.keys())
    return list_keys