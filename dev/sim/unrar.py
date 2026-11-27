import ctypes,os,sys
la=ctypes.CDLL('libarchive.so.13')
la.archive_read_new.restype=ctypes.c_void_p
for f in ['archive_read_support_filter_all','archive_read_support_format_all']: getattr(la,f).argtypes=[ctypes.c_void_p]
la.archive_entry_pathname_utf8.restype=ctypes.c_char_p; la.archive_entry_pathname_utf8.argtypes=[ctypes.c_void_p]
la.archive_entry_pathname.restype=ctypes.c_char_p; la.archive_entry_pathname.argtypes=[ctypes.c_void_p]
la.archive_error_string.restype=ctypes.c_char_p; la.archive_error_string.argtypes=[ctypes.c_void_p]
la.archive_read_open_filename.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
la.archive_read_next_header.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
la.archive_read_data.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]; la.archive_read_data.restype=ctypes.c_ssize_t
la.archive_entry_filetype.argtypes=[ctypes.c_void_p]
src,dst=sys.argv[1],sys.argv[2]; os.makedirs(dst,exist_ok=True)
a=la.archive_read_new(); la.archive_read_support_filter_all(a); la.archive_read_support_format_all(a)
print('open',la.archive_read_open_filename(a,src.encode(),1<<20))
e=ctypes.c_void_p(); buf=ctypes.create_string_buffer(1<<20); n=0
while True:
    r=la.archive_read_next_header(a,ctypes.byref(e))
    if r==1: break
    if r<0: print('err',la.archive_error_string(a)); 
    if r<-20: break
    name=(la.archive_entry_pathname_utf8(e) or la.archive_entry_pathname(e)).decode('utf8','replace').replace('\\','/')
    name=name.lstrip('/').replace('..','_')
    p=os.path.join(dst,name)
    if la.archive_entry_filetype(e)==0o040000: os.makedirs(p,exist_ok=True); continue
    os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,'wb') as out:
        while True:
            k=la.archive_read_data(a,buf,len(buf))
            if k<=0: break
            out.write(buf.raw[:k])
    n+=1
print('files',n)
