class TurnOn:
  
  def __init__(self, TurnOn):

    #self.print
    #self.action
 
    for att in TurnOn:
      tag = att.tag
      setattr(self, tag, att.text)

    