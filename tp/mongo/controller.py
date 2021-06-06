from connection import MongoController

c = MongoController("rir1")
#c.saveMessage(None,"ola")
#c.saveMessage("ole",{"id": 1, "xd":1})
#c.saveMessage("ole",{"id": 2, "xd":1})
#c.saveMessage("ole",{"id": 3, "xd":1})
#c.saveMessage("ole",{"id": 4, "xd":1})
#c.saveMessage("ole",{"id": 5, "xd":1})
#c.getTimeline()

c.saveMessages({
    "c": {
        "1": {
            "username": "c",
            "message": "c 1",
            "id": 18742260594014805534375936,
            "msg_nr": 1,
            "time": "2021-06-06 12:34:45",
            "seen": True
        },
        "2": {
            "username": "c",
            "message": "c 2",
            "id": 18742262850881168800415744,
            "msg_nr": 2,
            "time": "2021-06-06 12:34:53",
            "seen": True
        },
        "3": {
            "username": "c",
            "message": "c 3",
            "id": 18742269383070953324609536,
            "msg_nr": 3,
            "time": "2021-06-06 12:35:16",
            "seen": True
        },
        "4": {
            "username": "c",
            "message": "c 4",
            "id": 18742284303777993779773440,
            "msg_nr": 4,
            "time": "2021-06-06 12:36:09",
            "seen": True
        },
        "5": {
            "username": "c",
            "message": "c 5",
            "id": 18742290653853468372172800,
            "msg_nr": 5,
            "time": "2021-06-06 12:36:32",
            "seen": True
        }
    },
    "d": {
        "6": {
            "username": "d",
            "message": "d 6",
            "id": 18742298422844300563054592,
            "msg_nr": 6,
            "time": "2021-06-06 12:36:59",
            "seen": True
        }
    }
})