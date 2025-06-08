import re 
import os
path = r"C:\Education Project Data\Physics\Book9\Modified and Extracted Chp\ForFinalCompilation\Chp9.txt"
with open( path,'r',encoding='utf-8') as f:
    file_data = f.read()
    s =re.sub('<page_number>[0-9]+<page_number>','',file_data)
with open(path,'w',encoding='utf-8') as f:
    f.write(s)
