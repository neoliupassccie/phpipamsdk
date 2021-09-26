#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# Copyright (c) 2021 neo. All rights reserved.
"""
@Email: 445654045@qq.com
@project: phpipamsdk
@file: ip_require.py
@time: 7/25/21 10:35 PM
"""

import warnings
import phpipamsdk


'''
环境-上联交换机-上联交换机端口-端口对应装机网段-网段对应的subnet_id-获取第一个空闲地址
'''
DIR_AREA = {}


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    IPAM = phpipamsdk.PhpIpamApi()
    IPAM.login()

    # section_api = phpipamsdk.SectionsApi(phpipam=IPAM)
    # res1 = section_api.list_sections()
    # res1 = section_api.list_section_subnets(section_id='10')
    # print(res1)
    # if res1['code'] == 200 and res1['success'] is True:
    #     print(len(res1['data']))
    #     for section_item in res1['data']:
    #         print(section_item)
        # print('='*100)
        # res1_1 = [i for i in res1['data'] if i['masterSubnetId'] == '0']
        # print(len(res1_1))
        # print(res1_1)

        # print('='*100)
        # res1_1 = [i for i in res1['data'] if i['description'] == 'Connect_IPPool_NETWORK']
        # if len(res1_1) == 1:
        #     print(res1_1[0])
        # else:
        #     print('there are more than one ippool named Connect_IPPool_NETWORK!')

    subnets_api = phpipamsdk.SubnetsApi(phpipam=IPAM)
    # res1 = subnets_api.get_subnets_index()
    # print(res1)
    # if res1['code'] == 200 and res1['success'] is True:
    #     print(len(res1['data']))
    #     for i in res1['data']:
    #         print('{0}'.format(i))
    # res1 = subnets_api.get_subnet(subnet_id='10')
    # print(res1)
    # if res1['code'] == 200 and res1['success'] is True:
    #     print(len(res1['data']))
    #     for k,v in res1['data'].items():
    #         print('{0}:{1}'.format(k,v))

    # res2 = subnets_api.get_subnet(subnet_id='77')
    res2 = subnets_api.get_subnet_usage(subnet_id='506')
    # res2 = subnets_api.get_subnet_first_free_subnet(subnet_id='77', mask='30')
    # res2 = subnets_api.add_subnet_first_free(subnet_id='77', mask='30',description='add_subnet_first_free')
    # res2 = subnets_api.add_subnet(subnet='10.10.128.88', mask='30',section_id='13',master_subnet_id='77',description='ttest')
    print(res2)

    # address_api = phpipamsdk.AddressesApi(phpipam=IPAM)
    # res3 = address_api.get_address(address_id='221')
    # res3 = address_api.search_address(address='10.10.128.101')
    # res3 = address_api.list_address_tags()
    # res3 = address_api.get_address_tag(tag_id='3')
    # res3 = address_api.list_addresses_tag(tag_id='3')
    # res3 = address_api.add_address_first_free(subnet_id='103',description='add_address_first_free')
    # print(res3)
    # res4 = address_api.del_address(address_id='221')
    # res4 = address_api.del_address_subnet(address='10.10.128.101', subnet_id='103')
    # print(res4)






