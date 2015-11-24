from setuptools import setup
import glob

# from mpld3
def get_version(fname):
    """Get the version info from the mpld3 package without importing it"""
    import ast

    with open(fname) as init_file:
        module = ast.parse(init_file.read())

    version = (ast.literal_eval(node.value) for node in ast.walk(module)
               if isinstance(node, ast.Assign)
               and node.targets[0].id == "__version__")
    try:
        return next(version)
    except StopIteration:
        raise ValueError("version could not be located")



setup(name='bw',
      version=get_version("bw/__init__.py"),
      packages=['bw'],
      package_data={'bw': glob.glob("libBigWig/*")},
      zip_safe=False,
      install_requires=['cffi', 'setuptools>=0.6c11'],
      test_suite='nose.collector',
      tests_require=['nose'],
      cffi_modules=["bw/build_bw.py:ffi"],
      )

