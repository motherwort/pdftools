import os
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from copy import copy, deepcopy
import sys
from pathlib import Path
import re
import io


class File(io.BytesIO):
    def __init__(self, filename) -> None:
        self.name = filename
        super().__init__()

    @property
    def pages(self):
        reader = PdfFileReader(self)
        return reader.getNumPages()


# TODO реализовать все действия, заявленные в UI


def mergeFiles(files):
    merged = PdfFileWriter()
    for file in files:
        reader = PdfFileReader(file)
        merged.appendPagesFromReader(reader)
    output = File('merge.pdf')
    merged.write(output)
    return output


def splitPages(file, axis):
    reader = PdfFileReader(file)
    page = reader.getPage(0)
    """
    (x1,y2) (x2,y2)
    (x1,y1) (x2,y1)
    """
    x1, y1 = page.mediaBox.getLowerLeft()
    x2, y2 = page.mediaBox.getUpperRight()
    
    if axis == 0:
        x01 = x02 = x1 + (x2 - x1)/2
        y01, y02 = y2, y1
    else:
        x01, x02 = x2, x1
        y01 = y02 = y1 + (y2 - y1)/2
    
    def crop(reader, output_fname, x1, y1, x2, y2):
        temp_file = PdfFileWriter()
        for i in range(reader.getNumPages()):
            page = reader.getPage(i)

            page.mediaBox.lowerRight = (x2, y1)
            page.mediaBox.lowerLeft = (x1, y1)
            page.mediaBox.upperRight = (x2, y2)
            page.mediaBox.upperLeft = (x1, y2)
            
            temp_file.addPage(page)
            
        with open(output_fname, 'wb') as file:
            temp_file.write(file)
    
    crop(reader, '__temp_l__.pdf', x1, y1, x01, y01)
    crop(reader, '__temp_r__.pdf', x02, y02, x2, y2)
    
    f_l = open('__temp_l__.pdf', 'rb')
    f_r = open('__temp_r__.pdf', 'rb')
    file_l = PdfFileReader(f_l)
    file_r = PdfFileReader(f_r)

    splitted = PdfFileWriter()
    for i in range(file_l.getNumPages()):
        splitted.addPage(file_l.getPage(i))
        splitted.addPage(file_r.getPage(i))

    output = File('merge.pdf')
    splitted.write(output)
    
    f_l.close()
    f_r.close()
    os.remove('__temp_l__.pdf')
    os.remove('__temp_r__.pdf')
    return output
    

# TODO добавить нотацию слайсов с шагом: вместо (или наряду с) 1-10 использовать 1:10:2
def extractPages(file, args):
    reader = PdfFileReader(file)
    output = File('extract.pdf')
    extracted = PdfFileWriter()
    for arg in args:
        if re.match(r"^\d+-\d+$", arg):
            r = list(map(lambda x: int(x) - 1, arg.split('-')))
            for p in range(r[0], r[1] + (-1)**(r[1] < r[0]), (-1)**(r[1] < r[0])):
                page = reader.getPage(p)
                extracted.addPage(page)
        if re.match(r"^\d+$", arg):
            p = int(arg) - 1
            page = reader.getPage(p)
            extracted.addPage(page)
    extracted.write(output)
    return output
    

# TODO сделать потом консольный интерфейс, .cmd исправить чтобы прото передавал argv в скрипт,
# найти библиотеку, в которой уже красивый консольный интерфейс реализован
if __name__ == '__main__':
    raise NotImplementedError
    # parent = Path(sys.argv[1]).parent.absolute()

    # input_fpath = parent.joinpath(sys.argv[2])
    # output_fpath = parent.joinpath(sys.argv[3])

    # f = open(input_fpath, "rb")

    # input_file = PdfFileReader(f)

    # output_file = PdfFileWriter()

    # if len(sys.argv) > 5 and sys.argv[4] == 'extract':
    #     extractPages(input_file, output_file, sys.argv[5:])

    # if sys.argv[4] == 'split':
    #     if len(sys.argv) > 5:
    #         axis = int(sys.argv[5])
    #     else:
    #         axis = 0
    #     splitPages(input_file, output_file, axis)

    # with open(output_fpath, 'wb') as file:
    #     output_file.write(file)

    # f.close()