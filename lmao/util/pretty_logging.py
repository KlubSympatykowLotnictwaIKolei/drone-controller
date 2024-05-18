
import logging
import sys

class CustomLoggingFormatter(logging.Formatter):
    GREY = '\x1b[38;20m'
    YELLOW = '\x1b[33;20m'
    RED = '\x1b[31;20m'
    BOLD_RED = '\x1b[31;1m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\x1b[0m'

    def __init__(self, name = None, max_file_name_length: int = 20, max_logger_name_length: int = 32):
        self.max_file_name_length = max_file_name_length
        LOGGING_LINE_TEMPLATE = f"%(asctime)s {{color_levelname}}%(levelname)7s{self.RESET} --- %(logger_name)s{self.BLUE}[%(filename_short)s]{self.RESET} %(message)s"

        self.__logger_name = name
        if name is not None:
            self.__logger_name = self.__trim_string(name, max_logger_name_length)

        self.formats = {
            logging.DEBUG:    LOGGING_LINE_TEMPLATE.format(color_levelname=self.GREY,    ),
            logging.INFO:     LOGGING_LINE_TEMPLATE.format(color_levelname=self.GREEN,   ),
            logging.WARNING:  LOGGING_LINE_TEMPLATE.format(color_levelname=self.YELLOW,  ),
            logging.ERROR:    LOGGING_LINE_TEMPLATE.format(color_levelname=self.RED,     ),
            logging.CRITICAL: LOGGING_LINE_TEMPLATE.format(color_levelname=self.BOLD_RED,),
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)

        record.filename_short = self.__trim_string(record.filename, 20)
        record.logger_name = ''
        if self.__logger_name is not None:
            record.logger_name = f'[{self.__logger_name}] '
        
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
    def __trim_string(self, filename: str, max_char_count: int) -> str:
        if len(filename) > max_char_count:
            return '...' + filename[-(max_char_count-3):] 
        else:
            return filename.rjust(max_char_count, ' ')
        
def setup_pretty_logging(log_level = logging.INFO, logger_name = None, max_name_length=50):
    handler_sh = logging.StreamHandler(sys.stdout)
    handler_sh.setFormatter(CustomLoggingFormatter(logger_name, max_name_length))
    logging.basicConfig(level=log_level, handlers=[handler_sh])