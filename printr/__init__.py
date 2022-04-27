from datetime import datetime
import json, os

class printr:
    '''printr'''
    def __init__(self, *items, same_line=False, current_time=False):
        if len(items) == 1:
            message = items[0]
        else:
            message = ''
            for item in items:
                if message:
                    message += ' '
                message += str(item)
        if isinstance(message, dict) or isinstance(message, list):
            message = json.dumps(message, indent=4)
        elif current_time:
            current_time = datetime.now()
            current_time = current_time.strftime('%H:%M:%S:%f')
            message = f'{current_time}: {message}'
        if same_line:
            terminal_size = os.get_terminal_size()
            max_characters = terminal_size.columns - 1
            print(' ' * max_characters, end='') # Clear previous output
            print('\r', end='')
            print(message, end='')
            print('\r', end='')
        else:
            print(message)

class current_time:
    def __init__(self, *items, same_line=False):
        printr(*items, same_line=same_line, current_time=True)

class same_line:
    def __init__(self, *items, current_time=False):
        printr(*items, same_line=same_line, current_time=current_time)