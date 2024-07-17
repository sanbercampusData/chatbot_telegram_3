#kita akan membuat dua jenis logging
#1. untuk pencatatan/debug
#2. error

import logging
from dotenv import dotenv_values

env = dotenv_values(".env")
log_path = env['LOG_PATH']
log_format = env['LOG_FORMAT']
project_path = env['PROJECT_PATH']

# setup logger data
data_logger = logging.getLogger('data_logger')
data_logger.setLevel(logging.DEBUG)

# create handler data
data_file_handler = logging.FileHandler(f"{project_path}{log_path}/data.log")
data_file_handler.setLevel(logging.DEBUG)

# create formatter data
data_formatter = logging.Formatter(log_format)
data_file_handler.setFormatter(data_formatter)

# add handler data
data_logger.addHandler(data_file_handler)

# setup error data
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)

# create console handler
console_error_handler = logging.StreamHandler()
console_error_handler.setLevel(logging.ERROR)

# create handler error
error_file_handler = logging.FileHandler(f"{project_path}{log_path}/error.log")
error_file_handler.setLevel(logging.ERROR)

# create formatter error
error_formatter = logging.Formatter(log_format)
error_file_handler.setFormatter(error_formatter)
console_error_handler.setFormatter(error_formatter)

# add handler error
error_logger.addHandler(error_file_handler)
error_logger.addHandler(console_error_handler)

def log_data(data):
    data_logger.debug(data)

def log_error(error):
    error_logger.error(error)

if __name__ == "__main__":
    log_data("ini adalah data yang akan dibaca")
    log_error("ini adalah error yang akan dibaca")