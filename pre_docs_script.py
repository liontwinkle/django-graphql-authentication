"""
- get class names and docstrings as context variables into the docs
- copy [CONTRIBUTORS, CHANGES] files to the docs dir
"""

import os
import shutil
import re


# copy mixins file from .py to .yml
current_dir = os.path.abspath(os.path.split(os.path.split(__file__)[0])[0])
source = current_dir + "/graphql_auth/mixins.py"
destination = current_dir + "/docs/data/api.yml"
dest = shutil.copyfile(source, destination)

# get the text content
with open(destination, "r") as file:
    text = file.read()

# extract each class and docstring
pattern = re.compile(
    'class\s(?P<class>\w*)Mixin[\w|\(|\)]+:\n\s*"""(?P<doc>[^*]*)"""',
    re.S | re.M,
)
matches = re.findall(pattern, text)

# build the yaml string
yaml_strings = ["# this file is auto generated by the pre_docs_script.py", ""]
for m in matches:
    class_name, docstring = m
    yaml_strings.append(class_name + ": |" + docstring)
yaml_string = "\n".join(yaml_strings)

# write the file
with open(destination, "w") as file:
    file.write(yaml_string)


# copy contributors and changes files to docs dir
files = ["CONTRIBUTORS.md", "CHANGES.md"]
for file in files:
    shutil.copyfile(current_dir + "/" + file, current_dir + "/docs/" + file)
