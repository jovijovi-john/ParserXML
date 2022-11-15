from XMLController import Controller
from models.Room import Room
from models.Container import Container
from models.Player import Player
from utils.intervalInputValidator import intervalInputValidator


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

  def viewRoom(self, index: int, nameRoom: str):
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

    self.viewContainers(room) # diz se tem container ou nao
    self.viewItems(room) # diz se tem itens ou nao
    print("")

    self.showDescriptionRoom(room)

    self.showMenuOptions(room)

  def viewDirections(self, room: Room):
    """
      Mostra todas as borders de uma Room
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

    opt_direction = int(input("\nDigite a opção desejada: "))

    # str(type(room.border)) == "<class 'list'>"
    if (isinstance(borders, list)):
      direction = borders[opt_direction]
    else: 
      direction = borders

    self.viewRoom(-1, direction.name)
    #return direction.name

  def showMenuOptions(self, room: Room):
    """
      Mostr todas as opções de ação disponíveis para uma sala 
    """
    options = ["Mover", "Mostrar Inventário"]

    if (room.hasItem):
      options.append("Mostrar itens")
    if (room.hasContainer):
      options.append("Mostrar containers")

    self.showOptions(options)
    option_input = intervalInputValidator(0, len(options) - 1)

    # Opção de Mover
    if (option_input == 0):
      self.viewDirections(room)

    #Mostrar inventório
    elif (option_input == 1):
      self.clearTerminal()
      self.showInventory()
      thrash = input("\nDigite qualquer coisa para voltar para a sala: ")
    
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
        print(f"Item pego: {item}")
        
      # volta pra sala
      self.viewRoom(-1, room.name.text)

    #Mostra os containers de uma sala
    elif (options[option_input] == "Mostrar containers"):
      self.clearTerminal()
      index_lastContainer = self.showContainers(room)
      userContainerIndex = intervalInputValidator(0, index_lastContainer)
      
      if index_lastContainer != userContainerIndex:
        container = self.controller.findContainer(room, userContainerIndex)
        print(container.name.text)

      self.viewRoom(-1, room.name.text)

  def showOptions(self, options):
    print("\nEscolha uma opção: \n")
    print("=========================================")
    for index, option in enumerate(options):
      print(f"[ {index} ] = {option} ")
    print("=========================================")



    
  def viewContainers(self, room: Room):

    if (room.hasContainer):
      if(isinstance(room.container, list)):
        print(f"Tem {len(room.container)} containers")
      else:
        print(f"Tem 1 container")
    else:
      print("Não tem container")      

  def viewContainer(self, container: Container):
    if (container.hasItem):
      print("Tem item no container")

  def viewItems(self, room: Room):

    if (room.hasItem):
      if (isinstance(room.item, list)):
        print(f"Tem {len(room.item)} items")
      else: 
        print(f"Tem 1 item")
    else:
      print("Não tem items")

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
        print(f"[ {cont} ] - {container.name.text}")
        cont += 1

    else:
      print(f"[ {cont} ] - {room.container.name.text}")
      cont = 1
    
    print(f"[ {cont} ] - Voltar para a sala")
    


    return cont



  def showInventory(self):
    """
      Mostra o inventário do player
    """
    print(f"\033[1;36mItems no inventário: {self.player.inventoryNames}\033[m")

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
    