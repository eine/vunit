# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2018, Lars Asplund lars.anders.asplund@gmail.com

from os.path import join, dirname
from vunit import VUnit

root = dirname(__file__)

ui = VUnit.from_argv()
ui.add_random()
ui.add_verification_components()
lib = ui.library("vunit_lib")
lib.add_source_files(join(root, "test", "*.vhd"))


def encode(tb_cfg):
    return ",".join(["%s:%s" % (key, str(tb_cfg[key])) for key in tb_cfg])


def gen_avalon_tests(obj, *args):
    for data_width, num_cycles, readdatavalid_prob, waitrequest_prob, in product(*args):
        tb_cfg = dict(
            data_width=data_width,
            readdatavalid_prob=readdatavalid_prob,
            waitrequest_prob=waitrequest_prob,
            num_cycles=num_cycles)
        config_name = encode(tb_cfg)
        obj.add_config(name=config_name,
                       generics=dict(encoded_tb_cfg=encode(tb_cfg)))


tb_avalon_slave = lib.test_bench("tb_avalon_slave")

for test in tb_avalon_slave.get_tests():
    gen_avalon_tests(test, [32], [1, 2, 64], [1.0, 0.3], [0.0, 0.4])


ui.main()
