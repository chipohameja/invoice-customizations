from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in invoice_customization/__init__.py
from invoice_customization import __version__ as version

setup(
	name="invoice_customization",
	version=version,
	description="Invoice customization for upwork client",
	author="Chipo Hameja",
	author_email="chipohameja@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
