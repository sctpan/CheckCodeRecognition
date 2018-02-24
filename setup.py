from setuptools import setup, find_packages

setup(
    name = 'ZFCheckCode',
    version = '0.0.1',
    keywords = ('CheckCode', 'ImageProcess', 'ImageRecognition', 'SVM'),
    description = 'CheckCode recognition for ZhengFang',
    license = 'MIT License',
    author = 'Ivan',
    author_email = 'sctpan@qq.com',
    packages = find_packages(),
    platforms = 'any',
    install_requires = ['numpy', 'scipy', 'matplotlib', 'scikit-learn', 'pandas', 'requests', 'beautifulsoup4', 'Pillow'],
    package_data = {'ZFCheckCode': ['model/*.model', 'sets/*.png', 'sets/*.txt']},
    include_package_data = True,
)