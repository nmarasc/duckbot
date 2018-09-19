# Last Updated: 2.2
from datetime import datetime
from util.diagMessage import DiagMessage

# Logger class
# Buffers and writes messages to a file
class Logger:
    BUFFER_MAX = 10
    DEFAULT_FN = "../log.txt"

    # Constructor for logger class
    # Params: fn  - file name to use or leave default
    #         log - flag to keep a log file or not
    # Return: Logger instance
    def __init__(self, fn = DEFAULT_FN, log = True):
    #{{{
        self.keep_log = log
        self.fn = fn
        self.log_buffer = []
        if self.keep_log:
            self.log(DiagMessage("LOG0000I"))
    #}}}

    # Append line to internal log buffer, flush if needed
    # Params: diag  - DiagMessage to log
    #         flush - bool flag for flushing buffer early
    # Return: None
    def log(self, diag, flush=False):
    #{{{
        if self.keep_log:
            self.log_buffer.append(str(datetime.now()) + " - " + diag.msg)
            if len(self.log_buffer) >= self.BUFFER_MAX or flush:
                self._write()
        elif not flush:
            print(diag.msg)
    #}}}

    # Write contents of buffer out to file
    # Params: None
    # Return: None
    def _write(self):
    #{{{
        print("Writing log...") if debug else None
        with open(self.fn,'a') as logfile:
            for line in self.log_buffer:
                try:
                    logfile.write(line)
                except TypeError:
                    logfile.write(str(datetime.now())+" - LOG ERR")
                except UnicodeEncodeError:
                    logfile.write(str(line.encode("utf-8","replace")))
                logfile.write("\n")
        del self.log_buffer[:]
    #}}}
