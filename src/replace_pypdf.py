import os
import argparse
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, NameObject

def replace_text(content, replacements = dict()):
    lines = content.splitlines()

    result = ""
    in_text = False

    for line in lines:
        if line == "BT":
            in_text = True

        elif line == "ET":
            in_text = False

        elif in_text:
            cmd = line[-2:]
            if cmd.lower() == 'tj':
                replaced_line = line
                for k, v in replacements.items():
                    replaced_line = replaced_line.replace(k, v)
                result += replaced_line + "\n"
            else:
                result += line + "\n"
            continue

        result += line + "\n"

    return result


def process_data(object, replacements):
    data = object.get_data()
    decoded_data = data.decode('utf-8')

    replaced_data = replace_text(decoded_data, replacements)

    encoded_data = replaced_data.encode('utf-8')
    if object.decoded_self is not None:
        object.decoded_self.set_data(encoded_data)
    else:
        object.set_data(encoded_data)

def replace_text_in_pdf(input_filename, output_filename, replaced_text, new_text):
    pdf = PdfReader(input_filename)
    writer = PdfWriter()
    replacements = { replaced_text: new_text }

    for page in pdf.pages:
        contents = page.get_contents()

        if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
            process_data(contents, replacements)
        elif len(contents) > 0:
            for obj in contents:
                if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                    streamObj = obj.getObject()
                    process_data(streamObj, replacements)

        # Force content replacement
        page[NameObject("/Contents")] = contents.decoded_self
        writer.add_page(page)

    with open(output_filename, 'wb') as out_file:
        writer.write(out_file)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to PDF document")
    args = vars(ap.parse_args())

    in_file = args["input"]
    filename_base = in_file.replace(os.path.splitext(in_file)[1], "")
    out_file = filename_base + ".result.pdf"

    replace_text_in_pdf(
        in_file,
        out_file,
        "##NOMOR_SURAT##",
        "hasil",
    )

