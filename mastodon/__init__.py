import json
import pathlib
import readline


from typing import * 

readline.set_completer_delims(' \t\n=')
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

# Configuration is at the repository level
CONFIG_PATH = pathlib.Path(__file__).parent.parent.joinpath("./project-configs.json")

class Config(dict):
    _mastodon = "mastodon"
    _datarepo = "data_repository"

    _rdd = "rdd"
    _registries = "registries"
    _referral = "referral"

    bad_data_repo_msg = 'Data repository not set. Please provide path to data repository\n> '

    def input_path_loop(msg, dat, key):
        while True:
            try:
                path = pathlib.Path(input(msg))
                if path.exists():
                    dat[key] = str(path.resolve())
                    return
                else:
                    print(f'path {path} does not exist')
            except ValueError as e:
                print(e)


    def __init__(self):
        self.settable = None
        self.config_path = CONFIG_PATH
        self._load()


    def _load(self):

        self.__enter__()

        if self.config_path.exists() and self.config_path.stat().st_size > 0:
            # load all the key value pairs currently in the config object
            with open(self.config_path, 'r') as f:
                try:
                    for k, v in json.load(f).items():
                        self[k] = v
                except json.decoder.JSONDecodeError as e:
                    print('Ran into a decode error for your configuration file. Starting from scratch...')
         
        if Config._mastodon in self:
            MASTODON = self[Config._mastodon]
        else:
            MASTODON = {}
            self[Config._mastodon] = MASTODON
         
        if Config._datarepo not in MASTODON or len(MASTODON[Config._datarepo]) == 0:
            Config.input_path_loop(Config.bad_data_repo_msg, MASTODON, Config._datarepo)

        self.__exit__(None, None, None)


    def get_outdir(self, module_name): 
        m = self[Config._mastodon]
        path = pathlib.Path(m[Config._datarepo]).joinpath("data", *module_name.split('.'))
        return str(path.resolve())
    
    def __setitem__(self, __key: Any, __value: Any) -> None:
        if self.settable:
            return super().__setitem__(__key, __value)
        else: 
            raise ValueError('Setting config values must occur inside a context manager')
        
    def __str__(self):
        # replace this with some serde-like thing
        items = ",".join(['{k}:{v}'.format(k, str(v)) for k, v in self.iteritems()])
        return f'{items}'
        
    def __enter__(self):
        self.settable = True
        return self
    
    def __exit__(self, exec_type, exec_val, exec_tb):
        with open(self.config_path, 'w') as f:
            obj = {k: v for k, v in self.items()}
            json.dump(obj, f, indent=2)
        self.settable = False


CONFIG = Config()