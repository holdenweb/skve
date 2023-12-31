from __future__ import annotations

import os
import sys

from .textual_labelset import build_app
print(os.getcwd(), sys.argv)
names = list(
    enumerate([
        s.strip()
        for s in open('names.txt').readlines()[:24]
    ]),
)
n = len(names)//2
print('Building app')
app = build_app(dict(names[:n]), dict(names[n:]))
app.run()
