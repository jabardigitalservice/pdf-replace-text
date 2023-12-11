# generated by ChatGPT: https://chat.openai.com/share/e3136c18-6b8c-4c5e-98a9-a1a22a6fb2a1
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

import src.replace_pypdf as replacer

app = FastAPI()

# Allow all origins for simplicity. In production, you may want to restrict this.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>                                                      
        <head>
                <title>replace text in pdf</title>                  
        </head>
        <body>
                <h1>example request replace text in pdf</h1>
                <form method=POST action="/process_pdf" enctype="multipart/form-data">
                    <label>pdf file</label>                                 
                    <input type="file" name="file"/>
                    <br/>

                    <label>old text</label>                                 
                    <input type="text" name="old_text"/>                    
                    <br/>
                                 
                    <label>new_text</label>
                    <input type="text" name="new_text"/>                    
                    <br/>
                                                                            
                    <button>submit</button>                             
                </form>
        </body>
    </html>                                             
    """

@app.post("/process_pdf")
async def process_pdf_endpoint(
    file: UploadFile = Form(...),
    old_text: str = Form(...),
    new_text: str = Form(...),
):
    try:
        original_filename = file.filename
        # Save the uploaded PDF file to a temporary location
        with open(original_filename, "wb") as pdf_content:
            shutil.copyfileobj(file.file, pdf_content)

        # Process the PDF and get the output file path
        new_filename = "new_" + original_filename
        replacer.replace_text_in_pdf(
            original_filename,
            new_filename,
            old_text,
            new_text
        )

        # Return the processed file
        return FileResponse(new_filename, media_type="application/pdf")

    except Exception as e:
        # Handle errors and return an error message
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

    finally:
        # Clean up: Remove the temporary PDF file
        os.remove(file.filename)

