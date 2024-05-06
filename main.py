from api import cvp_api
import IDMap
import ConfigletsAndMappers
import argparse

# Warning DOES NOT HANDLE TENANT LEVEL CONFIGLETS
cvaas_token = ""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--topology", help="Topology JSON from RESTAPI", required=True)
    parser.add_argument("-m", "--mappers", help="Mappers JSON from RESTAPI", required=True)
    cmd_args = parser.parse_args()
    print(cmd_args.topology, cmd_args.mappers)

    # /cvpservice/provisioning/filterTopology.do?format=topology&startIndex=0&endIndex=0
    topology_id_map = IDMap.TopologyIDMap(cmd_args.topology, filter="")

    # /cvpservice/configlet/getConfigletsAndAssociatedMappers.do
    cm = ConfigletsAndMappers.Mappers(cmd_args.mappers, topology_id_map)
    print(cm)

    cvaas = cvp_api(cvaas_token, cvaas_url='www.cv-prod-us-central1-c.arista.io')
    cvaas.update_configs(mappers=cm, noEdit=[])

    # cvaas.create_container_layout(topology_id_map.containerID_map,
    #                               topology_id_map.topo["topology"]["childContainerList"])

    # cm.update_configs(cvp_client)
    # cm.apply_configlets(cvp_client)
