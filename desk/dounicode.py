import sys, re

def decode_heuristically(string, enc = None, denc = sys.getdefaultencoding()):
    #print denc
    #print string
    if isinstance(string, unicode):
        #print string
        return string, 0, "utf-8"
    try:
        new_string = unicode(string, "ascii")
        #print "hello"
        return string, 0, "ascii"
    except UnicodeError:
        encodings = ["utf-8","iso-8859-1","cp1252","iso-8859-15"]

        if denc != "ascii": encodings.insert(0, denc) 

        if enc: 
            encodings.insert(0, enc)    
            #print "iitr"

        for enc in encodings:
             #print "welcomme"
             if (enc in ("iso-8859-15", "iso-8859-1") and
                re.search(r"[\x80-\x9f]", string) is not None):
                #print "first time"
                continue

             if (enc in ("iso-8859-1", "cp1252") and
                re.search(r"[\xa4\xa6\xa8\xb4\xb8\xbc-\xbe]", string)\
                is not None):
                #print "two"
                continue
            
             try:
                new_string = unicode(string, enc)
             except UnicodeError:
                pass
             else:
                if new_string.encode(enc) == string:
                 #print "namune"
                 #print new_string,enc
                 return new_string,enc #0

        output = [(unicode(string, enc, "ignore"), enc) for enc in encodings]
        output = [(len(new_string[0]), new_string) for new_string in output]
        output.sort()
        new_string, enc = output[-1][1]
        #print "hkl"
        return new_string, 1, enc
