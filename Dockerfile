# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable for the bot token
ENV TELEGRAM_API_TOKEN=your-telegram-bot-token

# Command to run the bot
CMD ["python", "megabot.py"]
