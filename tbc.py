import PySimpleGUI as sg
import binascii
import pyperclip
import webbrowser
from json import (load as jsonload, dump as jsondump)
from os import path



binary_base = [1, 2, 4, 8, 16, 32, 64, 128]


def cypher(message):
    cypher_words = []
    for letter in message:
        cypher_letter = format(ord(letter), 'b')
        cypher_words.append(cypher_letter)
    return ' '.join(cypher_words)




def decipher(message):
    words = message.split(' ')
    decipher_message = []
    for word in words:
        word = str(word)
        sumatory = 0
        for value, letter in enumerate(word[::-1]):
            if int(letter) == 1:
                sumatory += binary_base[value]
        decipher_letter = chr(sumatory)
        decipher_message.append(decipher_letter)
    return "".join(decipher_message)

SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'theme': sg.theme()}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'theme': '-THEME-'}

def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


def save_settings(settings_file, settings, values):
    if values:      
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved')

def create_settings_window(settings):
    sg.theme(settings['theme'])

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  [sg.Text('Settings', font='Any 15')],
                [TextLabel('Theme'),sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)

    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')

    return window

def create_main_window(settings):
    sg.theme(settings['theme'])
    menu_def = [['&Menu', ['Refresh', '&Copy', '&Paste', 'Settings', 'E&xit']],
                ['&Help', '&About...']]

    right_click_menu = ['Unused', ['&Copy', '&Paste','Settings', 'E&xit']]

    layout = [[sg.Menu(menu_def)],
              [sg.Text('Text to Binary Converter', size=(60,1), font=('Helvetica', 11)), sg.Button('', key='paypal', size=(12,1), font=('Helvetica', 9), button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                                                image_filename='paypal.png', image_size=(80, 50), image_subsample=2, border_width=0)],      
              [sg.Output(size=(76, 14), key='out', font=('Helvetica', 11))],
              [sg.Text('Enter your text or binary here', size=[40, 1], font=('Helvetica', 9))],  
              [sg.Multiline(size=(76,6), key='-key-', font=('Helvetica', 11))],
              [sg.Button('To binary', font=('Helvetica', 9), size=(8, 1)),
               sg.Button('To text', font=('Helvetica', 9), size=(8, 1)),
               sg.Button('Refresh', font=('Helvetica', 9), size=(8, 1))]]

    return sg.Window('TBC',
                     layout=layout,
                     right_click_menu=right_click_menu)               
                     

def main():
    window, settings = None, load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    while True:
        if window is None:
            window = create_main_window(settings)
        event, value = window.Read()
        message = value['-key-'].rstrip()

        if event == 'To binary':
            cypher_message = cypher(message)
            print(cypher_message+"\n")


        elif event  == 'To text':
            try:
                decipher_message = decipher(message)
                print(decipher_message+"\n")
            except ValueError:
                continue
        

        elif event == 'Refresh':
            text = ''
            window.Element('out').Update(str(text))
            window.Element('-key-').Update(str(text))

        elif event == 'Copy':
            cypher_message = cypher(message)
            pyperclip.copy(str(cypher_message))
            pyperclip.paste()


        elif event == 'Paste':
            text = pyperclip.paste()
            window.Element('-key-').Update(str(text))

        elif event == 'Settings':
            event, values = create_settings_window(settings).read(close=True)
            if event == 'Save':
                window.close()
                window = None
                save_settings(SETTINGS_FILE, settings, values)

        elif event == 'About...':
            sg.popup('About:', 'Created by A. Petek', 'TBC', 'Version 1.1',)

        elif event == 'paypal':
            webbrowser.open_new_tab("https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=PFB6A6HLAQHC2&source=url")

        elif event in (None, 'Exit'):
            break

    window.Close()

main()
