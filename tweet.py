import sys,os,time as t;from shakespeare import stream
w=sys.stdout.write;f=sys.stdout.flush;g=stream(os.getenv("MODE","demo"));d=60/float(os.getenv("WPM",60))
try:
 while 1:w(next(g)+" ");f();t.sleep(d)
except(KeyboardInterrupt,BrokenPipeError):pass