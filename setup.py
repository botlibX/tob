#!/usr/bin/env python3


"stub"


import setuptools


setuptools.setup(
    data_files=[
        ('share/tob/mods', [
            'mods/atr.py',
            'mods/flt.py',
            'mods/fnd.py',
            'mods/irc.py',
            'mods/log.py',
            'mods/lst.py',
            'mods/man.py',
            'mods/mbx.py',
            'mods/mdl.py',
            'mods/mod.py',
            'mods/pth.py',
            'mods/req.py',
            'mods/rss.py',
            'mods/rst.py',
            'mods/sil.py',
            'mods/slg.py',
            'mods/tdo.py',
            'mods/thr.py',
            'mods/tmr.py',
            'mods/udp.py',
            'mods/upt.py',
            'mods/web.py',
            'mods/wsd.py'
            ]
        )
    ],
    scripts=[
        "bin/tob",
    ])
