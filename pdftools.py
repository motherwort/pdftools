from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from copy import copy, deepcopy
import sys
from pathlib import Path
import re


def splitPages(file, output, axis):
    page = file.getPage(0)
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
    
    def crop(file, output_fname, x1, y1, x2, y2):
        temp_file = PdfFileWriter()
        for i in range(file.getNumPages()):
            page = file.getPage(i)

            page.mediaBox.lowerRight = (x2, y1)
            page.mediaBox.lowerLeft = (x1, y1)
            page.mediaBox.upperRight = (x2, y2)
            page.mediaBox.upperLeft = (x1, y2)
            
            temp_file.addPage(page)
            
        with open(output_fname, 'wb') as file:
            temp_file.write(file)
    
    crop(file, '__temp_l__.pdf', x1, y1, x01, y01)
    crop(file, '__temp_r__.pdf', x02, y02, x2, y2)
    
    f_l = open('__temp_l__.pdf', 'rb')
    f_r = open('__temp_r__.pdf', 'rb')
    file_l = PdfFileReader(f_l)
    file_r = PdfFileReader(f_r)
    for i in range(file_l.getNumPages()):
        output.addPage(file_l.getPage(i))
        output.addPage(file_r.getPage(i))
    
    

def extractPages(file, output, args):
    for arg in args:
        if re.match(r"^\d+-\d+$", arg):
            r = list(map(lambda x: int(x) - 1, arg.split('-')))
            for p in range(r[0], r[1] + (-1)**(r[1] < r[0]), (-1)**(r[1] < r[0])):
                page = file.getPage(p)
                output.addPage(page)
        if re.match(r"^\d+$", arg):
            p = int(arg) - 1
            page = file.getPage(p)
            output.addPage(page)
    

if __name__ == '__main__':
    parent = Path(sys.argv[1]).parent.absolute()

    input_fpath = parent.joinpath(sys.argv[2])
    output_fpath = parent.joinpath(sys.argv[3])

    f = open(input_fpath, "rb")

    input_file = PdfFileReader(f)

    output_file = PdfFileWriter()

    if len(sys.argv) > 5 and sys.argv[4] == 'extract':
        extractPages(input_file, output_file, sys.argv[5:])

    if sys.argv[4] == 'split':
        if len(sys.argv) > 5:
            axis = int(sys.argv[5])
        else:
            axis = 0
        splitPages(input_file, output_file, axis)

    with open(output_fpath, 'wb') as file:
        output_file.write(file)

    f.close()