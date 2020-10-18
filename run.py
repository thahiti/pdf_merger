import os
import sys
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image

def jpg2pdf(src, dst):
    im1 = Image.open(src)
    pdf1_filename = dst
    im1.save(pdf1_filename, "PDF" ,resolution=100.0, save_all=True)

def merge_pdf(cover, main_list, output_name, start_page=1):
    def get_page_size():
        with open(main_list[0], 'rb') as fp:
            pdf = PdfFileReader(fp)
            return pdf.getPage(0).mediaBox
    def make_page_start_map(pdf_list):
        page_start_map = [0] * len(pdf_list)
        page_start_map[1] = start_page
        return page_start_map

    _, _, upleft, upright = get_page_size()

    pdf_list = [cover_pdf, *main_list]
    page_start_map = make_page_start_map(pdf_list)
    pdf_reader_list = [PdfFileReader(open(pdf_item, 'rb')) for pdf_item in pdf_list]

    pdf_writer = PdfFileWriter()

    for i, pdf_reader in enumerate(pdf_reader_list):
        for page in range(page_start_map[i], pdf_reader.getNumPages()):
            print("processing {}:{}".format(pdf_list[i], page))
            page_obj = pdf_reader.getPage(page)
            page_obj.scaleTo(int(upleft), int(upright))
            pdf_writer.addPage(page_obj)

    print("write pdf object to {}".format(output_name))
    with open(output_name, 'wb') as f:
        pdf_writer.write(f)

def print_page_info(filename):
    with open(filename, 'rb') as fp:
        pdf = PdfFileReader(fp)
        for i in range(pdf.getNumPages()):
            lowleft, lowright, upleft, upright = pdf.getPage(i).mediaBox
            print("{}, {}, {}, {}".format(lowleft, lowright, upleft, upright))

def cover_preprocess(cover_image):
    workdir = 'tmp'
    if not os.path.exists(workdir):
        os.mkdir(workdir)

    to = "{}/{}".format(workdir, os.path.split(cover_image)[1])
    if os.path.splitext(cover_image)[1] == '.pdf':
        shutil.copy(cover_image, to)
        return to
    else:
        cover_pdf = '{}.pdf'.format(os.path.splitext(to)[0])
        jpg2pdf(cover_image, cover_pdf)
        return cover_pdf

if(len(sys.argv) < 2):
    print("Add cover page and merge pdf files")
    print("first page of first pdf file is replaced to cover page")
    print("")
    print("usage:")
    print("    python run.py output_name cover_page pdf1 pdf2 pdf3 ...")
    print("    ex) python run.py output/out2.pdf input/22334307.jpg input/sample.pdf input/dummy.pdf")
    exit(0)

output_name = sys.argv[1]
if os.path.exists(output_name):
    print("Error> output({}) already exists".format(output_name))
    exit(0)

cover_image = sys.argv[2]
if not os.path.exists(cover_image):
    print("Error> cover image({}) does not exists".format(cover_image))
    exit(-1)

main_pdf_list = sys.argv[3:]
for main_pdf in main_pdf_list:
    if not os.path.exists(main_pdf):
        print("Error> pdf({}) does not exists".format(main_pdf))
        exit(-1)

cover_pdf = cover_preprocess(cover_image)

merge_pdf(cover_pdf, main_pdf_list, output_name)

##print_page_info(output_name)
