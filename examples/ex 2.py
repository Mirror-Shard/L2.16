#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# Вариант 1
with open("foo.txt") as f:
    contents = f.read()
my_list = json.loads(contents)

# Вариант 2
with open("foo.txt", "r") as f:
    my_list = json.load(f)

print(my_list)
