class Item:
  
  def __init__(self, Item):

    for att in Item:
      tag = att.tag
      setattr(self, tag, att)

    