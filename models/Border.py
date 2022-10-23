class Border:
  
  def __init__(self, Border):

    #self.name  >>>  guarda o nome da sala
    #self.direction  >>>  guarda o nome da direção
 
    for att in Border:
      tag = att.tag
      setattr(self, tag, att.text)

    