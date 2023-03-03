from models.Attack import Attack
from models.Trigger import Trigger
from models.Item import Item

class Creature: 
  def __init__(self, Creature): 
    for att in Creature:
      tag = att.tag

      try: 
        # se já existe valor no atributo
        value = getattr(self, tag)

        # se não é uma lista
        if (not isinstance(value, list)):
          setattr(self, tag, [value, att])
        else:
          value.append(att)
          
      except(AttributeError):
        
        # não existe valor no atributo

        if (tag == "attack"):
          att = Attack(att)

        setattr(self, tag, att)

    