# Internship Take Home Assignment - Software Engineer
# User Manuel competence test SpaceSense
The following Manuel or readme file will include the following parts:

1. **before starting.**
2. **clone the repository.**
4. **Prepearing the environment.**
5. **Creating Docker container.**
6. **Testing the back-end features with docker.**
7. **Testing the back-end features without using docker.**
8. **the code of the main applicatin.**


## Instructions:

1. **1-before starting:**
Before start testing our program, please make sure that you are using a recent version of Docker it is a very critical part of the testing process.

In case you don’t have it installed on your device, you can easily download it on Windows from Docker site and all Docker features will be automatically installed.

On Linux with Ubuntu distribution:

```bash
sudo apt install docker.io
 ```

always cheek the Docker site to have it properly installed.

On the other hand, if you are using Linux with Ubuntu distribution as I did its crucial to have docker compose installed. You can easily install it using the apt library using the following instruction:


    ```bash
    Sudo apt install docker compose.
    ```
or

    ```bash
    sudo apt-get install docker-compose-plugin
    ```
There are so many ways to install it!

2. **clone the repository:**

To clone the repository Navigate to the directory where you want the cloned directory to be added.
Run the git clone command:

  ```bash
  git clone https://github.com/SalahZITOUNI/SpaceSense_P_T.git
  ```

3. **Prepearing the environment:**

To prepare the environment to have a back-end compatibility, we need to modify the file requirements.txt to include the necessary libraries so that our program work properly:

    ```bash
        torch
    torchvision
    timm
    opencv-python
    git+https://github.com/dhkim2810/MobileSAM.git
    matplotlib
    numpy
    fastapi
    uvicorn[standard]
    numpy
    Pillow
    python-multipart
    ```
those libraries will assure that our main program main.py will function without problems:  

4. **Creating Docker container:**

Creating Docker container in a crucial part of the test because this container will be the server where our program will work, and it will also assure that the program and its files will be separated from the main computer which will work as a layer of protection and will facilitate the tests.

I. **Create docker file:**

The docker file is very important when you create a container because this file will include the settings on how this container will works, the location of the score’s files, preparing the virtual environment by downloading the python dependencies and le URL of the application:

   ```bash
   # Use the specified image as the base
   FROM python:3.10.12

   # Set a directory for the app
   WORKDIR /usr/src/app

   # Install system dependencies for OpenCV
   RUN apt-get update \
       && apt-get install -y --no-install-recommends libgl1 \
       && rm -rf /var/lib/apt/lists/*

   # Install Python dependencies
   COPY requirements.txt ./
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy the current directory contents into the container at /usr/src/app
   COPY . .

   # Correct the command to run the application
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

II. **Create docker composer file:**

The docker composer file will include the version of the container its ports, its IP address, and the application web:

    ```bash
    version: '3.9'
    
    services:
      web:
        build: .
        command: sh -c "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
        ports:
          - "8000:8000"
        volumes:
          - .:/usr/src/app
    
        ```

III. **compose the container:**
To compose the container you will need to go the location of your files,main.py ,Dockerfile , Docker composer …etc

Now you lunch the docker composer using the following instruction:

  ```bash
  sudo docker-compose -f /home/salah/SpaceSense/mobilesam-task/docker-compose.yaml up –build
  ```

make sur always to choose the correct path :

    ```bash
    sudo docker-compose -f /”your file location”/docker-compose.yaml up –build
    ```

it will take between five and seven minutes to create the container and lunch the application. 

In case it hasn’t lunch the application on your browser you can lunch the application using the following link:

http://localhost:8000/

5. **Testing the back-end features with docker:**

now after you clicked on the link it will open the following page:

As it’s demanded in the assignment we used a back-end API and we followed your suggestion and we have used Fast API, we have chosen fast API as it provides a good documentation and clear way to test the back-end features without the need to develop HTML interface.

To test it you will need to go to the following line:

http://localhost:8000/docs


now after you clicked on the link it will open the following page:

![Capture d'écran 2024-01-28 143723](https://github.com/SalahZITOUNI/SpaceSense_P_T/assets/157633302/69707120-421b-45bd-9326-f7d74cd203eb)
 
Now we tested by choosing an image to segment it:

![Capture d'écran 2024-01-28 143904](https://github.com/SalahZITOUNI/SpaceSense_P_T/assets/157633302/ce73f1e4-d5ed-4517-a717-37345ec1de20)

![Capture d'écran 2024-01-28 143927](https://github.com/SalahZITOUNI/SpaceSense_P_T/assets/157633302/eb5326fe-41a5-4657-b71b-08ebf8ffd71f)

![Capture d'écran 2024-01-28 144153](https://github.com/SalahZITOUNI/SpaceSense_P_T/assets/157633302/7c787264-8509-4aaa-b5a3-d10e6da86656)

![Capture d'écran 2024-01-28 144328](https://github.com/SalahZITOUNI/SpaceSense_P_T/assets/157633302/38ef923c-29d1-4bf6-9f22-d2a6c66c647b)


And as we test with many images, we can say that our back-end feature is fully functional which mean the back-end feature works well.

6** Testing the back-end features without using docker:**

To test the application without using docker you need to create virtual environment:

    ```bash
    python -m venv venv    #on windows
    python3 -m venv venv   #on Linux
    ```

then activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

then you will need to install to requirement on the virtual environment:

    ```bash
    pip install -r requirements.txt
    ```

and finally, you will need to start the unicorn server:


    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
the rest of the testing as we did before.

**Title:** P.S:

You may counter errors with the promotion access to folders generated and temp while testing without Docker.

You can override it using the following two commands lines:

    ```bash
    sudo chmod 777 generated
    ```
and :

    ```bash
    sudo chmod 777 temp
    ```
 7. **the code of the main applicatin:**

        ```bash
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
        # Optional: Add a root endpoint for health check or instructions
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
    ```
