#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import socket
from prettytable import PrettyTable
reload(sys)
sys.setdefaultencoding('utf8')


def check_isp(ip):
    url = "http://ip-api.com/json/{}?lang=zh-CN".format(ip)
    try:
        res = requests.get(url, timeout=3)
        r_json = res.json()
        return r_json.get('isp', '')
    except Exception:
        return ''

def splice_message(l):
    msg = ""
    for k, v in enumerate(l):
        isp = check_isp(v)
        if k % 2 != 0:
            msg = msg + "\n" + isp
        else:
            msg = msg + isp
    return msg

def splice_ip(l):
    msg = ""
    for k, v in enumerate(l):
        if k % 2 != 0:
            msg = msg + "\n" + v
        else:
            msg = msg + v
    return msg

def split_domain(domain, pre=''):
    domain_list = domain.split('.')
    primary_domain = '.'.join([domain_list[-2], domain_list[-1]])
    if pre:
        domain = "{}.{}".format(pre, primary_domain.strip())
    else:
        domain = primary_domain.strip()
    return domain

def check_domain(domain):
    ip_list = []
    try:
        addrs = socket.getaddrinfo(domain, None)
        for item in addrs:
            if item[4][0] not in ip_list:
                ip_list.append(item[4][0])
    except Exception as e:
        pass
    return ip_list

def main(path):
    table = PrettyTable(['域名','IP', 'ISP', '主域名', '主IP',  '主ISP'])
    with open(path, 'r') as f:
        for i in f.readlines():
            p_domain = split_domain(i.strip())
            p_ip_list = check_domain(p_domain)
            d_ip_list = check_domain(i.strip())
            p_ip = splice_ip(p_ip_list)
            d_ip = splice_ip(d_ip_list)
            isp_msg = splice_message(d_ip_list)
            z_isp_msg = splice_message(p_ip_list)
            table.add_row([i.strip(), d_ip, isp_msg, p_domain, p_ip, z_isp_msg])
    print(table)


if __name__ == "__main__":
    fname = sys.argv[1]
    main(fname)
