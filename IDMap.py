import json


class TopologyIDMap:
    """ Handles parsing and filtering of the topology.
    Topology info comes from the CloudVision REST API (Manually),
    Passed by file on `init`
    API End point `GET /cvpservice/provisioning/filterTopology.do?format=topology&startIndex=0&endIndex=0`
    REST API Explorer can be used to download this data.
    """

    containerID_map = {}
    deviceID_map = {}

    def __init__(self, filePath, filter=None) -> None:
        # GET /cvpservice/provisioning/filterTopology.do?format=topology&startIndex=0&endIndex=0
        file = open(filePath)
        self.topo = json.load(file)
        file.close
        if filter:
            self._search_containers(self.topo["topology"]["childContainerList"], filter)
        else:
            self._parse_topology(self.topo["topology"]["childContainerList"])

    # TODO Chnage to BFS or DFS (Preorder?) or Level Order Treversal
    def _parse_topology(self, dict):
        for container in dict:
            self.containerID_map[container["key"]] = container["name"]
            for net in container["childNetElementList"]:
                self.deviceID_map[net["key"]] = net["fqdn"]
            if container["childContainerList"] and len(container["childContainerList"]) > 0:
                self._parse_topology(container["childContainerList"])

    def _search_containers(self, dict, filter):
        for container in dict:
            if container["name"] == filter:
                tmp = [container]
                self._parse_topology(tmp)
                return
        print(f"Couldn't Find Container Name: {filter}")
