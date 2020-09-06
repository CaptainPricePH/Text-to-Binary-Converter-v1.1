import binascii, PySimpleGUI as sg, pyperclip, webbrowser


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



    
    
sg.theme('Black')

menu_def = [['&Edit', ['Refresh', '&Copy', '&Paste', 'E&xit']],
            ['&Help', ['&About...', 'Donate']]]

  
layout = [[sg.Menu(menu_def, tearoff=True)],
          [sg.Text('Simple Text to Binary Converter', size=[40, 1])],      
          [sg.Output(size=(80, 20), key='out')],
          [sg.Text('Enter your text or binary here', size=[40, 1])],  
          [sg.Input(size=(80, 5), key='-key-')],
          [sg.Button('To binary'), sg.Button('To text')]]


window = sg.Window('STB', default_element_size=(30, 2)).Layout(layout)      


while True:
    button, value = window.Read()
    message = value['-key-']
    
    if button == 'To binary':
        cypher_message = cypher(message)
        print(cypher_message+"\n")
        
        
    elif button  == 'To text':
        decipher_message = decipher(message)
        print(decipher_message+"\n")
        
        
    elif button == 'Refresh':
        text = ''
        window.Element('out').Update(str(text))
        window.Element('-key-').Update(str(text))
        
    elif button == 'Copy':
        cypher_message = cypher(message)
        pyperclip.copy(str(cypher_message))
        pyperclip.paste()
        
    elif button == 'Paste':
        text = pyperclip.paste()
        window.Element('-key-').Update(str(text))

    elif button == 'About...':      
        sg.popup('About:', 'Created by A. Petek', 'STB', 'Version 1.0',)

    elif button == 'Donate':
        webbrowser.open_new_tab("https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=PFB6A6HLAQHC2&source=url")


window.close()
