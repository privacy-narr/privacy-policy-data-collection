import importlib
from . import __all__, parser

args = parser.parse_args()
importlib.import_module('.'+args.obj, package=__package__)