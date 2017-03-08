import argparse


class _ArgActionMixin(object):
    
    def error(self, fmt, *args):
        raise argparse.ArgumentError(self, fmt % args)

    def autocast(self, value):
        try:
            return eval(value)
        except:
            # cannot eval, assume it is a plain string                           
            return value     
# ===============================================================================
# Action class for parser.add_argument(action=)


class SomeAction(argparse.Action):
    
    def __call__(self, parser, namespace, values, option_string=None):
        pass
        # TODO
        # Whatever I want
        # Whatever I need
        # Something I can plant
        # So that I won't bleed


# ===============================================================================
# Formatter class for ArgumentParser.formatter_class

class Formatter(argparse.RawDescriptionHelpFormatter):
    
    def _format_usage(self, usage, actions, groups, prefix):
        self._prog
        self._format_actions_usage(actions, groups)
        #return argparse.RawDescriptionHelpFormatter._format_usage(self, usage, actions, groups, prefix)


# ===============================================================================
# STATIC STRINGS

DESCR = '''
Generic Arg Parsing Module
'''

HELP = '''
HELPME
'''


#===============================================================================
# PARSER

def parser():
    """
    :return: parser object
    """

    '''
    # PARSER OBJECT
    p = argparse.ArgumentParser(description=DESCR,
                                formatter_class=Formatter,
                                epilog=HELP)
    '''

    '''
    # POSITIONAL ARGS
    p.add_argument('filepath',
                   metavar='PATHS',
                   help='the multiple paths you want to inspect',
                   nargs='*',
                   default=[],
                   action=SomeAction)
    '''

    '''
    # OPTIONAL ARGS
    p.add_argument('-s', '--short',
                   metavar='',
                   help='if you want less output',
                   nargs='+',
                   dest='short',
                   choices=[])
    '''

    # t = p.add_argument_group('output options')

    # return p