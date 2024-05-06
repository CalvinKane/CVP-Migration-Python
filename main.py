from api import cvp_api
import IDMap
import ConfigletsAndMappers
import argparse

# Service Account Token
cvaas_token = ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--topology", help="Topology JSON from RESTAPI", required=True)
    parser.add_argument("-m", "--mappers", help="Mappers JSON from RESTAPI", required=True)
    cmd_args = parser.parse_args()
    print(cmd_args.topology, cmd_args.mappers)

    # GET /cvpservice/provisioning/filterTopology.do?format=topology&startIndex=0&endIndex=0
    # Filter can be used to limit down to one container including its children
    # Only works with a container directly under tenant
    topology_id_map = IDMap.TopologyIDMap(cmd_args.topology, filter="")

    # GET /cvpservice/configlet/getConfigletsAndAssociatedMappers.do
    cm = ConfigletsAndMappers.Mappers(cmd_args.mappers, topology_id_map)
    # Debugging or for Manual Checks
    print(cm)

    cvaas = cvp_api(cvaas_token, cvaas_url='www.cv-prod-us-central1-c.arista.io')
    # noEdit is a list of strings that will be ignored when updating configs on CVaaS
    cvaas.update_configs(mappers=cm, noEdit=[])

    # Warning DOES NOT HANDLE TENANT LEVEL CONFIGLETS
    cvaas.apply_configlets(mappers=cm)

    # cvaas.create_container_layout(topology_id_map.containerID_map,
    #                               topology_id_map.topo["topology"]["childContainerList"])
