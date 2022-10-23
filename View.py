from XMLController import Controller
from models.Room import Room
import os

class View:
  
  def __init__(self, map: dict): 
    self.controller = Controller(map)
    self.viewRoom(0, "")
    # mostra as opcoes
    # recebe a opcao
    # mostra as direcoes (em caso de opcao == "mover")
    # recebe a direcao
    # move
  
  def getRoomByIndex(self, index: int):
    return self.controller.keys[index]

  def viewRoom(self, index: int, nameRoom: str):

    """
      se index == -1 quer dizer que a busca vai ser apenas pelo nome. Senão, a busca vai ser pelo índice

      Ou seja, se passar um indice diferente de -1, o nameRoom não importa.
    """

    os.system("cls") # clear terminal

    if (index != -1): # buscar por índice
      nameRoom = self.getRoomByIndex(index)

    # buscar por nome
    room = self.controller.getRoom(nameRoom)

    print(f"\033[1;32m{'*=*=' * 20}\033[m")
    print("Você está na sala " + room.name.text)
    print(f"\033[1;32m{'*=*=' * 20}\033[m \n")
    
    print(room.description.text)

    self.showMenuOptions(room)


  def viewDirections(self, room: Room):
    borders = room.border
    cont = 0

    print("\nDireções: \n")

    if (str(type(room.border)) == "<class 'list'>"): 
      for border in borders:
        print(f"   -> Ao {border.direction} está a sala {border.name}. Digite {cont} para visitá-la." )
        cont += 1
    else: 
        print(f"   -> Ao {borders.direction} está a sala {borders.name}. Digite {cont} para visitá-la." )

    opt_direction = int(input("\nDigite a opção desejada: "))

    if (str(type(room.border)) == "<class 'list'>"):
      direction = borders[opt_direction]
    else: 
      direction = borders

    self.viewRoom(-1, direction.name)
    #return direction.name

  def showMenuOptions(self, room: Room):
    print("\nEscolha uma opção: \n")
    print("=========================================")
    print("[ 0 ] - Mover")
    print("[ 1 ] - Pegar Item")
    print("=========================================")

    option = int(input(": "))
    if option == 0:
      self.viewDirections(room)
