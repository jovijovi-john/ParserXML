class Container: 
  def __init__(self, Container): 

    #self.name  >>>  guarda o tipo do container
    #self.item  >>>  guarda os itens do container
    #self.status  >>>  guarda o status do container
    #self.trigger  >>>  guarda um trigger

    for att in Container:
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

    