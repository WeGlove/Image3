class NodeFactory:

    def __init__(self, device, frame_counter, in_dict, factory_name):
        self.next_id = 0
        self.device = device
        self.frame_counter = frame_counter
        self.in_dict = in_dict
        self.factory_name = factory_name

    def reset(self):
        self.next_id = 0

    def set_next(self, x):
        self.next_id = x

    def node_from_dict(self, properties, system):
        name = system["name"]
        interactables = system["interactables"]

        if name in self.in_dict:
            return self.instantiate(node_id=system["node_id"], node_name=name, interactables=interactables, **properties)
        else:
            raise ValueError(f"Unknown Node {name}")

    def instantiate(self, node_name, node_id=None, interactables=None, **properties):
        node = self.in_dict[node_name](device=self.device, node_id=f"{self.factory_name}:{self.next_id}" if node_id is None else node_id,
                                       frame_counter=self.frame_counter, factory_id=self.factory_name, **properties)
        if interactables is not None:
            print(interactables)
            for interactble_properties, interactable in zip(interactables, node.interactables):
                interactable.set(interactble_properties["value"])
        if node_id is None:
            self.next_id += 1
        return node

    def get_factory_name(self):
        return self.factory_name
