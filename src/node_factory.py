import logging


class NodeFactory: # TODO I don't like the way these work, should go over it again

    def __init__(self, in_dict, factory_name, hierarchy=None):
        self.logger = logging.getLogger(__name__)
        self.next_id = 0
        self.in_dict = in_dict # TODO horrible name
        self.factory_name = factory_name
        self.hierarchy = hierarchy
        if self.hierarchy is None:
            self.hierarchy = list(in_dict.keys())

    def reset(self):
        self.next_id = 0

    def set_next(self, x):
        self.next_id = x

    def node_from_dict(self, system):
        name = system["name"]
        interactables = system["interactables"]
        position = system["position"]
        creation_time = system["creation_time"]
        if name in self.in_dict:
            node = self.instantiate(node_id=system["node_id"], node_name=name, interactables=interactables)
            node.set_position(position)
            node.creation_time = creation_time
            return node
        else:
            self.logger.warning("WARNING: UNKNOWN NODE")

    def instantiate(self, node_name, node_id=None, interactables=None):
        node = self.in_dict[node_name]()
        node.set_node_id(f"{self.factory_name}:{self.next_id}" if node_id is None else node_id)
        node.set_factory_id(self.factory_name)
        node.set_node_name(node_name)

        if interactables is not None:
            logging.debug(interactables)
            for interactble_properties, interactable in zip(interactables, node.interactables):
                interactable.set(interactble_properties["value"])
        if node_id is None:
            self.next_id += 1
        return node

    def get_factory_name(self):
        return self.factory_name
