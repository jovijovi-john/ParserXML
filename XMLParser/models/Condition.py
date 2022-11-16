class Condition:
  
  def __init__(self, Condition):

    for att in Condition:
      tag = att.tag
      setattr(self, tag, att.text)

    