from models.TurnOn import TurnOn

class Item:
  
  def __init__(self, Item):

    for att in Item:
      tag = att.tag
      
      if (tag == "turnon"):
        att = TurnOn(att)
      
      setattr(self, tag, att)

      

    