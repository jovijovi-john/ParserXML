class Player:

  def __init__(self):
    self.inventory = []
    self.inventoryNames = []
  
  def addItem(self, item):
    self.inventory.append(item)
    self.inventoryNames.append(item.name.text)
  
  def removeItem(self, item):
    self.inventory.remove(item)
    self.inventoryNames.remove(item.name.text)