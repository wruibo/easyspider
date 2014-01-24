import os
import threading

class es_fileq(object):
    def __init(self, cache_dir, file_prefix='fileq', record_per_file=20000):
        self._cache_dir = cache_dir
        self._file_prefix = file_prefix
        self._record_per_file = record_per_file

        self._queue_head = []
        self._queue_tail = []
        self._queue_files = []

        self._last_file_num = 0

        self._lock = threading.Lock()

        self.__open()

    def __del__(self):
        self.__close()

    def __open(self):
        self._lock.acquire()
        
        #scan directory for file list
        files_in_dir = os.listdir(self._cache_dir)
        for file in files_in_dir:
            if(file.startswith(self._file_prefix) and os.path.isfile(self._cache_dir+"/"+file)):
                    self._queue_files.append(file)

        if(self._queue_files):
            #sort the queue file list
            numpos = len(self._file_prefix)
            self._queue_files.sort(cmp=lambda x, y: x-y, key=lambda x: int(x[numpos:]))
            self._last_file_num = int(self._queue_files[-1][numpos:])

            #load queue header from queue file list
            head_fpath = self._cache_dir+"/"+self._queue_files.pop(0)
            self._queue_head = self.__loadf(head_fpath)
            os.remove(head_fpath)
        
        self._lock.release()

    def push(self, records):
        self._lock.acquire()
        
        #always add the new records to queue tail
        self._queue_tail += records

        if(self._queue_files):
            #sync the records to file if need
            while(len(self._queue_tail) >= self._record_per_file):
                self._last_file_num += 1
                currfname = self._file_prefix+"_"+str(self._last_file_num)
                currfpath = self._cache_dir+"/"+currfname
                self.__syncf(self._queue_tail[0:self._record_per_file], currfpath)
                self._queue_tail = self._queue_tail[self._record_per_file:]
                self._queue_files.append(currfname)
        else:
            #supply the queue head first
            if(len(self._queue_head) < self._record_per_file):
                addnum = self._record_per_file-len(self._queue_head)
                self._queue_head += self._queue_tail[0:addnum]
                self._queue_tail = self._queue_tail[addnum:]
            
            #sync the queue tail records to file if need
            while(len(self._queue_tail) >= self._record_per_file):
                self._last_file_num += 1
                currfname = self._file_prefix+"_"+str(self._last_file_num)
                currfpath = self._cache_dir+"/"+currfname
                self.__syncf(self._queue_tail[0:self._record_per_file], currfpath)
                self._queue_tail = self._queue_tail[self._record_per_file:]
                self._queue_files.append(currfname)

        self._lock.release()

    def pop(self):
        self._lock.acquire()
        
        records = None
        if(not self._file_list):
            records = self._records
            self._records = []
        else:
            fpath = self._workdir+"/"+self._file_list.pop(0)
            fobj = open(fpath, 'rb')
            records = fobj.readlines()
            fobj.close()
            os.remove(fpath)
        return records
        
        self._lock.release()

    def __loadf(self, fpath):
        fobj = open(fpath, 'rb')
        records = fobj.readlines()
        fobj.close()
        return records

    def __syncf(self, records, fpath):
        fobj = open(fpath, 'wb')
        fobj.write('\n'.join(records))
        fobj.close()

    def __close(self):
        self.__flush()

    def __flush(self):
        if(not self._records): return

        fname = self._file_prefix+"_"+str(self._last_file_num)
        fpath = self._workdir+"/"+fname
        fobj = open(fpath, 'wb')
        for record in self._records:
            fobj.write(record+'\n')
        fobj.close()
        
        self._records = []    
        self._file_list.append(fname)
        self._last_file_num += 1

    def __lines(self, fpath):
        lines = 0
        fobj = open(fpath, 'rb')
        while True:
            buffer = fobj.read(4*1024*1024)
            if not buffer: break
            lines += buffer.count('\n')
        fobj.close( )
        return lines



