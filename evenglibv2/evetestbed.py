#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Configure S-Terra
#
# alexeykr@gmail.com
# coding=utf-8
# import codecs
# Example
# -------
#
#   short script designed to be run with a datafile
#   (notice many expected values/parameters undefined)
import logging
from pyats import aetest
from genie import testbed as tbd
from genie.conf import Genie
import argparse
from pyats.log.utils import banner
import re


class common_setup(aetest.CommonSetup):
    """ Common Setup section """
    @aetest.subsection
    def check_topology_links(self, testscript, testbed):
        dev_links = dict()
        for dev_first in testbed.devices.values():
            dev_links[dev_first.name] = list()
            for dev_sec in testbed.devices.values():
                if dev_first != dev_sec:
                    links = dev_first.find_links(dev_sec)
                    dev_links[dev_first.name].append(links)
        testscript.parameters['dev_links'] = dev_links

    @aetest.subsection
    def establish_connections(self, steps, testscript, testbed):
        """ Common Setup subsection """
        dev_connected = list()
        for dev_name in testbed.devices.values():
            with steps.start(f'Connect to  {dev_name.name}'):
                dev_name.connect(init_exec_commands=[], log_stdout=False)
            dev_connected.append(dev_name)
        testscript.parameters['dev_conn'] = dev_connected


class TestConfEveNG(aetest.Testcase):

    @aetest.setup
    def collects_ip_ping(self, testbed, testscript, dev_links, dev_conn):
        dev_dest_ip = dict()
        for name in dev_links:
            dev_dest_ip[name] = list()
            for rt in testbed.custom.postcommands[name]:
                if re.search('ip\s*route', rt):
                    routes = rt.split()[4]
                    dev_dest_ip[name].append(routes)
                    # print(rt.split()[4])
            for links in dev_links[name]:
                for lnk in links:
                    for intf in lnk.interfaces:
                        if str(intf.ipv4.ip) not in dev_dest_ip[name]:
                            dev_dest_ip[name].append(str(intf.ipv4.ip))
        testscript.parameters['dev_dest_ip'] = dev_dest_ip
        aetest.loop.mark(self.ping, dev_router=dev_conn)

    @aetest.test
    def ping(self, steps, testbed, dev_dest_ip, dev_router, ):
        for dst in dev_dest_ip[dev_router.name]:
            with steps.start(f'Ping from {dev_router.name} to IP: {dst}'):
                try:
                    result = dev_router.ping(dst)
                except Exception as e:
                    self.failed('Ping {} from device {} failed with error: {}'.format(
                        dst,
                        dev_router.name,
                        str(e)
                    ))
                else:
                    match = re.search(r'Success rate is (?P<rate>\d+) percent', result)
                    success_rate = match.group('rate')
                    logger.info(banner('Ping {} with success rate of {}%'.format(
                        dst,
                        success_rate,
                    )
                    )
                    )


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed_file', type=str, default='')
    args = parser.parse_args()
    aetest.main(testbed=Genie.init(args.testbed_file))
