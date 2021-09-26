#!/usr/bin/env python
""" Example """

import warnings
import phpipamsdk

from phpipamsdk.utils import get_section_id
from phpipamsdk.utils import get_device_id
from phpipamsdk.utils import get_tools_rack_id
from phpipamsdk.utils import get_tools_location_id


def del_section(ipam=None, name=None):
    """ Use API to delete a section """
    sections_api = phpipamsdk.SectionsApi(phpipam=ipam)

    sect_id = get_section_id(ipam=ipam, name=name)

    res = sections_api.del_section(section_id=sect_id)
    print(res)


def del_location(ipam=None, name=None):
    """ Use API to delete a location """
    locations_api = phpipamsdk.ToolsLocationsApi(phpipam=ipam)

    location_id = get_tools_location_id(ipam=ipam, name=name)

    res = locations_api.del_tools_location(location_id=location_id)
    print(res)


def del_rack(ipam=None, name=None):
    """ Use API to delete a rack """
    racks_api = phpipamsdk.ToolsRacksApi(phpipam=ipam)

    rack_id = get_tools_rack_id(ipam=ipam, name=name)

    res = racks_api.del_tools_rack(rack_id=rack_id)
    print(res)


def del_device(ipam=None, name=None):
    """ Use API to delete a device """
    devices_api = phpipamsdk.DevicesApi(phpipam=ipam)

    device_id = get_device_id(ipam=ipam, name=name)

    res = devices_api.del_device(device_id=device_id)
    print(res)


if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    # IPAM = phpipamsdk.PhpIpamApi(
    #     api_uri='http://127.0.0.1/api/admin/', api_verify_ssl=False)
    # IPAM.login(auth=('admin', 'root@123'))
    IPAM = phpipamsdk.PhpIpamApi()
    IPAM.login()

    # Delete the Devices

    del_device(ipam=IPAM, name='border-leaf1.dc2')
    del_device(ipam=IPAM, name='border-leaf2.dc2')
    del_device(ipam=IPAM, name='spine1.dc2')
    del_device(ipam=IPAM, name='leaf1.dc2')
    del_device(ipam=IPAM, name='spine2.dc2')
    del_device(ipam=IPAM, name='leaf2.dc2')
    del_device(ipam=IPAM, name='spine3.dc2')
    del_device(ipam=IPAM, name='leaf3.dc2')
    del_device(ipam=IPAM, name='leaf4.dc2')

    # Delete the Racks

    del_rack(ipam=IPAM, name='R06')
    del_rack(ipam=IPAM, name='R05')
    del_rack(ipam=IPAM, name='R04')
    del_rack(ipam=IPAM, name='R03')
    del_rack(ipam=IPAM, name='R02')
    del_rack(ipam=IPAM, name='R01')

    # Delete the Location

    del_location(ipam=IPAM, name='equinix_dcxxx')

    # Delete the section along with all subnets contained within

    del_section(ipam=IPAM, name='ip_fabric_two3')

    IPAM.logout()
