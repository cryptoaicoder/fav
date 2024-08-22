FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    portaudio19-dev \
    swig \
    libpulse-dev \
    libasound2-dev \
    espeak \
    curl

RUN pip3 install SpeechRecognition pocketsphinx pyaudio requests pyttsx3

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

# Copy your Python script
COPY speech_assistant.py /app/speech_assistant.py

# Copy a startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

WORKDIR /app

CMD ["/app/start.sh"]
