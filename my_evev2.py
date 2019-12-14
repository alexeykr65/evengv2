#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Configure S-Terra
#
# alexeykr@gmail.com
# coding=utf-8
# import codecs
import os
import evenglibv2.evenglibv2 as evng
#import evenglibv2.evetestbed


# from pyats import aetest


unl_file = "lab_testbed"
eve_ng_ip_host = "10.121.1.21"
eve_ng_ssh_username = "root"
eve_ng_ssh_password = "cisco"
config_file = "my_eveng.cfg"
ip_mgm_gw = "10.80.1.0 255.255.255.0 10.122.1.1"


def testbed():
    # testbed_file = "./testbed_eveng.yaml"
    # aetest.main(testbed=Genie.init(testbed_file))
    # test_path = os.path.dirname(os.path.abspath(__file__))
    # testscript = os.path.join(test_path, 'evenglibv2/evetestbed.py')
    tbd = evng.TestbedConf('testbed_eveng.yaml')
    tbd.run_testbed()

    # testbed_file = "./testbed_eveng.yaml"
    # aetest.main(testbed=Genie.init(testbed_file))

    # testscript = 'evetestbed.py'
    # # run it
    # run(testscript)
    print("test")


def main():
    # logging_file = "eveng-configure.log"
    ev = evng.EveNgLab(unl_file=unl_file, eve_ip_host=eve_ng_ip_host, eve_ssh_username=eve_ng_ssh_username, eve_ssh_password=eve_ng_ssh_password, file_config=config_file)
    # ret =
    ev.get_remote_unl_file()
    # for unl in ret:
    #     print(ret[unl])
    ev.load_config_yaml("nod_network.yml")
    ev.get_proc_param()
    # for unl in ret:
    #     print(ret[unl])
    ev.create_tbd_file('testbed_eveng.yaml')
    ev.create_ansible_file()
    tbd = evng.TestbedConf('testbed_eveng.yaml')
    tbd.execute_testbed()


if __name__ == '__main__':
    # main()
    testbed()
