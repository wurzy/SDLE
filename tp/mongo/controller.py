from connection import MongoController

c = MongoController("ola")
#c.saveMessage(None,"ola")
#c.saveMessage("ole",{"id": 1, "xd":1})
#c.saveMessage("ole",{"id": 2, "xd":1})
#c.saveMessage("ole",{"id": 3, "xd":1})
#c.saveMessage("ole",{"id": 4, "xd":1})
#c.saveMessage("ole",{"id": 5, "xd":1})
c.getTimeline()