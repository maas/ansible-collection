# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class MaasError(Exception):
    pass


class AuthError(MaasError):
    pass


class UnexpectedAPIResponse(MaasError):
    def __init__(self, response):
        self.message = "Unexpected response - {0} {1}".format(
            response.status, response.data
        )
        super(UnexpectedAPIResponse, self).__init__(self.message)


class InvalidUuidFormatError(MaasError):
    def __init__(self, data):
        self.message = "Invalid UUID - {0}".format(data)
        super(InvalidUuidFormatError, self).__init__(self.message)


# In-case function parameter is optional but required
class MissingFunctionParameter(MaasError):
    def __init__(self, data):
        self.message = "Missing parameter - {0}".format(data)
        super(MissingFunctionParameter, self).__init__(self.message)


# In-case argument spec doesn't catch exception
class MissingValueAnsible(MaasError):
    def __init__(self, data):
        self.message = "Missing value - {0}".format(data)
        super(MissingValueAnsible, self).__init__(self.message)


# In-case MAAS API value is missing
class MissingValueMAAS(MaasError):
    def __init__(self, data):
        self.message = "Missing value from MAAS API - {0}".format(data)
        super(MissingValueMAAS, self).__init__(self.message)


class DeviceNotUnique(MaasError):
    def __init__(self, data):
        self.message = "Device is not unique - {0} - already exists".format(
            data
        )
        super(DeviceNotUnique, self).__init__(self.message)


class MachineNotFound(MaasError):
    def __init__(self, data):
        self.message = "Virtual machine - {0} - not found".format(data)
        super(MachineNotFound, self).__init__(self.message)


class ClusterConnectionNotFound(MaasError):
    def __init__(self, data):
        self.message = "No cluster connection found - {0}".format(data)
        super(ClusterConnectionNotFound, self).__init__(self.message)


class VlanNotFound(MaasError):
    def __init__(self, data):
        self.message = "VLAN - {0} - not found".format(data)
        super(VlanNotFound, self).__init__(self.message)


class BlockDeviceNotFound(MaasError):
    def __init__(self, data):
        self.message = "Block device - {0} - not found".format(data)
        super(BlockDeviceNotFound, self).__init__(self.message)


class PartitionNotFound(MaasError):
    def __init__(self, data):
        self.message = "Partition - {0} - not found".format(data)
        super(PartitionNotFound, self).__init__(self.message)
