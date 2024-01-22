import os
import json

default_path = os.environ["APPDATA"] + '\\r2modmanPlus-local\\LethalCompany\\profiles'

profiles = os.listdir(default_path)

for i in range(0,len(profiles)):
    print(str(i+1) + ". " + profiles[i])

sel = input("Select the profile number you want to export: ")

YMLpath = default_path + '\\' + profiles[int(sel)-1] + '\\mods.yml'

with open(YMLpath) as yml:
    ymldata = yml.readlines()

mods = []
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
        mods.append(mod)
        mod = ""

manifest = {}

name = "MyFirstMod"
manifest['name'] = input("Import mod name (only letters A-Z a-z; Default: (" + name + "): ") or name

version_number = "1.1.0"
manifest['version_number'] = str(input("Input version (Example: " + version_number + "): ") or version_number)

website_url = "https://www.youtube.com/@grizberrypi/shorts"
manifest['website_url'] = input("Input link (Example: (" + website_url + "): ") or website_url

description = "My first mod"
manifest['description'] = input("Input description (Example: (" + description + "): ") or description

manifest['dependencies'] = mods

if not os.path.exists(manifest['name']):
    os.mkdir(manifest['name'])

with open(str(manifest['name']) + "\\manifest.json", "w") as outfile:
    json.dump(manifest, outfile)

with open(str(manifest['name']) + "\\README.md", "w") as outfile:
    outfile.writelines(manifest['description'])

os.system('copy icon-template.png ' + str(manifest['name']) + '\\icon.png')

nothing = input("The mod files are ready in " + manifest['name'] + "folder. Now you may change the icon.png (should be the same 256x256 size) and compress the files to zip (not the folder). FILES SHOULD BE IN ZIP ROOT!\n PRESS ENTER...")