#!/bin/python
# coding: utf-8

if __name__ == '__main__':
    # prep
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\src'))
    from Log import Logger 
    sys.path.pop()
    import tempfile
    d = tempfile.mkdtemp()
    logger = Logger(d)
    # Act
    logger.info("info test")
    logger.warn("warning test")
    logger.error("error test")
    logger.finalize()
    # verify
    from os import path
    logfile = path.join(d, "log.txt")
    with open(logfile,'r') as logstream:
        info_line = logstream.readline()
        assert 'info: info test' in info_line
        warn_line = logstream.readline()
        assert 'warning: warning test' in warn_line
        error_line = logstream.readline()
        assert 'error: error test' in error_line
    print("Logger test passed")

