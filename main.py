import configparser
from build_wiki_reader import build_wiki_reader
config = configparser.ConfigParser()
config.read('settings.cfg')

print("[Wiki Reader Builder] Starting")
build_wiki_reader(
    config['Paths']['base_html'],
    config['Paths']['wiki_md_root'],
    config['Paths']['wiki_root'],
    config['Paths']['wiki_home']
    )
print("[Wiki Reader Builder] Finished")
