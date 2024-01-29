#Here we start by importing necessary libraries
import os
import numpy as np
import torch
from mobile_sam import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry
from PIL import Image
from tools import  fast_process  
import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import torch
from mobile_sam import SamAutomaticMaskGenerator, sam_model_registry
from datetime import datetime
from fastapi.responses import HTMLResponse
# Starting the Back-end application using Fast API 
app = FastAPI()

# Check the device to check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Mount a static directory to seve the generated images
app.mount("/generated", StaticFiles(directory="generated"), name="generated")

# Load the model mobile_sam on application startup
@app.on_event("startup")
def load_model():
    device = torch.device("cpu")
    sam_checkpoint = "mobile_sam.pt"
    model_type = "vit_t"
    mobile_sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    mobile_sam.to(device=device)
    mobile_sam.eval()
    global mask_generator
    mask_generator = SamAutomaticMaskGenerator(mobile_sam)
#the segment image from the original code 
@torch.no_grad()
def segment_everything(
    image,
    input_size=1024,
    better_quality=False,
    withContours=True,
    use_retina=True,
    mask_random_color=True,
):
    global mask_generator

    input_size = int(input_size)
    w, h = image.size
    scale = input_size / max(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    image = image.resize((new_w, new_h))

    nd_image = np.array(image)
    annotations = mask_generator.generate(nd_image)

    fig = fast_process(
        annotations=annotations,
        image=image,
        device=device,
        scale=(1024 // input_size),
        better_quality=better_quality,
        mask_random_color=mask_random_color,
        bbox=None,
        use_retina=use_retina,
        withContours=withContours,
    )
    return fig



if __name__ == "__main__":
    input_path = "resources/dog.jpg"
    output_path = "generated/output.png"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    image = Image.open(input_path).convert("RGB")
    fig = segment_everything(
        image=image
    )
    fig.save(output_path)

# Create a POST endpoint /segment-image to accept an image file, process it through MobileSam
@app.post("/segment-image/")
async def segment_image(file: UploadFile = File(...)):
    try: # to avoids errors 
        # Save uploaded file
        input_path = f"temp/{file.filename}"
        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Load and process image using the function provided with the original code 
        image = Image.open(input_path).convert("RGB")  # Ensure image is in RGB mode
        fig = segment_everything(image=image)

        # Specify output format based on file extension or convert to a compatible format
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") #set the time of segmentation
        output_filename = f"{file.filename.rsplit('.', 1)[0]}_{timestamp}.png" # naming format
        output_path = f"generated/{output_filename}" #chose the path of the generated image 
        os.makedirs(os.path.dirname(output_path), exist_ok=True) # cheak if the file existe
        fig.save(output_path, "PNG")  # Save as PNG to support transparency

        # Clean up the input file / the temp file 
        os.remove(input_path)

        # Return processed image to show it on the fast API application
        return FileResponse(output_path)
    except Exception as e:
        # Log the exception (use logging in production)
        print(f"An error occurred: {str(e)}")
        # Return a JSON response that contain the error details
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred during image processing.", "detail": str(e)}
        )
#Add a root endpoint for health check and to show welcome message
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>MobileSAM Segmentation API</title>
        </head>
        <body>
            <h1>Welcome to the MobileSAM segmentation API</h1>
            <p>Using FastAPI by Salah ZITOUNI.</p>
            <p>Access to the documentation and make tests <a href="/docs" target="_blank">here</a>.</p>
        </body>
    </html>
    """
