from os import path
import nonebot as nb
import config

if __name__ == '__main__':
    nb.init(config)
    nb.load_plugins(
        path.join(path.dirname(__file__), 'ALLplugins', 'plugins'),
        'ALLplugins.plugins'
    )
    nb.run()
