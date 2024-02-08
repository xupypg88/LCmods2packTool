import PySimpleGUI as sg
import promaker.promaker as pmk
from PIL import Image
import os

pm = pmk.promaker()

profiles = pm.getProfiles()
lst = sg.Combo(profiles,  expand_x=True, enable_events=True,  readonly=False, key='-COMBO-') #font=('Arial Bold', 14)

layout = [[sg.Text("Choose profile to export:"), lst, sg.Button("Load")],
          [
              sg.Text("Output folder:"),
              sg.In(size=(34, 1), enable_events=True, key="-FOLDER-"),
              sg.FolderBrowse(),
          ],
          [
              sg.Text("Choose Icon (png):"),
              sg.In(size=(29, 1), enable_events=True, key="-ICON-"),
              sg.FileBrowse(),
          ],
          [
              sg.Text("Mod name (a-z A-Z 0-9):"),
              sg.In(size=(29, 1), enable_events=True, key="-NAME-")
          ],
          [
              sg.Text("Version (1.1.0):"),
              sg.In(size=(15, 1), enable_events=True, key="-VERSION-")
          ],
          [
              sg.Text("Mod URL:"),
              sg.In(size=(15, 1), enable_events=True, key="-URL-")
          ],
          [
              sg.Text("Description:"),
              sg.Multiline(s=(38,3), key="-DESCRIPTION-")
          ],
          [sg.Text("Mods:")],
          [sg.Listbox(['Mod list is Empty', 'Choose a profile from the list', 'and click Load'], no_scrollbar=False,  s=(50,15), key="-MODSLIST-")],
          [sg.Button("Export"), sg.Button("Close")]]

def errOutput(errmsg):
    err = sg.Window("Error", [[sg.Text(errmsg, text_color=('red'))], [sg.Button("OK")]], size=(200, 80))
    err.read()
    return

# Create the window
window = sg.Window("LC Profile to Modpack", layout, size=(420, 560))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Close" or event == sg.WIN_CLOSED:
        break

    if event == "Load" and window['-COMBO-'].get() in profiles:
        window['-MODSLIST-'].update(pm.getModsList(window['-COMBO-'].get()))

    if event == "Export" and window['-COMBO-'].get() in profiles:
        if os.path.exists(window['-FOLDER-'].get()):
            mfs = pm.exportManifest(window['-NAME-'].get(), window['-VERSION-'].get(), window['-URL-'].get(), window['-DESCRIPTION-'].get(), pm.getModsList(window['-COMBO-'].get()))
            pm.saveJson(mfs, str(window['-FOLDER-'].get()))

            if window['-ICON-'].get() != "" and os.path.exists(window['-ICON-'].get()):
                image = Image.open(window['-ICON-'].get())
                new_image = image.resize((256, 256))
                new_image.save(str(window['-FOLDER-'].get()) + '/' + mfs['name'] + '/icon.png')
            else:
                errOutput("ICON path is incorrect!")
        else:
            errOutput("Folder path is incorrect!")

window.close()