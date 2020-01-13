'''Setup.py
'''

from os import getenv
import re
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext as _build_ext

from src.preprocessors import mingw_preprocessor

copts = {
    'unix': ['-O3', '-fopenmp'],
    'mingw32': ['-O3'],
}
lopts = {
    'unix': ['-fopenmp'],
    'mingw32': [],
}
include_dirs = ['src/', 'mingw32/src/', 'bart/src/']

# Here are all the files we pull from BART
bart_files = [
    "src/sys/mman.c",
    "bart/src/misc/version.c",
    "bart/src/num/vecops.c",
    "bart/src/num/simplex.c",
    "bart/src/num/optimize.c",
    "bart/src/num/multind.c",
    "bart/src/misc/ya_getopt.c",
    "bart/src/misc/opts.c",
    #"bart/src/misc/nested.c",
    "bart/src/misc/misc.c",
    "bart/src/misc/io.c",
    "bart/src/misc/mmio.c",
    "bart/src/misc/debug.c",
    "bart/src/twixread.c",
]

class build_ext(_build_ext):
    '''Subclass build_ext to bootstrap numpy and deal with compile.'''

    def finalize_options(self):
        _build_ext.finalize_options(self)

        # Prevent numpy from thinking it's still in its setup process
        import numpy as np
        self.include_dirs.append(np.get_include())

    def build_extensions(self):
        '''We want different opts and potentially preprocess.'''
        c = self.compiler.compiler_type
        print(c)
        if c in copts:
            for e in self.extensions:
                if e.name == 'rawdatarinator.twixread':
                    e.extra_compile_args = copts[c]
        if c in lopts:
            for e in self.extensions:
                if e.name == 'rawdatarinator.twixread':
                    e.extra_link_args = lopts[c]

        # We might need to do some preprocessing before we build...
        if c in ['mingw32']:
            for b in bart_files:
                mingw_preprocessor(b)

        _build_ext.build_extensions(self)


# See make_release.sh, __DO_CYTHON_BUILD is set to 1 when we want
# to convert *.pyx into *.c files and 0 when we want to compile *.c
pyx_or_c = 'c'
if getenv('__DO_CYTHON_BUILD') == '1':
    pyx_or_c = 'pyx'
    print('DOING CYTHON')

extensions = [
    Extension(
        'rawdatarinator.twixread',
        [re.sub('bart', 'mingw32', f) for f in bart_files] + ["src/twixread_pyx.%s" % pyx_or_c],
        include_dirs=include_dirs,
    ),
    Extension(
        'rawdatarinator.read',
        ['src/readcfl.%s' % pyx_or_c],
        include_dirs=[]),
    Extension(
        'rawdatarinator.write',
        ['src/writecfl.%s' % pyx_or_c],
        include_dirs=[]),
]

setup(
    name='rawdatarinator',
    version='1.3.1',
    author='Nicholas McKibben',
    author_email='nicholas.bgp@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/mckib2/rawdatarinator',
    license='GPL',
    description='Read Siemens raw data.',
    long_description=open('README.rst').read(),
    install_requires=[
        "numpy>=1.17.2",
    ],
    cmdclass={'build_ext': build_ext},
    setup_requires=['numpy'],
    python_requires='>=3.5',

    # And now for Cython generated files...
    ext_modules=extensions
)
