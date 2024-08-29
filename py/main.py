import json, urandom

class Interceptron:
    def generate_id(length=36):
        return ''.join(random.choice(string.ascii_letters + string.digits)for _ in range(length))
    def __init__(self, name, Brain=None):
        self.name = name
        self.Brain = Brain
        self.Timer = Timer()
        self.graph_stores = []
        self.msglen = 0

        self.id = self.generate_id()
        self.send_data({ "type": "init", "init": "id", "id": self.id })
    def send_data(self, data):
        if type(data)==dict: self.err("Can only send Dict Type to JSON", TypeError)
        self.msgstore += 1
        data['id'] = self.id
        print(json.dumps(data))
    def err(self, msg, type=BaseException):
        self.send_data({ "type": "error", "msg": msg })
        raise type(msg)

    def graph_init(self, name, labels=["X","Y"]):
        if len(labels)!=2: return self.err
        self.send_data({ "type": "init", "init": "graph", "name": name, "labels": labels })
        self.graph_stores.append({ "name": name, "labels": labels, "listening": False })
    def graph_data(self, name, f1, f2):
        self.send_data({ "type": "graphdata", "name": name, "y": f1(), "x": f2() })
    def graph_listen(self, name, callback1, callback2, delay=50):
        if name not in self.graph_stores: return self.err("Graph name not found/initialized: "+name, ValueError)
        if self.graph_stores[self.graph_stores.index(name)]["listening"]: return self.err("Graph is already listening. You can close the listener with Interceptron.graph_close")
        self.graph_stores[self.graph_stores.index(name)]["listening"] = True
        def loop():
            self.graph_data(self, name, callback1, callback2)
            if self.graph_stores[self.graph_stores.index(name)]["listening"]:
                self.Timer.event(loop, delay)
        loop()
        return self.graph_stores.index(name)
    def graph_close(self, name):
        if name not in self.graph_stores: return self.err("Graph name not found/initialized: "+name, ValueError)
        self.graph_stores[self.graph_stores.index(name)]["listening"] = False
    