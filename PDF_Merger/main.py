from PyPDF2 import PdfFileMerger, PdfWriter

merger = PdfWriter()

pdfs=[]

n=int(input("Enter the number of pdfs you want to merge: "))

for i in range(n):
    pdf=input(f"Enter the name of the pdf file {i+1} with extension: ")
    pdfs.append(pdf)

for pdf in pdfs:
    merger.append(pdf)

merger.write("merged.pdf")
merger.close()
