from setuptools import setup, find_packages


version = __import__('vv').__version__

setup(
  name = 'django-vitevue',
  packages=find_packages(),
  include_package_data=True,
  version = version,
  description = 'Assemble a Vue.js frontent from several Django modules',
  author = 'synw',
  author_email = 'synwe@yahoo.com',
  url = 'https://github.com/synw/django-vitevue', 
  download_url = 'https://github.com/synw/django-vitevue/releases/tag/'+version, 
  keywords = ['django', 'vuejs'], 
  classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
  zip_safe=False
)
