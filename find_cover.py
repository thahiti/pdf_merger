import sys
import os

pdf_dir = sys.argv[1]
cover_dir = sys.argv[2]

pdf_list = os.listdir(pdf_dir)
cover_list = os.listdir(cover_dir)

matched_list = dict()
not_found_list = []

def matched(a, b):
    a = os.path.splitext(a)[0]
    b = os.path.splitext(b)[0]
    if a == b:
        return True
    if a.replace(' ', '') == b.replace(' ', ''):
        return True
    if a.replace(' ', '_') == b.replace(' ', ''):
        return True
    if a.replace(' ', '_').lower() == b.replace(' ', '').lower():
        return True
    if a.replace(' ', '_').lower() == b.replace(' ', '').lower():
        return True
    if a.replace(' ', '_').lower()[:-1] == b.replace(' ', '').lower():
        return True
    if a.lower()[:-1] == b.lower():
        return True
    if a.startswith(b):
        return True
    return False

def find_cover(pdf, cover_list):
    for cover in cover_list:
        if matched(pdf, cover):
            return cover
    return None

for pdf in pdf_list:
    cover = find_cover(pdf, cover_list)
    if cover:
        if cover not in matched_list.keys():
            matched_list[cover] = []
        matched_list[cover].append(pdf)
        matched_list[cover].sort()
    else:
        not_found_list.append(pdf)

multiple_item = []

if False:
    for cover, pdf in matched_list.items():
        if(len(pdf) > 1):
            multiple_item.append(cover)
        print("{}:{}".format(cover, pdf))

    for pdf in multiple_item:
        print("multiple for {}".format(pdf))
        print(matched_list[pdf])

    for pdf in not_found_list:
        print("Not found for {}".format(pdf))

    print("found, {}".format(len(matched_list)))
    print("not found, {}".format(len(not_found_list)))
else:
    output_path = "output"
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for cover, pdf in matched_list.items():
        title = os.path.split(pdf[0])[1]
        pdfs = ("{} "*len(pdf)).format(*pdf)
        os.system('python run.py "{}/{}" "{}/{}" "{}/{}"'.format(output_path, title,
                                                       cover_dir, cover,
                                                       pdf_dir, pdfs))
