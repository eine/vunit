# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2019, Lars Asplund lars.anders.asplund@gmail.com

"""
Helper functions to get/generate sources for the documentation
"""

from __future__ import print_function

import sys
import json
import inspect
from os.path import basename, dirname, isabs, isdir, isfile, join
from os import environ, listdir, popen, mkdir, remove
from shutil import copyfile


ROOT = join(dirname(__file__), '..', 'docs')


def get_theme(url, strip=None, tarfilter=None):
    """
    Check if the theme is available locally, retrieve it with curl otherwise
    """
    if not isdir(join(ROOT, '_theme')) or not isfile(join(ROOT, '_theme', 'theme.conf')):
        if not isdir(join(ROOT, '_theme')):
            mkdir(join(ROOT, '_theme'))
        if not isfile(join(ROOT, 'theme.tgz')):
            print(popen(' '.join([
                'curl',
                '-fsSL',
                url,
                '-o', join(ROOT, 'theme.tgz')
            ])).read())
        tar_cmd = [
            'tar',
            '-C',
            join(ROOT, '_theme'),
            '-xvzf',
            join(ROOT, 'theme.tgz')
        ]

        if tarfilter:
            tar_cmd += [tarfilter]
        if strip:
            tar_cmd += ['--strip-component', str(strip)]
        print(popen(' '.join(tar_cmd)).read())


def copy_common():
    """
    Copy RST sources used outside 'docs' into 'docs' and fix paths accordingly
    """
    copyfile(join(ROOT, '..', 'README.rst'), join(ROOT, 'readme.rst'))
    print(popen(' '.join([
        'sed',
        '-i',
        '"s#\./docs/_static/img/#_static/img/#g"',
        join(ROOT, 'readme.rst')
    ])).read())

    copyfile(join(ROOT, '..', 'LICENSE.rst'), join(ROOT, 'license.rst'))


def custom_last(user, repo, cidomain='travis-ci.org'):
    """
    Build a custom 'Last updated on' field with CI info
    """
    custom = {'last': None, 'pre': None}
    try:
        slug = user + '/' + repo
        commit = environ['TRAVIS_COMMIT']
        custom['pre'] = 'Last updated on '
        custom['last'] = ''.join([
            '[',
            '<a href="https://github.com/', slug, '/commit/', commit, '">', commit[0:8], '</a>',
            ' - ',
            '<a href="https://', cidomain, '/', slug, '/builds/', environ['TRAVIS_BUILD_ID'], '">',
            environ['TRAVIS_BUILD_NUMBER'], '</a>',
            '.',
            '<a href="https://', cidomain, '/', slug, '/jobs/', environ['TRAVIS_JOB_ID'], '">',
            environ['TRAVIS_JOB_NUMBER'].split('.')[1], '</a>',
            ']',
        ])
    except KeyError as err:
        print('Could not retrieve CI build info: envvar', err, 'not found.')

    context = {}
    if custom['pre']:
        context['custom_last_pre'] = custom['pre']
    if custom['last']:
        context['custom_last'] = custom['last']

    if context:
        with open(join(ROOT, 'context.json'), 'w') as fptr:
            json.dump(context, fptr)


def examples():
    """
    Traverses the examples directory and generates examples.rst with the docstrings
    """
    eg_path = join(ROOT, '..', 'examples')
    egs_fptr = open(join(ROOT, 'examples.rst'), "w+")
    egs_fptr.write('\n'.join([
        '.. _examples:\n',
        'Examples',
        '========',
        '\n'
    ]))
    for language, subdir in {'VHDL': 'vhdl', 'SystemVerilog': 'verilog'}.items():
        egs_fptr.write('\n'.join([
            language,
            '~~~~~~~~~~~~~~~~~~~~~~~',
            '\n'
        ]))
        for item in listdir(join(eg_path, subdir)):
            loc = join(eg_path, subdir, item)
            if isdir(loc):
                _data = _get_eg_doc(
                    loc,
                    'https://github.com/VUnit/vunit/tree/master/examples/%s/%s' % (subdir, item)
                )
                if _data:
                    egs_fptr.write(_data)


def _get_eg_doc(location, ref):
    """
    Reads the docstring from a run.py file and rewrites the title to make it a ref
    """
    if not isfile(join(location, 'run.py')):
        print(
            "WARNING: Example subdir '"
            + basename(location)
            + "' does not contain a 'run.py' file. Skipping...")
        return None

    print("Generating '_main.py' from 'run.py' in '" + basename(location) + "'...")
    with open(join(location, 'run.py'), 'r') as ifile:
        with open(join(location, '_main.py'), 'w') as ofile:
            ofile.writelines(['def _main():\n'])
            ofile.writelines([''.join(['    ', x]) for x in ifile])

    print("Extracting docs from '" + basename(location) + "'...")
    sys.path.append(location)
    from _main import _main  # pylint: disable=import-error
    eg_doc = inspect.getdoc(_main)
    del sys.modules['_main']
    sys.path.remove(location)

    remove(join(location, '_main.py'))

    if not eg_doc:
        print(
            "WARNING: 'run.py' file in example subdir '"
            + basename(location)
            + "' does not contain a docstring. Skipping..."
        )
        return ''

    title = '`%s <%s/>`_' % (eg_doc.split('---', 1)[0][0:-1], ref)
    return '\n'.join([
        title,
        '-' * len(title),
        eg_doc.split('---\n', 1)[1],
        '\n'
    ])


def _read_vcs_cfg(location=None):
    """
    Read list of known third-party VC libraries/repositories
    """
    root = join(dirname(__file__), '..', 'vunit', 'vhdl', 'verification_components')
    cfg = {'third_party': location or join(dirname(__file__), '..', '..')}
    cfg.update(json.loads(open(join(root, 'vc_list.json')).read()))
    return cfg


def third_party_vcs(location=None):
    """
    Extract content from third-party VCs (generates examples.rst and third_party.rst)
    """
    cfg = _read_vcs_cfg(location=location)
    vc_list = [item for item in cfg]
    vc_list.remove('third_party')

    doc_list = {}
    doc_egs = join(ROOT, 'examples.rst')
    egs_fptr = open(doc_egs, "a+")
    egs_fptr.write('\n'.join([
        'Verification Components',
        '~~~~~~~~~~~~~~~~~~~~~~~',
        '\n'
    ]))

    # WIP
    vc_list = ['AXI', 'UART']

    for key in vc_list:
        if key not in cfg:
            print('VC <' + key + '> not defined. Please add it to the configuration first.')
            exit(1)
        else:
            item = cfg[key]
            loc = item['path'] if isabs(item['path']) else join(cfg['third_party'], item['path'])
            if not isdir(loc):
                print('VC <%s> not available. Please install it to %s' % (key, loc))
                exit(1)

            vc_cfg_file = join(loc, 'vunit_cfg.json')
            if not isfile(vc_cfg_file):
                print('File <' + vc_cfg_file + '> not found.')
                exit(1)
            vc_cfg = json.loads(open(vc_cfg_file).read())

            doc_list[key] = vc_cfg['provides']

            egs = join(loc, 'examples')
            if isdir(egs):
                for item in listdir(egs):
                    if isdir(join(egs, item)):
                        egs_fptr.write(_get_eg_doc(
                            join(egs, item),
                            '%s/tree/master/examples/%s' % (cfg[key]['remote'], item)
                        ))
    vc_rst = []
    for key, val in doc_list.items():
        vc_rst += ['- `%s <%s>`_\n' % (key, cfg[key]['remote'])]
        for item in val:
            vc_rst += ['  - %s' % item]
    open(join(ROOT, 'verification_components', 'third_party.rst'), "w+").write('\n'.join(vc_rst))


if __name__ == '__main__':
    examples()
    third_party_vcs('/src')
