## Cria um objeto room e garante que se existir dois atributos com mesmo nome, esse atributo passará a ser um array com esses valores

from models.Condition import Condition

class Trigger: 
  def __init__(self, Trigger): 
    for att in Trigger:
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
        
        if (tag == "condition"):
          att = Condition(att)
        
        setattr(self, tag, att)
    