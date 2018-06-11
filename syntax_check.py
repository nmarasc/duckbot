import os,py_compile
bot_dir = "duckbot/"
for fn in os.listdir(bot_dir):
    if fn.endswith(".py"):
        try:
            py_compile.compile(bot_dir + fn, doraise=True)
        except PyCompileError:
            sys.exit(1)
