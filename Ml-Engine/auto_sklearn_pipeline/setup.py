from setuptools import setup, find_packages

REQUIRED_PACKAGES = ['google-cloud-storage',
                     'scikit-learn==0.20.0',
                     'pandas==0.23.0',
                     'numpy==1.14.3']

setup(name='automobile-pipeline',
      version='1.0',
      packages=find_packages(),
      include_package_data=True,
      description='Sklearn model on Cloud ML Engine',
      author='Loonycorn',
      author_email='contact@loonycorn.com',
      license='MIT',
      install_requires=[REQUIRED_PACKAGES],
      zip_safe=False)




