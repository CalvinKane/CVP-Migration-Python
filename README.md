# CVP Migration Automation
### Limits
Some current limits are
- Doesn't handle tenant-level configlets
- Creating containers isn't fully implemented
- Doesn't move devices or apply configlets to devices, only containers

[Ansible Alternative](https://github.com/arista-netdevops-community/cvaas-migration)

## Requirements
`python 3`\
`cpvrac`

### REST API Data from old CVP
- https://[CVP_IP]/cvpservice/provisioning/filterTopology.do?format=topology&startIndex=0&endIndex=0
- https://[CVP_IP]/cvpservice/configlet/getConfigletsAndAssociatedMappers.do

Or using CVP REST API Explorer (Settings > Developer Tools > REST API Explorer)
- Provisioning > `GET` FilterTopology
  - `Filter` = topology
  - `startIndex` = 0
  - `endIndex` = 0
- Configlet > `GET` getConfigletsAndAssociatedMappers

Clicking `Try it out` allows you to execute the request in the browser. While hovering over the `Response body` a download button will show up.

### CVaaS Service Token
A service token will have to be generated for the API calls to CVaaS

Go to `Settings > Access Control > Service Accounts` on CVaaS to generate a token.

## How To
Once you have two API responses and a service token. The service token needs to be set in `main.py` as `cvaas_token`. The API responses (Saved as JSON files) are provided by command line args.

i.e.
`python3 main.py -t filterTopology.json -m getConfigletsAndAssociatedMappers.json`

### `main.py` can be edited to change functionality of the migration.

`IDMap.TopologyIDMap` can have a container name to filter down what "top-level" container will be worked on. More info in the code comments.

`cvaas.update_configs` can have a filter of configlets to not update.

`apply_configlets` will apply configlets to the containers. This will be affected if a filter was used with `IDMap.TopologyIDMap`