from  PyPDF2 import PdfFileReader,PdfFileWriter
import glob
path = r'C:\Users\dzk\Desktop'

file_list = glob.glob(path+'\\1?.pdf')

merge_pdf = path+'\\四合一.pdf'  # 输出文件名字
merge = PdfFileWriter()

for i in file_list:   #遍历所有pdf
    p1_reader =  PdfFileReader(i)
    for j in range(p1_reader.getNumPages()): #遍历单个pdf每一页
        merge.addPage(p1_reader.getPage(j))
# 写入输出
with open(merge_pdf,'wb') as f:
    merge.write(f)