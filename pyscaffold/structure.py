# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import os
import copy
from datetime import date
from string import Template
from os.path import join as join_path

from six import string_types

import pyscaffold
from . import info
from . import utils
from . import templates

__author__ = "Florian Wilhelm"
__copyright__ = "Blue Yonder"
__license__ = "new BSD"


def set_default_args(args):
    args = copy.copy(args)
    utils.safe_set(args, "author", info.username())
    utils.safe_set(args, "email", info.email())
    utils.safe_set(args, "year", date.today().year)
    utils.safe_set(args, "license", "new BSD")
    utils.safe_set(args, "version", pyscaffold.__version__)
    utils.safe_set(args, "title", "="*len(args.project) + '\n' +
                                  args.project + '\n' +
                                  "="*len(args.project))
    return args


def make_structure(args):
    args = set_default_args(args)
    struct = {args.project: {
        ".gitignore": templates.gitignore(args),
         args.package: {"__init__.py": templates.init(args),
                        "_version.py": templates.version(args)},
         "tests": {"__init__.py": ""},
         "docs": {"conf.py": templates.sphinx_conf(args),
                  "index.rst": templates.sphinx_index(args),
                  "Makefile": templates.sphinx_makefile(args),
                  "_static": {
                      ".gitignore": templates.gitignore_all(args)}},
         "README.rst": templates.readme(args),
         "AUTHORS.rst": templates.authors(args),
         "MANIFEST.in": templates.manifest_in(args),
         "COPYING": templates.copying(args),
         "setup.py": templates.setup(args),
         "versioneer.py": templates.versioneer(args),
         "requirements.txt": templates.requirements(args),
         ".coveragerc": templates.coveragerc(args)}}
    return struct


def create_structure(struct, prefix=None, update=False):
    if prefix is None:
        prefix = os.getcwd()
    for name, content in struct.items():
        if isinstance(content, string_types):
            with open(join_path(prefix, name), "w") as fh:
                fh.write(content)
        elif isinstance(content, dict):
            try:
                os.mkdir(join_path(prefix, name))
            except OSError:
                if not update:
                    raise
            create_structure(struct[name],
                             prefix=join_path(prefix, name),
                             update=update)
        else:
            raise RuntimeError("Don't know what to do with content type "
                               "{type}.".format(type=type(content)))
