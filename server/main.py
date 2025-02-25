import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.embeddings import process_pdfs
from services.rag_model import get_answer
from routes.pdf_routes import pdf_routes

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

UPLOAD_FOLDER = 'models/pdf'
ALLOWED_EXTENSIONS = {'pdf'}

app.include_router(pdf_routes, prefix="/pdf")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")  # Log received file name
    if not allowed_file(file.filename):
        print("Invalid file type")
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    try:
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            print(f"Created upload folder: {UPLOAD_FOLDER}")

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        print(f"Saving file to {file_path}")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        print(f"File saved to {file_path}")  # Log file save location
        
        # Process the newly uploaded PDF
        try:
            print(f"Processing PDF: {file_path}")
            process_pdfs(file_path)
            print(f"PDF processed successfully: {file_path}")
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
        
        print("File uploaded and processed successfully")
        return {"message": "File uploaded and processed successfully"}
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
@app.post("/ask")
async def ask_question(question: str):
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")
    answer = get_answer(question)
    return {"answer": answer}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)