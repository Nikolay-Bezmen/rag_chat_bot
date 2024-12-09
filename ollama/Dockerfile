# Start with an official Ollama image as the base image
FROM ollama/ollama:latest

# Set environment variables for Ollama
ENV MODELS_DIR=/models
ENV OLLAMA_HOST=0.0.0.0
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Create and set the working directory
WORKDIR /ollama

# Pull the llama2 model
RUN ollama pull llama2

# Expose the necessary port for API interaction
EXPOSE 11434

# Run the Ollama server when the container starts
CMD ["serve"]
