from ide import Ide

class DataStore:
    def __init__(self):
        self.idea = Ide("IntelliJ IDEA")
        self.idea.regex = '.*idea.*'
        self.idea.install_directory = 'idea'

        self.rubymine = Ide("RubyMine")
        self.rubymine.regex = '.*RubyMine.*'
        self.rubymine.install_directory = 'rubymine'

        self.pycharm = Ide("PyCharm")
        self.pycharm.regex = '.*pycharm.*'
        self.pycharm.install_directory = 'pycharm'

        self.phpstorm = Ide("PhpStorm")
        self.phpstorm.regex = '.*PhpStorm.*'
        self.phpstorm.install_directory = 'phpstorm'

        self.webstorm = Ide("WebStorm")
        self.webstorm.regex = '.*WebStorm.*'
        self.webstorm.install_directory = 'webstorm'

        self.clion = Ide("CLion")
        self.clion.regex = '.*clion.*'
        self.clion.install_directory = 'clion'

        self.dbe = Ide("0xDBE")
        self.dbe.regex = '.*0xDBE.*'
        self.dbe.install_directory = '0xdbe'
