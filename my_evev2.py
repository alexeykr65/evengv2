#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Example script for initialize EVE-NG
#
# alexeykr@gmail.com
# coding=utf-8
# import codecs
import evenglibv2.evenglibv2 as evng


unl_file = "lab_testbed"
eve_ng_ip_host = "10.121.1.21"
eve_ng_ssh_username = "root"
eve_ng_ssh_password = "cisco"
testbed_file = "testbed_eveng.yaml"
conf_int_lab = "nod_network.yml"


def main():
    ev = evng.EveNgLab(unl_file=unl_file, eve_ip_host=eve_ng_ip_host, eve_ssh_username=eve_ng_ssh_username, eve_ssh_password=eve_ng_ssh_password)
    # ev.get_remote_unl_file()
    # ev.load_config_yaml(conf_int_lab)
    # ev.get_proc_param()
    # ev.create_tbd_file(testbed_file)
    # ev.create_ansible_file()
    tbd = evng.TestbedConf(testbed_file)
    tbd.execute_testbed()
    tbd.run_testbed()


if __name__ == '__main__':
    main()
