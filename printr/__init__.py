from datetime import datetime
import json

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
            print(' ' * 200, end='')
            print('\r', end='')
            print(message, end='')
            print('\r', end='')
        else:
            print(message)