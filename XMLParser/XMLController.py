from models.Border import Border
from models.Room  import Room
from models.Container  import Container
from models.Item import Item
from models.Creature import Creature
from models.Player import Player
from models.Trigger import Trigger

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
      self.createTriggersObject(room)
      self.createCreaturesObject(room)
      self.hasBaus(room)
    
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
    
    room.baus = []
    self.hasContainer(room)

    # Se existe containers na sala
    if (room.hasContainer == True):
      # Se existe só um container na sala
      if (isinstance(room.container, list)):
        containers = room.container #array
        containers_obj = []

        for container in containers:
          container_obj = Container(container)
          self.createItemsObject(container_obj) # se tiver item ele cria os itens

          if container_obj.hasItem:
            room.baus.append(container_obj)
            print(container_obj.name.text)

          self.createTriggersObject(container_obj)
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
  
  def hasCreature(self, room: Room):
    """
      Recebe uma sala adiciona na propriedade hasCreature um bool

      :param   (Room )   room  :  sala que será verificado se tem criatura
    """
    try:
      creature = room.creature
      room.hasCreature = True
    except AttributeError:
      room.hasCreature = False
  
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

  def createTriggersObject(self, obj):
    self.hasTrigger(obj)

    if (obj.hasTrigger):

      triggers = obj.trigger

      if (isinstance(triggers, list)):
        triggers_objs = []

        for trigger in triggers:
          trigger_obj = Trigger(trigger)
          trigger_obj.pai = obj # referenciando quem é o pai do trigger
          triggers_objs.append(trigger_obj)
        
        obj.trigger = triggers_objs
      else:
        trigger_obj = Trigger(obj.trigger)
        obj.trigger = trigger_obj

  def createCreaturesObject(self, room: Room):
    
    self.hasCreature(room)

    if (room.hasCreature):        
      creatures = room.creature
      
      if (isinstance(creatures, list)):
        creatures_obj = []

        for creature in creatures:
          creature_obj = Creature(creature)
          self.createItemsObject(creature_obj) # se tiver item ele cria os itens
          self.createTriggersObject(creature_obj) # criando os triggers

          creatures_obj.append(creature_obj)
        
        room.creature = creatures_obj
      else:
        creature_obj = Creature(room.creature)
        self.createItemsObject(creature_obj) # se tiver item ele cria os itens
        self.createTriggersObject(creature_obj) # criando os triggers
        room.creature = creature_obj

  def hasBaus(self, room):
    """
      Recebe uma room e adiciona na propriedade hasBaus um bool

      :param   Room   room  :  Sala que será verificada
    """
    try: 
      containers = room.baus

      if containers != []:
        room.hasBaus = True
      else:
        print(containers)
        print(containers != [])
        room.hasBaus = False
    except AttributeError:
      room.hasBaus = False

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
     
  def findContainerWithItem(self, room, index):
    containers = room.baus
    
    return containers[index]

  def catchItem(self, obj, index_item, item, player: Player):
    """
      Pega um item de uma sala, de uma criatura ou de um container, remove ele de onde ele estava e coloca no inventário do usuário

      :param  (Room | Container | Creature) obj         :  Local de onde será retirado o item 
      :param  int                           index_item  :  Index do item no obj
      :param  Item                          item        :  item que irá para o inventário 
      :param  Player                        player      :  player que receberá o item
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
      raise(ValueError)

  def verifiyTypeTrigger(self, trigger: Trigger):
    """
      Retorna o type do trigger, caso não haja, retorna None
    """
    try:
      typeTrigger = trigger.type.text
      return typeTrigger
    except ValueError:
      return None

  def hasTrigger(self, obj):
    """
      Recebe um objeto e adiciona na propriedade hasItem um bool

      :param   (Room | Container | Creature)   obj  :  Local que será verificado se tem item
    """
    try:
      trigger = obj.trigger
      obj.hasTrigger = True
    except AttributeError:
      obj.hasTrigger = False
    
  def toTrigger(self, obj, player: Player):
    
    if isinstance(obj, Trigger):
      trigger = obj
    else:
      trigger = obj.trigger


    typeTrigger = self.verifiyTypeTrigger(trigger)

    if (typeTrigger == "permanente"):
      # Trigger que bloqueia ou não movimentação entre salas

      # Como já sabemos que refere-se à movimentação devemos verificar 
      # se a direção escolhida é a mesma que está bloqueada
      if (player.command == trigger.command.text):
        try:
          # has object owner
          if (trigger.condition.has != None and trigger.condition.object != None):
            return self.triggerHasObjectOwner(trigger, player)
        except AttributeError:
          try:
             # status
            if (trigger.condition.status != None):
              # se a condição é apenas status então quer dizer que o trigger está dentro de um container
              return self.triggerStatus(trigger, player)
          
           
          except AttributeError:
            try:
              # object owner
              if (trigger.condition.object != None):
                  pass
            except:
              pass
    elif (typeTrigger == "único"):
      try:
        # status object owner 
        if (trigger.condition.status != None and trigger.condition.object != None):
          itemTrigger = trigger.condition.object
          itemPlayer = self.findItemInInventory(player, itemTrigger)

          if itemPlayer.status == trigger.condition.status:
            return "success"
              
          # if trigger.condition.status == itemPlayer.status:
      except AttributeError:

        try:
          # has(sim) object owner
          if (trigger.condition.has != None and trigger.condition.object != None):
            return self.triggerHasObjectOwner(trigger, player)
        except: 
          print("probleminhas")
          # no final de um trigger único ele é apagado da sala/container
      
  def triggerStatus(self, trigger: Trigger, player: Player):
    statusPai = trigger.pai.status.text
    statusTrigger = trigger.condition.status

    if statusPai == statusTrigger:
      return "blocked"
    else:
      return None

  def triggerStatusObject(self, trigger: Trigger, player: Player):
      itemTrigger = trigger.condition.object
      itemPlayer = self.findItemInInventory(player, itemTrigger)

      try:
        statusItem = itemPlayer.status
      except:
        statusItem = ""
      
      if statusItem == itemTrigger.status:
        return "success"
      
      return None

  def hasItemInInventory(self, player: Player, itemName):
    try:
      index = player.inventoryNames.index(itemName)
      return True
    except ValueError:
      return False

  def findItemInInventory(self, player: Player, itemName):
    """
      Retorna um item do inventário baseado no itemName
    """
    try:
      indexItem = player.inventoryNames.index(itemName)
      item = player.inventory[indexItem]
    except ValueError:
      item = None

    return item

  def triggerHasObjectOwner(self, trigger: Trigger, player: Player):
      if (trigger.condition.has == "não"):
        if (not self.hasItemInInventory(player, trigger.condition.object)):
          return "blocked" 
      else:
        if (self.hasItemInInventory(player, trigger.condition.object)):
          return "success"
      
      return None

  def updateObj(self, obj):
    if (obj.turnon.print != ""):
      try:
        # action = obj.turnon.action
        status = "ativado"
        obj.status = status

        return obj.turnon.print
      except AttributeError:
        pass

    return ""
  
  def attackCreature(self, player: Player, creature: Creature):

    condition = creature.attack.condition
    item = self.findItemInInventory(player, condition.object)

    # object status
    
    if item == None:
      return f"Não há {condition.object} no inventário"

    if (condition.status == item.status):
      if creature.hasItem:
        # pegando os itens dropados pela criatura
        itemsDrops = creature.item
        # verificando se tem mais de um item
        if (isinstance(itemsDrops, list)):
          for index, item_drop in itemsDrops:
            self.catchItem(creature, index, item_drop, player)
        else:
          self.catchItem(creature, 0, itemsDrops, player)

      return "venceu"
    else:
      return f"{item.name.text} desativado"
   
    # object
    try:
      print()
    except:
      pass
  
  def removeCreature(self, room: Room, creature: Creature):
    
    # verificando se a sala tem mais de uma criatura
    creatures = room.creature
    
    if (isinstance(creatures, list)):
      for index, creatureRoom in enumerate(creatures):
        if creatureRoom == creature:
          creatures.pop(index)

          if (len(creatures) == 0):
            room.hasCreature = False
    else:
      room.creature = []
      room.hasCreature = False

  def removeContainer(self, room: Room, container: Container):
    
    # verificando se a sala tem mais de uma criatura
    containers = room.container
    
    if (isinstance(containers, list)):
      for index, containerRoom in enumerate(containers):
        if containerRoom == container:
          containers.pop(index)

          if (len(containers) == 0):
            room.hasContainer = False

    else:
      room.container = []
      room.hasContainer = False
  
  def removeTrigger(self, container: Container, trigger: Trigger):
    
    # verificando se a sala tem mais de uma criatura
    triggers = container.trigger
    
    if (isinstance(triggers, list)):
      for index, triggerContainer in enumerate(triggers):
        if triggerContainer == trigger:
          triggers.pop(index)

          if (len(triggers) == 0):
            container.hasTrigger = False

    else:
      container.trigger = []
      container.hasTrigger = False
  
  def updateStatusObj(self, obj):
    obj.turnon.print = ""