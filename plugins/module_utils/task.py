# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

from time import sleep

from ..module_utils.rest_client import RestClient
from ..module_utils.state import TaskState


class Task:
    @classmethod
    def wait_task(cls, client, device, check_mode=False):
        if check_mode:
            return
        while True:
            task_status = Task.get_task_status(client, device, id)
            if not task_status:  # No such task_status is found
                break
            if (
                task_status.get("status_name", "") == TaskState.ready
            ):  # Task has finished
                break
            # TODO: Add other states like Error or not complete etc...
            sleep(1)

    @staticmethod
    def get_task_status(client, device, id):
        rest_client = RestClient(client=client)
        endpoint = ""
        if device == "host":
            endpoint = f"/api/2.0/machines/{id}/"
        elif device == "machine":
            endpoint = f"/api/2.0/vm-hosts/{id}/"
        # TODO: Add other endpoints
        task_status = rest_client.get_record(endpoint)
        return task_status if task_status else {}
