class Item:
  
  def __init__(self, Item):

    for att in Item:
      print(att)
      tag = att.tag
      setattr(self, tag, att)

    