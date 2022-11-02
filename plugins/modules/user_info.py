#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
module: user_info

author:
  - Domen Dobnikar (@domen_dobnikar)
short_description: 
description: 
version_added: 1.0.0
extends_documentation_fragment:
  - canonical.maas.cluster_instance
seealso: []
options:
  name:
    description:
      - The user name.
      - Identifier-style username for the user.
    type: str
"""

EXAMPLES = r"""
"""

RETURN = r"""
record:
"""

from ansible.module_utils.basic import AnsibleModule


from ..module_utils import arguments, errors
from ..module_utils.cluster_instance import get_oauth1_client



def run(module, client):
    if module.params["name"]:
      response = client.get(f"/api/2.0/users/{module.params['name']}/")
    else:
      response = client.get("/api/2.0/users/")
    return response.json


def main():
    module = AnsibleModule(
        supports_check_mode=False,
        argument_spec=dict(
            arguments.get_spec("cluster_instance"),
            name=dict(
                type="str",
            ),
        ),
    )

    try:
        client = get_oauth1_client(module.params)
        record = run(module, client)
        module.exit_json(changed=False, record=record)
    except errors.MaasError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
