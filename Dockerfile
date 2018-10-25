# Run from official python runtime
FROM python:3.6

# Set working directory
WORKDIR /bot

# Copy contents into working directory
COPY . /bot

# Install requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Start duckbot
CMD ["python", "duckbot/main.py"]
