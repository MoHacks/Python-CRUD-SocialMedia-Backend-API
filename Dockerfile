FROM python:3.12.4-bookworm

# where all the commands are going to run from
WORKDIR /usr/src/app

# Copy all dependencies from requirements.txt into the image's /usr/src/app
COPY requirements.txt ./

# install all dependencies in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy everthing in current directory to the WORKDIR image
COPY . .

# command to run when starting the container (runs the server)
# CMD ["uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]