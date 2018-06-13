import os, sys, py_compile
from glob import glob

file_paths = glob('duckbot/**/*.py', recursive=True)
for path in file_paths:
    try:
        py_compile.compile(path, doraise=True)
    except py_compile.PyCompileError as err:
        print("File failed to compile: " + path, file=sys.stderr)
        err = [x.strip() for x in str(err).split('\n')]
        prefix = [">>  ",">>    ",">>    ",">>  ",">>"]
        for i in range(0,len(err)):
            print(prefix[i % len(prefix)] + err[i], file=sys.stderr)
        return 1
return 0
