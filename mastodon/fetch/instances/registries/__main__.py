from importlib import import_module
from . import parser, __all__ as registry_options


parser.add_argument('registry', choices=registry_options)
args = parser.parse_args()


try:
    module = args.registry.replace('.', '_')
    import_module('.'+module, package= __package__)
except ValueError as e:
    print(e)