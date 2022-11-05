class Container:
  
  def __init__(self, Container):

    #self.name  >>>  guarda o tipo do container
    #self.item  >>>  guarda um item
    #self.status  >>>  guarda o status do container
    #self.trigger  >>>  guarda um trigger
    
    for att in Container:
      tag = att.tag
      setattr(self, tag, att)

    