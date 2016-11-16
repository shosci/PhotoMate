# coding=utf-8
import os

class Logger:
    def __init__(self, directory):
        self.log_file = os.path.join(directory, 'log.txt')
        self.log_stream = open(self.log_file, 'w')

    def info(self, info_str):
        self.log_stream.write('info: ' + info_str + os.linesep)

    def warn(self, warn_str):
        self.log_stream.write('warning: ' + warn_str + os.linesep)

    def error(self, error_str):
        self.log_stream.write('error: ' + error_str + os.linesep)

    def finalize(self)
        self.log_stream.flush()
        self.log_stream.close()

