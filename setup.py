from distutils.core import setup
from setuptools.command.install import install as _install


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(
            _post_install, (self.install_lib,),
            msg="")

def _post_install(dir):
    print_cafe_mug()

def print_cafe_mug():
    print('\n'.join(["\t\t    ...................",
                     "\t\t    |.................|",
                     "\t\t    |                 |",
                     "\t\t    |   O         O   |",
                     "\t\t    |                 |",
                     "\t\t    |        |        |",
                     "\t\t    |        |        |",
                     "\t\t    |        |        |",
                     "\t\t    |                 |",
                     "\t\t    |    \_______/    |",
                     "\t\t    |                 |",
                     "\t\t    |_________________|",
                     ]))
    print("********************************************************")
    print("Congratulations, maRshEST is now Installed")
    print("********************************************************")

setup(
  name = 'marshest',
  packages = ['marshest'],
  version = '0.1.1',
  description = 'A library for Marshalling JSON requests',
  author = 'Jaydeep Chakrabarty',
  author_email = 'jaydeepc@thoughtworks.com',
  install_requires=['requests'],
  url = 'https://github.com/jaydeepc/marshmallow',
  download_url = 'https://github.com/jaydeepc/marshmallow/tarball/0.1',
  keywords = ['testing', 'marshalling', 'json', 'restapi', 'api', 'automation', 'functionaltesting'],
  classifiers = [],
  cmdclass={'install': install}
)
