# in Docker, it is common to base a new image on a previously-created image
FROM python:3.11-slim-buster

# Set the working directory in the image
WORKDIR /app

# BEFORE BUILDING AN IMAGE, run "pipenv requirements > requirements.txt" in terminal to make sure requirements.txt is up to date with Pipfile contents

# install dependencies into the image - doing this first will speed up subsequent builds, as Docker will cache this step
COPY /requirements.txt ./
RUN pip3 install -r requirements.txt

# the ADD command is how you add files from your local machine into a Docker image
# Copy the current directory contents into the container at /app
ADD . .

# expose the port that the Flask app is running on... by default 5000
EXPOSE 5000

# # Run app.py when the container launches
# CMD [ "gunicorn", "app:create_app()" ]
CMD [ "python3", "-m" , "flask", "-A", "web-app/app.py", "run", "-h", "0.0.0.0" ]