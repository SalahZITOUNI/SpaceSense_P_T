# Internship Take Home Assignment - Software Engineer
# User Manuel competence test SpaceSense
The following Manuel or readme file will include the following parts:

1. **before starting.**
2. **Prepearing the environment.**
3. **Creating Docker container.**
4. **Testing the back-end features with docker.**
5. **Testing the back-end features without using docker.**


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

2. **Prepearing the environment:**

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

3. **Creating Docker container:**

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

4. **Testing the back-end features with docker:**

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

5** Testing the back-end features without using docker:**

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
