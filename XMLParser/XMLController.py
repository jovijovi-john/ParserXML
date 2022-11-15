from models.Border import Border
from models.Room  import Room
from models.Container  import Container
from models.Item import Item

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
      
      self.createBordersObj(room)
      self.createItemsObject(room)
      self.createContainersObj(room)
    
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
    """
      Recebe uma room e transforma todas suas borders em objetos Border

      :param Room room : Sala que terá as borders trasnformadas em objetos
    """

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
    """
      Recebe uma room e transforma todos seus containers em objetos Container

      :param Room room : Sala que terá os containers trasnformados em objetos
    """

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
    """
      Recebe um objeto e adiciona na propriedade hasItem um bool

      :param   (Room | Container)   obj  :  Local que será verificado se tem item
    """
    try:
      item = obj.item
      obj.hasItem = True
    except AttributeError:
      obj.hasItem = False
  
  def createItemsObject(self, obj):

    self.hasItem(obj)

    if (obj.hasItem):        
      items = obj.item
      
      if (isinstance(items, list)):
        items_obj = []

        for item in items:
          item_obj = Item(item)
          items_obj.append(item_obj)
        
        obj.item = items_obj
      else:
        item_obj = Item(obj.item)
        obj.item = item_obj

  def hasContainer(self, room):
    """
      Recebe uma room e adiciona na propriedade hasContainer um bool

      :param   Room   room  :  Sala que será verificada
    """
    try:
      container = room.container
      room.hasContainer = True
    except AttributeError:
      room.hasContainer = False

  
  def findItem(self, obj, index):
    """
      Retorna um item de um objeto a partir de um index

      :param (Room | Container)   obj   : Local de onde será buscado o item 
      :param int                  index : index do item no obj
    """
    item = obj.item

    if (isinstance(item, list)):
      return item[index]
    else:
      return item
  
  def findContainer(self, room, index):
    container = room.container
    
    if (isinstance(container, list)):
      return container[index]
    else:
      return container
     

  def catchItem(self, obj, index_item, item, player):
    """
      Pega um item de uma sala ou de um container, remove ele de onde ele estava e coloca no inventário do usuário

      :param  (Room | Container) obj         :  Local de onde será retirado o item 
      :param  int                index_item  :  Index do item no obj
      :param  Item               item        :  item que irá para o inventário 
      :param  Player             player      :  player que receberá o item
    """
    try:
      items = obj.item
      player.addItem(item)

      if (isinstance(items, list)):
        items.pop(index_item)
        if (len(items) == 0):
          obj.hasItem = False

      else:
        items = []
        obj.hasItem = False

    except:
      print("NÃO EXISTE ITEM NO OBJETO")

