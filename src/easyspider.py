import sys
import es_manager

if(len(sys.argv) != 2):
    print "Usage: python easyspider.py <serviceport> <workdir>\n"
    sys.exit()

service_port = int(sys.argv[1])
working_dir = sys.argv[2]

print "Running easyspider on service port %d, working directory %s" %(service_port, working_dir)

esmgr = es_manager(service_port, working_dir);
esmgr.run()

