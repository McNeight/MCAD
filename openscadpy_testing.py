import py
import os

from openscadpy_utils import *


temppath = py.test.ensuretemp('MCADpy')

def pytest_generate_tests(metafunc):
    if "modpath" in metafunc.funcargnames:
        for fpath, modnames in collect_test_modules().items():
            if "modname" in metafunc.funcargnames:
                for modname in modnames:
                    metafunc.addcall(funcargs=dict(modname=modname, modpath=fpath))
            else:
                metafunc.addcall(funcargs=dict(modpath=fpath))


def test_module_compile(modname, modpath):
    tempname = modpath.basename + '_' + modname + '.py'
    fpath = temppath.join(tempname)
    stlpath = temppath.join(tempname + ".stl")
    f = fpath.open('w')
    code = """
# generated testfile
import sys
sys.path.append('%s')
from %s import %s

openscad.assemble(%s())
""" % (os.getcwd(), modpath.basename[:-3], modname, modname)
    print code
    f.write(code)
    f.flush()
    output = call_openscad(path=fpath, stlpath=stlpath, timeout=35)
    print output
    assert output[0] is 0
    for s in ("warning", "error"):
        assert s not in output[2].strip().lower()
    assert len(stlpath.readlines()) > 2
