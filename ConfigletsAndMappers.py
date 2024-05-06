import json
import IDMap


class Mappers:
    device_map = {}
    containermapper_map = {}
    mappers = {}
    configlets = {}

    def __init__(self, file_path, ID_map: IDMap.TopologyIDMap) -> None:
        # /cvpservice/configlet/getConfigletsAndAssociatedMappers.do
        file = open(file_path)
        data = json.load(file)
        self.mappers = data["data"]["configletMappers"]
        self.configlets = data["data"]["configlets"]
        file.close
        self._setup_map()
        # self.ID_map = ID_map
        self.containermapper_map = self._sort_map(ID_map.containerID_map, self.containermapper_map)
        self.device_map = self._sort_map(ID_map.deviceID_map, self.device_map)

    def _setup_map(self):
        for map in self.mappers:
            if map["type"] == "container":
                for configlet in self.configlets:
                    if map["configletId"] == configlet["key"]:
                        if map["objectId"] in self.containermapper_map:
                            self.containermapper_map[map["objectId"]].append(configlet["name"])
                        else:
                            self.containermapper_map[map["objectId"]] = [configlet["name"]]
                        # print(f'{map["objectId"]} {configlet["name"]}')
            elif map["type"] == "netelement":
                for configlet in self.configlets:
                    if map["configletId"] == configlet["key"] and map["containerId"] == "":
                        if map["objectId"] in self.device_map:
                            self.device_map[map["objectId"]].append(configlet["name"])
                        else:
                            self.device_map[map["objectId"]] = [configlet["name"]]
            else:
                # Incase of new types
                print(map["type"])

    def _sort_map(self, key_look_up, dict):
        final = {}
        # Converts Key to Names
        for obj in dict:
            # Only care for obj we have keys for (Sneaky way of using the Filter from IDMap)
            if obj in key_look_up:
                final[key_look_up[obj]] = dict[obj]
        myKeys = list(final.keys())
        myKeys.sort()
        dict = {i: final[i] for i in myKeys}
        return dict

    # Overwriting the print call for the class
    def __repr__(self) -> str:
        if len(self.containermapper_map) == 0 and len(self.device_map) == 0:
            return "Maps are empty"
        out = ""
        for container_name in self.containermapper_map:
            out += f"{container_name}\n"
            for configlet_name in self.containermapper_map[container_name]:
                out += f"\t {configlet_name}\n"
        out += "\nDevices:\n"
        for device in self.device_map:
            out += f"{device} - Device\n"
            for configlet_name in self.device_map[device]:
                out += f"\t {configlet_name}\n"
        return out
