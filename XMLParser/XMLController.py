from models.Border import Border
from models.Room  import Room
from models.Container  import Container
from models.Item  import Item

class Controller:

  def __init__(self, rooms: list):
    self.map = self.createMap(rooms)
    self.keys = self.createListKeys()

  def createMap(self, rooms: list):
    """
      Recebe uma lista de Rooms e retorna um dicionário onde cada chave é o nome de uma sala e o valor é um objeto Room correspondente

      :param list rooms: Lista de salas (objetos Room)
    """
    map_rooms = {}

    for room in rooms:
      print(room.item)
      
      print("\n")
      for item in room.item:
        print(f"primeiro item: {item}")
      self.createBordersObj(room)
      

      # Atualizando a sala com as novas informações
      map_rooms[room.name.text] = room
    return map_rooms

  def getRoom(self, name: str):
    """
      Retorna uma sala baseado no nome passado como parâmetro

      :param str name: Nome da sala a ser retornada
    """
    return self.map[name]

  def createListKeys(self):
    """
      Converte as keys do map ( que é um dicionário ) para uma lista
    """
    list_keys = list(self.map.keys())
    return list_keys

  def createBordersObj(self, room):
    # Verificando se o objeto border da Sala contém mais de uma borda
    if (str(type(room.border)) == "<class 'list'>"):
      borders = room.border #array
      borders_obj = []
      
      # Convertendo todas as bordas para um objeto Border
      for border in borders:
        border_obj = Border(border)
        borders_obj.append(border_obj)
      
      room.border = borders_obj
    else:
      # Convertendo a borda para um Objeto border
      border_obj = Border(room.border)
      room.border = border_obj

  def createContainersObj(self, room):

    self.hasContainer(room)

    # Se existe containers na sala
    if (room.hasContainer == True):
      # Se existe só um container na sala
      if (isinstance(room.container, list)):
        containers = room.container #array
        containers_obj = []

        for container in containers:
          container_obj = Container(container)
          self.createItemsObject(container_obj)
          containers_obj.append(container_obj)
        
        room.container = containers_obj
      else:
        container_obj = Container(room.container) 
        self.createItemsObject(container_obj)
        room.container = container_obj

  def hasItem(self, obj):
    try:
      item = obj.item
      obj.hasItem = True
    except AttributeError:
      obj.hasItem = False
  
  def createItemsObject(self, obj):

    print(f"O item é {obj.item}")
    self.hasItem(obj)

    if (obj.hasItem):        
      items = obj.item
      
      if (isinstance(items, list)):
        items_obj = []

        for item in items:
          print(item)
          item_obj = Item(item)
          items_obj.append(item_obj)
        
        obj.item = items_obj
      else:
        item_obj = Item(obj.item)
        obj.item = item_obj


  def hasContainer(self, room):
    try:
      container = room.container
      room.hasContainer = True
    except AttributeError:
      room.hasContainer = False
