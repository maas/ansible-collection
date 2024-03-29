# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..module_utils import errors
from ..module_utils.client import Client
from ..module_utils.partition import Partition
from ..module_utils.rest_client import RestClient
from ..module_utils.utils import MaasValueMapper, get_query


class BlockDevice(MaasValueMapper):
    def __init__(
        self,
        name=None,
        id=None,
        machine_id=None,
        model=None,
        serial=None,
        id_path=None,
        block_size=None,
        size=None,
        tags=None,
        partitions=None,
    ):
        self.name = name
        self.id = id
        self.machine_id = machine_id
        self.model = model
        self.serial = serial
        self.id_path = id_path
        self.block_size = block_size
        self.size = size
        self.tags = tags
        self.partitions = partitions

    @classmethod
    def get_by_name(
        cls,
        module,
        client: Client,
        machine_id,
        must_exist=False,
        name_field_ansible="name",
    ):
        rest_client = RestClient(client=client)
        query = get_query(
            module,
            name_field_ansible,
            ansible_maas_map={name_field_ansible: "name"},
        )
        block_device_maas_dict = rest_client.get_record(
            f"/api/2.0/nodes/{machine_id}/blockdevices/",
            query,
            must_exist=must_exist,
        )
        if block_device_maas_dict:
            block_device = cls.from_maas(block_device_maas_dict)
            return block_device

    @classmethod
    def get_by_id(cls, id, client: Client, machine_id, must_exist=False):
        response = client.get(
            f"/api/2.0/nodes/{machine_id}/blockdevices/{id}/"
        )
        if response.status == 404:
            if must_exist:
                raise errors.BlockDeviceNotFound(id)
            return None
        block_device_maas_dict = response.json
        block_device = cls.from_maas(block_device_maas_dict)
        return block_device

    @classmethod
    def from_ansible(cls, module):
        return

    @classmethod
    def from_maas(cls, maas_dict):
        obj = cls()
        try:
            obj.name = maas_dict["name"]
            obj.id = maas_dict["id"]
            obj.machine_id = maas_dict["system_id"]
            obj.model = maas_dict["model"]
            obj.serial = maas_dict["serial"]
            obj.id_path = maas_dict["id_path"]
            obj.block_size = maas_dict["block_size"]
            obj.size = maas_dict["size"]
            obj.tags = maas_dict["tags"]
            obj.partitions = [
                Partition.from_maas(partition)
                for partition in maas_dict["partitions"] or []
            ]
        except KeyError as e:
            raise errors.MissingValueMAAS(e)
        return obj

    def to_maas(self):
        return

    def to_ansible(self):
        return

    def delete(self, client):
        client.delete(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/"
        )

    def get(self, client):
        return client.get(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/"
        ).json

    def update(self, client, payload):
        return client.put(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/",
            data=payload,
        ).json

    def add_tag(self, client, tag):
        return client.post(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/",
            query={"op": "add_tag"},
            data=dict(tag=tag),
        ).json

    def remove_tag(self, client, tag):
        return client.post(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/",
            query={"op": "remove_tag"},
            data=dict(tag=tag),
        ).json

    def mount(self, client, payload):
        return client.post(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/",
            query={"op": "mount"},
            data=payload,
        ).json

    def unmount(self, client):
        return client.post(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/",
            query={"op": "unmount"},
            data={},
        ).json

    def format(self, client, payload):
        return client.post(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/",
            query={"op": "format"},
            data=payload,
        ).json

    def unformat(self, client):
        return client.post(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/",
            query={"op": "unformat"},
            data={},
        ).json

    def set_boot_disk(self, client):
        return client.post(
            f"/api/2.0/nodes/{self.machine_id}/blockdevices/{self.id}/",
            query={"op": "set_boot_disk"},
            data={},
        )  # Response is OK

    @classmethod
    def create(cls, client, machine_id, payload):
        block_device_maas_dict = client.post(
            f"/api/2.0/nodes/{machine_id}/blockdevices/",
            data=payload,
            timeout=60,  # Sometimes we get timeout error thus changing timeout from 20s to 60s
        ).json
        block_device = cls.from_maas(block_device_maas_dict)
        return block_device

    def __eq__(self, other):
        """One block device is equal to another if it has all attributes exactly the same"""
        return all(
            (
                self.name == other.name,
                self.id == other.id,
                self.machine_id == other.machine_id,
                self.model == other.model,
                self.serial == other.serial,
                self.id_path == other.id_path,
                self.block_size == other.block_size,
                self.size == other.size,
                self.tags == other.tags,
            )
        )
