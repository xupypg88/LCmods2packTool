import os
import json
import re

class promaker:
    def __init__(self):
        self.default_path = os.environ["APPDATA"] + '\\r2modmanPlus-local\\LethalCompany\\profiles'
        self.profiles = os.listdir(self.default_path)

    def getProfiles(self):
        return self.profiles

    def getProfilePath(self, pname):
        return str(self.default_path + '\\' + pname + '\\mods.yml')

    def getModsList(self, pname):
        with open(str(self.getProfilePath(pname))) as yml:
            ymldata = yml.readlines()

        self.Mods = []
        mod = ""

        for line in ymldata:

            if "name: " in line:
                mod += (line.split(':')[1].strip() + '-')
            if "major: " in line:
                mod += (line.split(':')[1].strip() + '.')
            if "minor: " in line:
                mod += (line.split(':')[1].strip() + '.')
            if "patch: " in line:
                mod += (line.split(':')[1].strip())
                self.Mods.append(mod)
                mod = ""

        return self.Mods

    def checkVersion(self, version):
        pat = re.compile(r'[^.0-9]+')
        version = re.sub(pat, '', version)
        if version != "":
            return version
        else:
            return "1.0.1"

    def filterName(self, name):
        pat = re.compile(r'[^a-zA-Z0-9]+')
        name = re.sub(pat, '', name)
        if name != "":
            return name
        else:
            return "emptyName"

    def exportManifest(self, name, version, website_url, description, dependencies):
        manifest = {}
        manifest['name'] = self.filterName(name)
        manifest['version_number'] = self.checkVersion(version)
        manifest['website_url'] = website_url
        manifest['description'] = description
        manifest['dependencies'] = dependencies

        return manifest

    def saveJson(self, manifest, path):
        if not os.path.exists(path + '/' + manifest['name']):
            os.mkdir(path + '/' + manifest['name'])

        with open(path + "/" + str(manifest['name']) + "/manifest.json", "w") as outfile:
            json.dump(manifest, outfile)

        with open(path + "/" + str(manifest['name']) + "/README.md", "w") as outfile:
            outfile.writelines(manifest['description'])
        return
