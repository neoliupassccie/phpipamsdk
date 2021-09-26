#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# Copyright (c) 2021 neo. All rights reserved.
"""
@Email: 445654045@qq.com
@project: phpipamsdk
@file: apply_connect_subnet.py
@time: 9/24/21 2:45 PM
"""

import warnings
import phpipamsdk
import json


class IpdbInit:
    def __init__(self):
        self.ipam = self.login()

    def login(self):
        warnings.filterwarnings('ignore')
        IPAM = phpipamsdk.PhpIpamApi()
        IPAM.login()
        return IPAM

    def logout(self):
        self.ipam.logout()


class IpdbConnect(IpdbInit):
    def __init__(self):
        super().__init__()
        self.section_api = phpipamsdk.SectionsApi(phpipam=self.ipam)
        self.subnets_api = phpipamsdk.SubnetsApi(phpipam=self.ipam)
        self.address_api = phpipamsdk.AddressesApi(phpipam=self.ipam)

    def get_sections_list(self):
        res = self.section_api.list_sections()
        return res

    def get_subnet_id(self, section_id=''):
        res1 = self.section_api.list_section_subnets(section_id=section_id)
        return res1

    def get_subnet_id_via_tag(self, res1=dict(), tag='Connect_IPPool_NETWORK'):
        if res1['code'] == 200 and res1['success'] is True:
            res1_1 = [i for i in res1['data'] if tag in str(i['description'])]
            if len(res1_1) == 1:
                return res1_1[0]
            else:
                return 'there are more than one ippool named {0}!'.format(tag)
        else:
            return 'request missing'

    def apply_one_subnet_from_section(self, section_id='', tag='Connect_IPPool_NETWORK',
                                      subnet_describe='from_api', subnet_mask='30',
                                      gwinit_tag=False):
        res1 = self.get_subnet_id(section_id)
        res2 = self.get_subnet_id_via_tag(res1=res1, tag=tag)
        if res2 is not None and isinstance(res2, dict):
            master_subnet_id = res2['id']
            res_master_subnet_usage = self.subnets_api.get_subnet_usage(subnet_id=master_subnet_id)
            if res_master_subnet_usage['code'] == 200 and res_master_subnet_usage['success'] is True:
                if res_master_subnet_usage['data']['freehosts_percent'] > 10:
                    res_apply_subnets = self.subnets_api.get_subnet_first_free_subnet(subnet_id=master_subnet_id,
                                                                                      mask=subnet_mask)
                    if res_apply_subnets['code'] == 200 and res_apply_subnets['success'] is True:
                        try:
                            _list_net_mask = str(res_apply_subnets['data']).split('/')
                            if len(_list_net_mask) == 2:
                                res3_2 = self.subnets_api.add_subnet(subnet=_list_net_mask[0], mask=_list_net_mask[1],
                                                                     section_id=section_id,
                                                                     master_subnet_id=master_subnet_id,
                                                                     description=subnet_describe)
                                if gwinit_tag:
                                    res3_3 = self.apply_gateway(subnet_id=res3_2['id'])
                                    res3_2['gatewayInfo'] = res3_3
                                    return res3_2
                                else:
                                    return res3_2
                        except:
                            return '_list_net_mask split fail'
                else:
                    return 'freehosts_percent of the ip pool is less than 10%'
            else:
                return 'request missing'

    def apply_many_subnets_from_section(self, count=1, section_id='',
                                        tag='Connect_IPPool_NETWORK', subnet_describe='from_api'):
        all_res = []
        total_time = 0
        for i in range(count):
            _res = self.apply_one_subnet_from_section(section_id=section_id, tag=tag, subnet_describe=subnet_describe)
            all_res.append(_res)
            total_time += float(_res['time'])
            if _res['code'] == 201 and _res['success'] is True:
                continue
            else:
                return {'code': 500, 'success': False, 'data': all_res, 'total_time': round(total_time, 3)}
        return {'code': 201, 'success': True, 'data': all_res, 'total_time': round(total_time, 3)}

    def recycle_subnet(self, subnet_id=''):
        res = self.subnets_api.del_subnet(subnet_id=subnet_id)
        return res

    def get_subnet_id_via_name(self, subnetname=''):
        res = self.subnets_api.search_subnets_cidr(subnet_cidr=subnetname)
        return res

    def recycle_subnet_via_name(self, subnetname=''):
        _res = self.get_subnet_id_via_name(subnetname=subnetname)
        if _res['code'] == 200 and _res['success'] is True:
            if len(_res['data']) == 1:
                res = self.recycle_subnet(subnet_id=_res['data'][0]['id'])
                res['subnetname'] = subnetname
                return res
            else:
                return 'subnet named {0} is more than one'.format(subnetname)
        else:
            return 'subnets_api search_subnets_cidr fail'

    def apply_address(self,subnet_id=''):
        _res = self.address_api.add_address_first_free(subnet_id=subnet_id, description='add_address_first_free')
        return res

    def apply_gateway(self,subnet_id=''):
        _res = self.address_api.add_address_first_free(subnet_id=subnet_id, description='add_address_first_free')
        if _res['code'] == 201 and _res['success'] is True:
            _res2 = self.address_api.update_address(address_id=_res['id'], is_gateway=1)
            res = self.get_address_info(address_id=_res['id'])
            return res
        else:
            return 'address_api add_address_first_free fail'

    def apply_many_address(self, count=int(), subnet_id=''):
        all_res = []
        total_time = 0
        for i in range(count):
            _res = self.apply_address(subnet_id=subnet_id)
            all_res.append(_res)
            total_time += float(_res['time'])
            if _res['code'] == 201 and _res['success'] is True:
                continue
            else:
                return {'code': 500, 'success': False, 'data': all_res, 'total_time': round(total_time, 3)}
        return {'code': 201, 'success': True, 'data': all_res, 'total_time': round(total_time, 3)}

    def apply_address_via_name(self,subnetname=''):
        _res = self.get_subnet_id_via_name(subnetname=subnetname)
        if _res['code'] == 200 and _res['success'] is True:
            if len(_res['data']) == 1:
                res = self.apply_address(subnet_id=_res['data'][0]['id'])
                res['subnetname'] = subnetname
                return res
            else:
                return 'subnet named {0} is more than one'.format(subnetname)
        else:
            return 'subnets_api search_subnets_cidr fail'

    def get_address_info(self, address_id=''):
        _res_address = self.address_api.get_address(address_id=address_id)
        _res_mastersubnet = self.subnets_api.get_subnet(subnet_id=_res_address['data']['subnetId'])
        _res_address['subnetInfo'] = _res_mastersubnet['data']
        return _res_address

    def apply_aio_subnet_and_address(self, count=2, section_id=''):
        _res = self.apply_one_subnet_from_section(section_id=section_id)
        if _res['code'] == 201 and _res['success'] is True:
            res = self.apply_many_address(count=count, subnet_id=_res['id'])
            res['subnetInfo'] = self.subnets_api.get_subnet(subnet_id=_res['id'])['data']
            return res
        else:
            return 'apply_one_subnet_from_section fail'


if __name__ == '__main__':
    ipdbsubnet = IpdbConnect()
    # res = ipdbsubnet.get_sections_list()
    # res = ipdbsubnet.apply_one_subnet_from_section(section_id='17')
    # res = ipdbsubnet.apply_one_subnet_from_section(section_id='17', tag='_ROOT_VPC',
    #                                                subnet_describe='MGT', subnet_mask='24')
    res = ipdbsubnet.apply_one_subnet_from_section(section_id='17', tag='_ROOT_VPC',
                                                   subnet_describe='MGT', subnet_mask='24', gwinit_tag=True)
    # res = ipdbsubnet.apply_many_subnets_from_section(count=2, section_id='17')
    # res = ipdbsubnet.recycle_subnet_via_name(subnetname="10.10.128.164/30")
    # res = ipdbsubnet.apply_address(subnet_id='212')
    # res = ipdbsubnet.apply_many_address(count=2, subnet_id='206')
    # res = ipdbsubnet.apply_address_via_name(subnetname='10.10.128.140/30')
    # res = ipdbsubnet.get_address_info(address_id='403')
    # res = ipdbsubnet.apply_aio_subnet_and_address(section_id='17')
    # res = ipdbsubnet.apply_gateway(subnet_id='212')
    # res = ipdbsubnet.address_api.del_address(address_id='')
    print(json.dumps(res))
    ipdbsubnet.logout()
