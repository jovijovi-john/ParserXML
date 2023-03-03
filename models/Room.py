## Cria um objeto room e garante que se existir dois atributos com mesmo nome, esse atributo passará a ser um array com esses valores

class Room: 
  def __init__(self, Room): 
    for att in Room:
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
        setattr(self, tag, att)

    