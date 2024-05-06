import requests.packages.urllib3
from cvprac.cvp_client import CvpClient
import ssl
import ConfigletsAndMappers


class cvp_api:
    def __init__(self, cvaas_token, cvaas_url='www.arista.io', client=None):
        if client:
            return
        # TODO if given a client skip
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings()
        self.cvp_client = CvpClient()
        self.cvp_client.connect(nodes=[cvaas_url], username='',
                                password='', is_cvaas=True, api_token=cvaas_token)
        print(self.cvp_client.api.get_cvp_info())

    def create_container_layout(self, filtered, dict):
        for container in dict:  # topo["topology"]["childContainerList"]:
            # print(filtered.values())
            if filtered and container["name"] in filtered.values():
                # add container
                print(container["name"])
                self.create_container_layout(None, container["childContainerList"])
        # self.cvp_client.api.add_container(container_name, parent_name, parent_key)
        # for device in respose
        # if device in containermapper_map
        # add container
        # raise NotImplementedError

    def update_configs(self, mappers: ConfigletsAndMappers.Mappers, noEdit: list):
        # list[dict[Name, Key]]
        cvaas_configlets = self.cvp_client.api.get_configlets()
        names = []
        for c in mappers.containermapper_map.values():
            names.extend(c)
        for c in mappers.device_map.values():
            names.extend(c)
        for api_configlet in mappers.configlets:
            if api_configlet["name"] in noEdit:
                print(f'Skipping {api_configlet["name"]}... Not Updating')
                continue
            if api_configlet["name"] not in names:
                continue
            if api_configlet['type'].lower() != "static":
                continue
            existing_config = None
            for cvaas_configlet in cvaas_configlets['data']:
                if api_configlet['name'] == cvaas_configlet['name']:
                    existing_config = cvaas_configlet
            if existing_config:
                if api_configlet['config'] == existing_config['config']:
                    print(f"Skipping {api_configlet['name']}... Nothing to Update")
                    continue
                print(f"Updating: {api_configlet['name']}")
                res = self.cvp_client.api.update_configlet(
                    api_configlet['config'],
                    existing_config['key'],
                    api_configlet['name'])
                print(res)
            else:
                print(f"Creating: {api_configlet['name']}")
                res = self.cvp_client.api.add_configlet(
                    api_configlet['name'], api_configlet['config'])
                print(res)
                cvaas_configlets = self.cvp_client.api.get_configlets()

    # Filter containermapper_map based on UserInput
    def apply_configlets(self, containermapper_map):
        all_containers = {}
        print("Setting Up Container Dictionary")
        res = self.cvp_client.api.get_containers()
        for container in res['data']:
            all_containers[container['name']] = container
        print("Done")
        all_configlets = self.cvp_client.api.get_configlets()
        for container_name in containermapper_map:
            configlets = []
            for configlet_name in containermapper_map[container_name]:
                for configlet in all_configlets["data"]:
                    # This is getting the CVaaS key of the configlet
                    if configlet_name == configlet["name"]:
                        configlets.append(
                            {"name": configlet["name"], "key": configlet["key"]})
            if len(configlets) > 0:
                res = self.cvp_client.api.apply_configlets_to_container(
                    'pythonautomation', all_containers[container_name], configlets)
                tmp = ""
                for conf in configlets:
                    tmp += f"\t{conf['name']}\n"
                print(
                    f"{container_name}: {res['data']['status'].upper()}\n{tmp}")

    # def update_configsOLD(self, mappers: ConfigletsAndMappers.Mappers):
    #     # list[dict[Name, Key]]
    #     cvaas_configlets = self.cvp_client.api.get_configlets()
    #     for api_configlet in mappers.configlets:
    #         # Dont handle any configlet thats not static
    #         if api_configlet['type'].lower() != "static":
    #             continue
    #         existing_config = None
    #         for cvaas_configlet in cvaas_configlets['data']:
    #             if api_configlet['name'] == cvaas_configlet['name']:
    #                 existing_config = cvaas_configlet
    #         if existing_config:
    #             if api_configlet['config'] == existing_config['config']:
    #                 print(f"Skipping {api_configlet['name']}... Nothing to Update")
    #                 continue
    #             print(f"Updating: {api_configlet['name']}")
    #             res = self.cvp_client.api.update_configlet(
    #                     api_configlet['config'],
    #                     existing_config['key'],
    #                     api_configlet['name'])
    #             print(res)
    #         else:
    #             print(f"Creating: {api_configlet['name']}")
    #             res = self.cvp_client.api.add_configlet(api_configlet['name'], api_configlet['config'])
    #             print(res)
    #             cvaas_configlets = self.cvp_client.api.get_configlets()
