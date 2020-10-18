import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image

def jpg2pdf(src, dst):
    im1 = Image.open(src)
    pdf1_filename = dst
    im1.save(pdf1_filename, "PDF" ,resolution=100.0, save_all=True)

def add_cover(cover, main_list, output_name, start_page=1):
    def get_page_size():
        with open(main_list[0], 'rb') as fp:
            pdf = PdfFileReader(fp)
            return pdf.getPage(0).mediaBox
    _, _, upleft, upright = get_page_size()

    cover_pdf = PdfFileReader(open(cover, 'rb'))

    pdf = PdfFileReader(open(main_list[0], 'rb'))

    pdf_writer = PdfFileWriter()

    scaled_cover = cover_pdf.getPage(0)
    scaled_cover.scaleTo(int(upleft), int(upright))
    pdf_writer.addPage(scaled_cover)

    for page in range(start_page, pdf.getNumPages()):
        page_obj = pdf.getPage(page)
        page_obj.scaleTo(int(upleft), int(upright))
        pdf_writer.addPage(page_obj)

    with open(output_name, 'wb') as f:
        pdf_writer.write(f)

def print_page_info(filename):
    with open(filename, 'rb') as fp:
        pdf = PdfFileReader(fp)
        for i in range(pdf.getNumPages()):
            lowleft, lowright, upleft, upright = pdf.getPage(i).mediaBox
            print("{}, {}, {}, {}".format(lowleft, lowright, upleft, upright))

def cover_preprocess(cover_image):
    if os.path.splitext(cover_image)[1] == '.pdf':
        return cover_image
    else:
        cover_pdf = '{}.pdf'.format(os.path.splitext(cover_image)[0])
        jpg2pdf(cover_image, cover_pdf)
        return cover_pdf

cover_image = sys.argv[1]
if not os.path.exists(cover_image):
    print("cover image does not exists")
    exit(-1)

output_name = sys.argv[2]
if os.path.exists(output_name):
    print("output({}) already exists".format(output_name))
    exit(0)

main_pdf_list = sys.argv[3:]
for main_pdf in main_pdf_list:
    if not os.path.exists(main_pdf):
        print("pdf does not exists")
        exit(-1)

cover_pdf = cover_preprocess(cover_image)

add_cover(cover_pdf, main_pdf_list, output_name)

print_page_info(output_name)
