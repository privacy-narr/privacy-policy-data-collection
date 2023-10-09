from importlib import import_module
from . import parser, CONFIG


parser.add_argument('registry')
args = parser.parse_args()


try:
    module = args.registry.replace('.', '_')
    print(__package__)
    import_module('.'+module, package= __package__)
except ValueError as e:
    print(e)