import json, urandom

class Interceptron:
    def generate_id(length=36):
        return ''.join(random.choice(string.ascii_letters + string.digits)for _ in range(length))
    def __init__(self, name, Brain=None):
        self.name = name
        self.Brain = Brain
        self.datastore = {}
        self.msgstore = []

        self.id = self.generate_id()
        self.send_data_raw({ "type": "init", "init": "id", "id": self.id })
    def init_graph(self, name, labels=["X","Y"]):
        if len(labels)!=2: return self.err
        self.send_data_raw({ "type": "init", "init": "graph", "name": name, "labels": labels })
        self.name
    def send_data_raw(self, data):
        if type(data)==dict: self.err("Can only send Dict Type to JSON")
        self.msgstore.append(data)
        data['id'] = self.id
        print(json.dumps(data))
    def err(self, msg, type=TypeError):
        self.send_data_raw({ "type": "error", "msg": msg })
        raise type(msg)
    def listen(self, f1, f2):
        self