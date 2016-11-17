#!/bin/python
# coding: utf-8

if __name__ == '__main__':
    # prep
    from sys import path
    path.append('..\src')
    from Log import Logger 
    path.pop()
    import tempfile
    d = tempfile.mkdtemp()
    print("Created temp directory: " + d)
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

