# from https://stackoverflow.com/a/75574195
from borb.pdf import Document
from borb.pdf import PDF
from borb.toolkit import SimpleFindReplace

import typing

def replace_text_in_pdf(input_filename, output_filename, replaced_text, new_text):

    # attempt to read a PDF
    doc: typing.Optional[Document] = None
    with open(input_filename, "rb") as pdf_file_handle:
        doc = PDF.loads(pdf_file_handle)

    # check whether we actually read a PDF
    assert doc is not None

    # find/replace
    doc = SimpleFindReplace.sub(replaced_text, new_text, doc)

    # store
    with open(output_filename, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)


if __name__ == "__main__":
    replace_text_in_pdf(
        "test.pdf",
        "result.pdf",
        "{{nomor_surat}}",
        "hasil"
    )
