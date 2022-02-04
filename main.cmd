@echo off

:: NOT IMPLEMENTED YET
echo NOT IMPLEMENTED YET
exit

set script=C:/Users/alimb/anaconda3/python.exe c:/Users/alimb/pdftools/pdftools.py %0

:: SYNTAX
::
:: %script% %input.pdf% %output.pdf% (split|extract P [P [P [...]]])
:: P - page number or page range (can be reverse)
::
:: note: %output.pdf% can't be equal to %input.pdf%

:: EXAMPLES
::
:: %script% input.pdf out.pdf extract 10-1
:: %script% input.pdf out.pdf extract 1 3 4
:: %script% input.pdf out.pdf extract 6 1-5 29
::
:: %script% input.pdf __temp.pdf extract 45-52
:: %script% __temp.pdf __temp2.pdf split
:: %script% __temp.pdf out.pdf extract 1-15

%script% input.pdf out.pdf split 1

del __*.pdf