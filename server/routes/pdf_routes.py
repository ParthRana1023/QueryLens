from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from typing import List
from services.embeddings import process_pdfs
from fastapi import File, UploadFile 

pdf_routes = APIRouter()

PDF_FOLDER = 'services/pdf'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pdf_routes.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")  # Log received file name
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    try:
        if not os.path.exists(PDF_FOLDER):
            os.makedirs(PDF_FOLDER)
            print(f"Created upload folder: {PDF_FOLDER}")

        file_path = os.path.join(PDF_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        print(f"File saved to {file_path}")  # Log file save location
        
        # Process the newly uploaded PDF
        try:
            process_pdfs(file_path)
            print(f"PDF processed successfully: {file_path}")
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
        
        return {"message": "File uploaded and processed successfully"}
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@pdf_routes.get("/view/{filename}")
async def view_pdf(filename: str):
    """
    Route to view a PDF file.
    """
    file_path = os.path.join(PDF_FOLDER, filename)
    
    if os.path.exists(file_path):
        headers = {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'inline; filename="{}"'.format(filename)
        }
        return FileResponse(
            path=file_path, 
            headers=headers, 
            media_type='application/pdf'
        )
    else:
        raise HTTPException(status_code=404, detail="PDF not found")

@pdf_routes.delete("/delete/{filename}")
async def delete_pdf(filename: str):
    """
    Route to delete a PDF file.
    """
    file_path = os.path.join(PDF_FOLDER, filename)
    
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"message": f"PDF {filename} deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete PDF: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="PDF not found")

@pdf_routes.get("/list", response_model=List[dict])
async def list_pdfs():
    """
    Route to list all PDF files with their creation timestamps.
    """
    try:
        pdf_files = []
        for f in os.listdir(PDF_FOLDER):
            if f.endswith('.pdf'):
                file_path = os.path.join(PDF_FOLDER, f)
                creation_time = os.path.getctime(file_path)
                pdf_files.append({
                    "name": f,
                    "created": creation_time
                })
        # Sort by creation time, newest first
        pdf_files.sort(key=lambda x: x["created"], reverse=True)
        return pdf_files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list PDFs: {str(e)}")