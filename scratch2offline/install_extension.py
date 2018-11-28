# Register GoPiGo3 scratch extension in Raspbian's Scratch 2 Offline Editor.
# The extension can then be used like one of the built-in extensions.

import datetime
import json
import shutil

# extension name
EXT_NAME = "GoPiGo3"

# locations Scratch 2 Offline Editor
S2_FOLDER = "/usr/lib/scratch2"
SE_FOLDER = S2_FOLDER + "/scratch_extensions"
MEDIA_FOLDER = S2_FOLDER + "/medialibrarythumbnails"

REGISTRY_FILE = SE_FOLDER + "/extensions.json"

EXTJS_FILENAME = "gopigo3Extension.js"
EXTJS_FILE = SE_FOLDER + "/" + EXTJS_FILENAME

THUMB_FILENAME = "gopigo3.png"
THUMB_FILE = MEDIA_FOLDER + "/" + THUMB_FILENAME

# read scratch extension registry
print("Reading {}".format(REGISTRY_FILE))
with open(REGISTRY_FILE, "r") as f:
    old_data = json.load(f)

# build new structure
new_data = []

# retain all existing extensions but GoPiGo3
for ext in old_data:
    if ext['name'] != EXT_NAME:
        print("Adding existing extension '{}'".format(ext['name']))
        new_data.append(ext)
    else:
        print("Skipping existing extension '{}'".format(EXT_NAME))

# add GoPiGo3 extension
print("Adding new extension '{}'".format(EXT_NAME))
new_data.append({
    'name': EXT_NAME,
    'type': 'extension',
    'file': EXTJS_FILENAME, 
    'md5': THUMB_FILENAME,
    'url': "http://localhost:8080/",
    'tags': ['hardware']
})

# make backup of registry
registry_backup = (REGISTRY_FILE + ".backup_" + 
    datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
print("Creating backup {}".format(registry_backup))
shutil.move(REGISTRY_FILE, registry_backup)

# write new registry
print("Writing {}".format(REGISTRY_FILE))
with open(REGISTRY_FILE, "w") as f:
    json.dump(new_data, f)

# put supporting files into place
print("Writing {}".format(EXTJS_FILE))
shutil.copy(EXTJS_FILENAME, EXTJS_FILE)
print("Writing {}".format(THUMB_FILE))
shutil.copy(THUMB_FILENAME, THUMB_FILE)
