class Ide:

    def __init__(self, name):
        self.available_version = ""
        self.installed_version = ""
        self.install_directory = ""
        self.regex = ""
        self.name = name
        self.installed = False
        self.install_eap = True
        self.builds = []


    # def get_download_url(self):
    #     m = re.search('.*\/download\/.*', url)
    #     if m:
    #         url += "download_thanks.jsp?os=linux&edition=prof"
    #
    #
