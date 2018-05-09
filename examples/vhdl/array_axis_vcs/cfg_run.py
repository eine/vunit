# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2018, Lars Asplund lars.anders.asplund@gmail.com

from os.path import join, dirname
from vunit import VUnit
import json


# Load configuration from file
cfg = json.loads(open('config.json', 'r').read())


# Set root path
try:
    root = cfg["root"]
except:
    root = dirname(__file__)


# Create VUnit instance
vu = VUnit.from_argv()


# Load addons/modules
try:
    for a in cfg["add"]:
        getattr(vu, "add_"+a)()
except Exception as e:
    pass


# Set libraries and source files
try:
    for l in cfg["libs"]:
        lib = vu.add_library(l)
        for p in cfg["libs"][l]:
            try:
                if p[0] == '/':
                    lib.add_source_files(p)
                else:
                    lib.add_source_files(join(root, p))
            except:
                pass
except:
    pass


# Set testbench configuration (encoded generics)
try:
    tb_cfg = dict()
    for c in cfg["tb_cfg"]:
        try:
            tb_cfg[c] = cfg["tb_cfg"][c];
        except:
            pass
    vu.set_generic("tb_cfg", ", ".join(["%s:%s" % (key, str(tb_cfg[key])) for key in tb_cfg]) )
except:
    pass


#vu.set_sim_option('modelsim.init_files.after_load',['runall_addwave.do'])


vu.main()
