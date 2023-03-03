from models.Condition import Condition

class Attack:
  
  def __init__(self, Attack):

    for att in Attack:
      tag = att.tag

      if (tag == "condition"):
          att = Condition(att)
          
      setattr(self, tag, att)

    