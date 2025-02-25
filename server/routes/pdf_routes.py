from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
import os
from typing import List

pdf_routes = APIRouter()

PDF_FOLDER = 'models/pdf'

@pdf_routes.get("/view/{filename}")
async def view_pdf(filename: str):
    """
    Route to view a PDF file.
    """
    file_path = os.path.join(PDF_FOLDER, filename)
    
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename=filename)
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

@pdf_routes.get("/list", response_model=List[str])
async def list_pdfs():
    """
    Route to list all PDF files.
    """
    try:
        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
        return pdf_files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list PDFs: {str(e)}")