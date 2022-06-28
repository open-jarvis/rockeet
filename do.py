"""
Copyright (c) 2022 Philipp Scheer
"""


import os
import shutil


_ = os.path.dirname(os.path.realpath(__file__))


for dir in ["build", "dist", "*.egg-info"]:
    print(f"I | Deleting {dir}")
    shutil.rmtree(_ + "/" + dir, ignore_errors=True)

print(f"I | Calling setup script")
# os.system("python setup.py sdist bdist_wheel")
os.system("python setup.py install")

print(f"I | Uploading package with twine")
os.system("python -m twine upload dist/* --verbose")
