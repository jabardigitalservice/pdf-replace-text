EXAMPLE HTTP API TO REPLACE TEXT IN PDF FILE
============================================

Using Python 3 with FastAPI (for HTTP API) and borb (for PDF processing)

## How to install (without docker)
1. clone
1.b. (optional) setup a pip venv `python -m venv .venv ; . ./venv/bin/activate`
2. `pip install -r requirements.txt`

## How to run

- without docker: `uvicorn server:app --port 8000 --host 0.0.0.0 --reload`
- with docker: `docker compose up -d`

## How to use service

```
curl --location 'http://127.0.0.1:8000/process_pdf' \
--form 'file=@"./test.pdf"' \
--form 'old_text="##NOMOR_SURAT##"' \
--form 'new_text="CONTOH AJA"' \
-o hasil.pdf
```
