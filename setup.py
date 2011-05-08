import glob
import os
#from setuptools import setup
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from version import get_git_version

git_version = get_git_version()

# write the version to file so that pybedtools can import it
version_py = os.path.join(os.path.dirname(__file__), 'pybedtools', 'version.py')
fout = open(version_py,'w')
fout.write('__version__="%s"' % git_version)
fout.close()

exts = [ Extension("pybedtools.cbedtools",
              sources=["pybedtools/cbedtools.pyx", "pybedtools/cbedtools.pxi"] \
                   + glob.glob("src/*.cpp"),
              libraries=["stdc++", 'z'],
              include_dirs=["src/"],
              depends = glob.glob("src/*.h"),
              language="c++"),

         Extension('pybedtools.featurefuncs', sources=['pybedtools/featurefuncs.pyx']),

         Extension('pybedtools._Window', 
                    sources=['pybedtools/_Window.pyx'],),
        ]

long_description = """
``pybedtools`` is a wrapper around Aaron Quinlan's BEDtools suite
(http://code.google.com/p/bedtools/), used for comparing genomic features.

``pybedtools`` allows you to intuitively call BEDtools programs from within
Python without writing awkward system calls.

Development version, as well as documentation, can be found on github:

    http://github.com/daler/pybedtools

"""

setup( 
        name="pybedtools",
        version=git_version,
        ext_modules=exts,
        requires=['argparse','cython'],
        packages=['pybedtools','pybedtools.test', 'pybedtools.scripts', 'pybedtools.test.data'],
        author="Ryan Dale",
        description='Wrapper around BEDTools for bioinformatics work',
        long_description=long_description,
        url="none",
        package_data = {'pybedtools':['test/data/*', "*.pyx", "*.pxi", "*.cpp"]},
        package_dir = {"pybedtools": "pybedtools"},
        scripts = ['pybedtools/scripts/venn_gchart.py',
                   'pybedtools/scripts/venn_mpl.py',
                   'pybedtools/scripts/classify_reads.py',
                   'pybedtools/scripts/annotate.py'],
        cmdclass = {'build_ext': build_ext},
        author_email="dalerr@niddk.nih.gov",
    )
