from tabulate import tabulate
from IPython.display import SVG, display, Latex, HTML, display_latex
import sys
import os
import subprocess
import __builtin__ as bi

def get_pname(id):
    p = subprocess.Popen(["ps -o cmd= {}".format(id)], stdout=subprocess.PIPE, shell=True)
    return str(p.communicate()[0])

def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def need_latex():
    cmds = get_pname(os.getpid())
    cmds += get_pname(os.getppid())
    if 'jupyter-nbconvert' in cmds and ('to pdf' in cmds or 'to latex' in cmds):
        import IPython
        ip = IPython.core.getipython.get_ipython()
        ip.display_formatter.formatters['text/latex'].enabled = True
        return True
    else:
        return os.path.isfile('/tmp/need_latex')

def table(array, caption='', label=None, headers=None, floatfmt=".2f"):
    if label is None:
        label = caption
    if run_from_ipython() and not need_latex():
        table = tabulate(array, headers=headers, tablefmt='html',
                         numalign='center', stralign='center',
                         floatfmt=floatfmt)
        fig_html = r"""
            <div class='table' style='align: center; margin-left: auto; margin-right: auto;'>
                <div style='margin: auto; text-align: center;' class='tablecaption' name='%s'><b>Table %d:</b> %s</div>
                %s
            </div>
        """ % (label, bi.__tabcount__, caption, table)
        bi.__tables__[label] = bi.__tabcount__
        bi.__tabcount__ += 1
        display(HTML(fig_html))
    elif run_from_ipython() and need_latex():
        table = tabulate(array, headers=headers, tablefmt='latex',
                         numalign='center', stralign='center',
                         floatfmt=floatfmt)
        strlatex = r"""
        \begin{table}
            \centering
            %s
            \caption{%s}
            \label{tab:%s}
        \end{table}""" % (table, caption, label)
        display(Latex(strlatex))

def cite(label):
    if run_from_ipython() and not need_latex():
        return '[1]'

def figures():
    print bi.__tables__
    print bi.__figures__

def cref(label):
    if run_from_ipython and not need_latex():
        if label in bi.__tables__.keys():
            number = bi.__tables__[label]
            text = 'table'
        elif label in bi.__figures__.keys():
            number = bi.__figures__[label]
            text = 'figure'
        else:
            text = 'ref'
            number = 0
        html_str = '<a href="#%s">%s %d</a>' % (label, text, number)
        return display(HTML(html_str))
    elif run_from_ipython and need_latex():
        return display(Latex('\[fig:%s\]' % label))
