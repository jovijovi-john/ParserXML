from XMLController import Controller
from models.Room import Room
from models.Container import Container
from models.Player import Player
from models.Item import Item
from utils.intervalInputValidator import intervalInputValidator

from time import sleep

import os

class View:
  
  def __init__(self, map: dict): 
    self.controller = Controller(map)
    self.player = Player()
    self.viewRoom(0, "")
    # mostra as opcoes
    # recebe a opcao
    # mostra as direcoes (em caso de opcao == "mover")
    # recebe a direcao
    # move
  
  def getRoomByIndex(self, index: int):
    """
      Retorna a {index + 1}º sala
    """
    return self.controller.keys[index]

  def viewRoom(self, index: int, nameRoom: str, **kwargs):
    """
      Busca uma sala:
        se index == -1 quer dizer que a busca vai ser apenas pelo nome. Senão, a busca vai ser pelo índice
        Ou seja, se passar um indice diferente de -1, o nameRoom não importa.
    """
    self.clearTerminal()

    if (index != -1): # buscar por índice
      nameRoom = self.getRoomByIndex(index)

    # buscar por nome
    room = self.controller.getRoom(nameRoom)

    self.showNameRoom(room)
    
    print("")
    self.showDescriptionRoom(room)
    print("")


    try:
      permanent = kwargs["permanent"]
    except KeyError:
      permanent = False

    if (room.hasCreature):
      creature = self.showCreatures(room, permanent)
    else:
      creature = None

    self.showMenuOptions(room, creature)

  def viewDirections(self, room: Room):
    """
      Mostra todas as borders de uma Room e retorna a quantidade de borders da sala
    """
    borders = room.border
    cont = 0

    print("\nDireções: \n")

    if (isinstance(borders, list)): 
      for border in borders:
        print(f"   -> Ao {border.direction} está a sala {border.name}. Digite {cont} para visitá-la." )
        cont += 1
    else: 
        print(f"   -> Ao {borders.direction} está a sala {borders.name}. Digite {cont} para visitá-la." )

    return cont

  def showMenuOptions(self, room: Room, creature):
    """
      Mostr todas as opções de ação disponíveis para uma sala 
    """
    options = ["Mover", "Mostrar Inventário"]

    if (room.hasItem):
      options.append("Mostrar itens")
    if (room.hasBaus):
      options.append("Mostrar containers")
    if (creature != None):
      options.append("Atacar")

    self.showOptions(options)
    option_input = intervalInputValidator(0, len(options) - 1)

    # Opção de Mover
    if (option_input == 0):
      qtd_directions = self.viewDirections(room)
      opt_direction = intervalInputValidator(0, qtd_directions)
      self.moveToDirection(opt_direction, room)
    

    #Mostrar inventório
    elif (option_input == 1):
      self.clearTerminal()
      
      sizeInventory = len(self.player.inventory)
      if (sizeInventory != 0):
        # mostra os itens do inventário
        self.showInventory()
        userItemIndex = intervalInputValidator(0, sizeInventory)
       
        # Se for a opção de voltar
        if (userItemIndex == sizeInventory):
          self.clearTerminal()
          print("Voltando para a sala...")
       
        else:
          item = self.getItemOfInvetory(userItemIndex) # atualiza o item do inventario 
          self.showItem(item)
          thrash = input("\nDigite qualquer tecla para voltar: ")

          if (thrash != None):
            self.clearTerminal()
            print("Voltando para a sala...")

      else:
        print("Não há items no inventário!")
      
      sleep(2)
      if room.creatureAlive:
        self.viewRoom(-1, room.name.text, permanent=True)
      else:
        self.viewRoom(-1, room.name.text)

        

    #Mostrar itens
    elif (options[option_input] == "Mostrar itens"):  
      self.clearTerminal()    
      index_lastItem = self.showItems(room)
      userItemIndex = intervalInputValidator(0, index_lastItem)
      
      # o ultimo index guarda a posição de voltar
      if index_lastItem != userItemIndex:
        item = self.controller.findItem(room, userItemIndex)
        
        # Pega o item
        self.controller.catchItem(room, userItemIndex, item, self.player)
        self.clearTerminal()
        print(f"Você pegou \033[1;33m{item.name.text}\033[m!!! \nVeja no seu inventário")
        sleep(2.5)

      # volta pra sala      
      if room.creatureAlive:
        self.viewRoom(-1, room.name.text, permanent=True)
      else:
        self.viewRoom(-1, room.name.text)


    #Mostra os containers(que tem itens) de uma sala
    elif (options[option_input] == "Mostrar containers"):
      self.clearTerminal()
      index_lastContainer = self.showContainersWithItems(room)
      userContainerIndex = intervalInputValidator(0, index_lastContainer)

      if index_lastContainer != userContainerIndex:
        container = self.controller.findContainerWithItem(room, userContainerIndex)
        index_lastItem = self.showItems(container)
        userItemIndex = intervalInputValidator(0, index_lastItem)
        
        if index_lastItem != userItemIndex:
          item = self.controller.findItem(container, userItemIndex)
          
          # Pega o item
          self.controller.catchItem(container, userItemIndex, item, self.player)
          self.clearTerminal()
          print(f"Você pegou \033[1;33m{item.name.text}\033[m!!! \nVeja no seu inventário")
          sleep(2.5)

      if room.creatureAlive:
        self.viewRoom(-1, room.name.text, permanent=True)
      else:
        self.viewRoom(-1, room.name.text)

    elif (options[option_input] == "Atacar"):
      resultado = self.controller.attackCreature(self.player, creature)
      if resultado == "venceu":
        self.clearTerminal()
        print(f"\033[1;32m{creature.attack.print.text}\033[m")
        
        self.controller.removeCreature(room, creature)
        sleep(2)
        
        # voltando para a sala
        self.viewRoom(-1, room.name.text)
      else:
        self.clearTerminal()
        print(f"\033[1;31m{'=|=|=' * 21 }")
        print (f"{'GAME OVER ' * 11}\n")

        print(resultado)
        print(f"{creature.name.text} matou você\n")

        print (f"{'GAME OVER ' * 11}")
        print(f"\033[1;31m{'=|=|=' * 21 }\033[m\n")

  def showOptions(self, options):
    print("\nEscolha uma opção: \n")
    print("=========================================")
    for index, option in enumerate(options):
      print(f"[ {index} ] = {option} ")
    print("=========================================")

  def showItems(self, obj):
    """
      Printa todos os itens de um objeto e retorna a quantidade de itens dele
    """
    string = f"\033[1;34m{'*=*=*=' * 8}\033[m"

    print(string)
    print("ITENS DISPONÍVEIS: ".center(50))
    print(string + "\n")

    cont = 0
    # se tem mais de 1 item
    if obj.hasItem:
      if (isinstance(obj.item, list)):
        
        for item in obj.item:
          print(f"[ {cont} ] - {item.name.text}")

          try:
            print(f"\033[3;30m{' ' * 7} {item.writing.text}\033[m")
          except:
            pass

          cont += 1

      else:
        print(f"[ {cont} ] - {obj.item.name.text}")
        try:
          print(f"\033[3;30m{' ' * 7} {obj.item.writing.text}\033[m")
        except:
          pass

        cont = 1
    print(f"[ {cont} ] - Voltar para a sala")

    return cont

  def showContainers(self, room: Room):
    """
      Mostra todos os containers de uma sala
    """
    string = f"\033[1;35m{'*=*=*=' * 8}\033[m"

    print(string)
    print("CONTAINERS DISPONÍVEIS: ".center(50))
    print(string + "\n")

    cont = 0
    # se tem mais de 1 item
    if (isinstance(room.container, list)):

      for container in room.container:
        name = container.name.text
        print(f"[ {cont} ] - {name}")
        cont += 1

    else:
      print(f"[ {cont} ] - {room.container.name.text}")
      cont = 1
    
    print(f"[ {cont} ] - Voltar para a sala")

    return cont
  
  def showContainersWithItems(self, room: Room):
    """
      Mostra todos os containers de uma sala
    """
    string = f"\033[1;35m{'*=*=*=' * 8}\033[m"

    print(string)
    print("CONTAINERS DISPONÍVEIS: ".center(50))
    print(string + "\n")

    cont = 0
    for container in room.baus:
      name = container.name.text
      print(f"[ {cont} ] - {name}")
      cont += 1
    
    print(f"[ {cont} ] - Voltar para a sala")

    return cont

  def showInventory(self):
    """
      Mostra o inventário do player
    """
    print(f"\033[1;36mItems no inventário: \n\033[m")
    for index, item in enumerate(self.player.inventoryNames):
      print (f"[ {index} ] - {item}" ) 
    
    print(f"[ {index + 1} ] - Voltar")

  def clearTerminal(self):
    """
      Limpa o terminal, seja no windows ou linux
    """
    os.system('cls||clear')
  
  def showDescriptionRoom(self, room: Room):
    """
      Mostra a descrição da sala
    """
    print(f"\033[3;33m{room.description.text}\033[m")
  
  def showNameRoom(self, room: Room):
    """
      Mostra o nome da sala estilizado
    """
    print(f"\033[1;32m{'*=*=' * 20}\033[m")
    print(f"Você está na sala {room.name.text}".center(80))
    print(f"\033[1;32m{'*=*=' * 20}\033[m \n")

  def getItemOfInvetory(self, indexItem: int):
    
    item = self.player.inventory[indexItem]
    
    return item 

  def showItem(self, item: Item):
    """
      Mostra um item e atualiza seu status
    """
    self.clearTerminal()
    print(f"\033[1;32mItem: {item.name.text}\033[m \n")
    
    # Padronizando status do objeto
    try:
      item.status = item.status.text
    except:
      pass
    
    # Mostrando os status do item se existir
    try:
      print(f"status: {item.status}")
    except AttributeError:
      pass
    
    # Mostrando a descrição do item
    try:
       print(f"\033[3;33m{item.writing.text}\033[m")
    except AttributeError:
      pass

    #Mostrando  mensagem de atualização
    print(self.controller.updateObj(item)) 

    #confirmando que o print não aparecerá na proxima vez que escolher o item
    self.controller.updateStatusObj(item) 
    
  def moveToDirection(self, indexBorder, room):
    """
      Move o usuário para a sala correspondente à borda
    """
    
    borders = room.border

    if (isinstance(borders, list)):
      border_choosed = borders[indexBorder]
    else: 
      border_choosed = borders

    # guardando o comando utilizado
    self.player.command = border_choosed.direction

    # verificando se tem trigger
    if (room.hasTrigger):
      isblocked = self.verifyBlocked(room.trigger, self.player, room)
      if isblocked:
        return
    
    # verificando se na sala tem container
    if (room.hasContainer):
      # verificando se tem mais de um container na sala
      if (isinstance(room.container, list)):
        for container in room.container:
          # verificando se o container atual tem trigger
          if container.hasTrigger:
           
            # iterando sobre cada trigger:
            if (isinstance(container.trigger, list)):
              for trigger in container.trigger:

                isblocked = self.verifyBlocked(trigger, self.player, room, nextRoom=border_choosed.name, container=container)

                if isblocked:
                  return
    
    # move para a sala referente
    self.viewRoom(-1, border_choosed.name)

  def verifyBlocked(self, obj, player: Player, room: Room, **kwargs):

    """
      Ativa triggers para o
    """

    self.clearTerminal()
    action = self.controller.toTrigger(obj, player)
                  
    if action != None:
        print(obj.print.text)
        sleep(2)

        # continua na mesma sala
        if action != "success":
          self.viewRoom(-1, room.name.text)
        else:
          # removendo container de bloqueio
          self.controller.removeContainer(room, kwargs["container"])
          self.viewRoom(-1, kwargs["nextRoom"])
        
        return True

  def showCreatures(self, room: Room, permanent: bool):

    creatures = room.creature

    if (isinstance(creatures, list)):

      for creature in creatures:
        print(creature.name.text)
        isblocked = self.controller.toTrigger(creature.trigger, self.player, room)
        if isblocked and not permanent:
          return
    else: 
      creature = room.creature
      retorno = self.controller.toTrigger(creature.trigger, self.player)

      if retorno == "success" or permanent:
        print(f"\033[1;31m{'=|=|=' * 20 }\n")
        print(f"{creature.trigger.print.text}\n")
        print(f"{' ' * 5}Criatura: {creature.name.text}")
        print(f"{' ' * 5}Fraqueza: {creature.vulnerability.text}\n")
        print(f"\033[1;31m{'=|=|=' * 20 }\033[m")

        room.creatureAlive = True

      return creature

  