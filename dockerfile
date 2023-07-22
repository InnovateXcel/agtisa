# Use the official Python base image
FROM python

# Set the working directory inside the container to /agtisa
WORKDIR /agtisa

# Copy your images, audios, and libraries to the container's working directory
COPY images/ /agtisa/images/
COPY audios/ /agtisa/audios/
COPY codes/ /agtisa/codes/
COPY ABSTRACT_AGTISA.docx /agtisa/

# Copy the requirements.txt file to the container's working directory
COPY requirements.txt /agtisa/

# Install the Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Display the instruction message when the container starts
ENTRYPOINT echo -e "Agtisa docker container has started and is running\nThis a is help for your reference\nUse '/agtisa/<file_name>' to specify the path\nPaths:\nImages - /agtisa/images\nAudios - /agtisa/audios\nContents:\n- car.png\n- background.jpg\n- pedals.png\n- exit.png\n- location.png\n- menu.png\n- start.png\n- warning.png\nAudios:\n- beep.mp3\n- brake_sound.mp3\n- engine_sound.mp3" && tail -f /dev/null