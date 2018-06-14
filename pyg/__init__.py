import os

__pygtemplate__ = os.getenv('PYGTEMPLATE', 'default')

if __pygtemplate__ is 'default':
    from .colors import pnnl as c
elif __pygtemplate__ is 'pu':
    from .colors import pu as c
elif __pygtemplate__ is 'pnnl':
    from .colors import pnnl as c
