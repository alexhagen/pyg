import psgv.psgv as psgv

__context__ = 'writeup'
__figcount__ = 1
__tabcount__ = 1
__tables__ = {}
__figures__ = {}
__exported_files__ = {}

def interactive(i=False):
    psgv.psgv('__pyginteractive__').val = i


def is_interactive():
    return psgv.psgv('__pyginteractive__').val
