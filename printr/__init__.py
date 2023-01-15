import sys, logging, json, os, shutil, coloredlogs
from pathlib import Path
from datetime import datetime

class logger:
    def __init__(self, log_filepath=None, max_lines=10000):
        filename = Path(sys.argv[0]).stem
        self.filename = filename
        if not log_filepath:
            log_filepath = f'{os.getcwd()}/{filename}.txt'
        self.log_filepath = log_filepath
        self.max_lines = max_lines

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_file = logging.FileHandler(log_filepath, encoding='utf-8')
        log_format = logging.Formatter(fmt='%(levelname)s - %(asctime)s.%(msecs)03d - Line %(lineno)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        log_file.setFormatter(log_format)
        logger.addHandler(log_file)
        self.log_file = log_file

        coloredlogs.install(level=logging.INFO, logger=logger, fmt='%(message)s')
        self.logger = logger

        self.log()
        self.log('Starting', filename)
        self.log()

    def log(self, *items, level='info'):
        message = ''
        for item in items:
            if message and '\n' not in message:
                message += ' ' # Add space in between variables
            if isinstance(item, dict) or isinstance(item, list):
                try:
                    if message and '\n' not in message: # Add line breaks before and after
                        formatted_item = '\n'
                    else:
                        formatted_item = ''
                    formatted_item += json.dumps(item, indent=4) # Beautify JSON objects
                    item = formatted_item + '\n'
                except TypeError:
                    pass
            message += str(item)

        if not message:
            log_format = logging.Formatter(fmt='%(message)s')
            self.log_file.setFormatter(log_format)

        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'success':
            self.logger.success(message)
        elif level == 'warning':
            self.logger.warning(message)

        if not message:
            log_format = logging.Formatter(fmt='%(levelname)s - %(asctime)s.%(msecs)03d - Line %(lineno)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            self.log_file.setFormatter(log_format)

        log_file = open(self.log_filepath, 'r+').read()
        number_of_lines = len(log_file.splitlines())
        if number_of_lines > self.max_lines:
            self.logger.info('Resetting log file')
            self.log_file.close()
            log_file = logging.FileHandler(self.log_filepath, mode='w', encoding='utf-8')
            log_format = logging.Formatter(fmt='%(levelname)s - %(asctime)s.%(msecs)03d - Line %(lineno)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            log_file.setFormatter(log_format)
            self.logger.addHandler(log_file)
            self.log_file = log_file
    
    def error(self, *items):
        self.log(*items, level='error')
    
    def debug(self, *items):
        self.log(*items, level='debug')
    
    def success(self, *items):
        self.log(*items, level='success')
    
    def warning(self, *items):
        self.log(*items, level='warning')
    
    def current_time(self, *items, level='info'):
        coloredlogs.install(level=logging.INFO, logger=self.logger, fmt='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S') # Add current time to printed log output format
        self.log(*items, level=level)
        coloredlogs.install(level=logging.INFO, logger=self.logger, fmt='%(message)s') # Reset to default log format

    # def __del__(self):
    #     self.log('Exiting', self.filename)
    #     self.log()

class printr:
    '''printr'''
    def __init__(self, *items, same_line=False, current_time=False, check_for_log=True, level='info'):
        if len(items) == 1:
            message = items[0]
            if isinstance(message, dict) or isinstance(message, list):
                try: message = json.dumps(message, indent=4) # Beautify JSON objects
                except TypeError: pass
        else:
            message = ''
            for item in items:
                if message:
                    message += ' ' # Add space in between variables
                if isinstance(item, dict) or isinstance(item, list):
                    try: item = json.dumps(item, indent=4) # Beautify JSON objects
                    except TypeError: pass
                message += str(item)
        if current_time:
            current_time = datetime.now()
            current_time = current_time.strftime('%H:%M:%S:%f')
            message = f'{current_time}: {message}'
        if same_line:
            terminal_size = shutil.get_terminal_size() # Uses shutil rather than os to support piping output to file
            max_characters = terminal_size.columns - 1
            print(' ' * max_characters, end='') # Clear previous output
            print('\r', end='')
            print(message, end='')
            print('\r', end='')
        else:
            if not check_for_log:
                print(message)
            else:
                logger = logging.getLogger()
                if logger.level != 30:
                    if level == 'debug':
                        logger.debug(message)
                    elif level == 'error':
                        logger.error(message)
                    else:
                        logger.info(message)
                elif level != 'debug':
                    print(message)

class current_time:
    def __init__(self, *items, same_line=False, check_for_log=True):
        printr(*items, same_line=same_line, current_time=True, check_for_log=check_for_log)

class same_line:
    def __init__(self, *items, current_time=False, check_for_log=True):
        printr(*items, same_line=same_line, current_time=current_time, check_for_log=check_for_log)