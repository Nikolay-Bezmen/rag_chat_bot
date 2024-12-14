# Ollama TinyLlama Setup

This guide explains how to build, configure, and run a Docker container for the TinyLlama model using Ollama. Follow the steps below to get started.

## Steps to Build and Run

### 1. Build the Docker Image
First, create a Docker image using the provided Dockerfile. Run the following command:

```bash
docker build -t ollama-image .
```
### 2. Start the Initial Container
Run a container using the base image and expose the necessary port:
```bash
docker run -d --name ollama-tinyllama-loader -p 11434:11434 ollama-base
```
### 3.  Pull the TinyLlama Model
Inside the running container, pull the TinyLlama model using the Ollama CLI:
```bash
docker exec -it ollama-tinyllama-loader ollama pull tinyllama
```
### 4. Commit the Container to a New Image
Save the current state of the container as a new Docker image:
```bash
docker build -t ollamadocker commit ollama-tinyllama-loader ollama-tinyllama-image .
```
### 5.  Run the Final TinyLlama Container
Start a new container based on the ollama-tinyllama image:
```bash
docker run -d --name tinyllama-container -p 1145:11434 -e OLLAMA_HOST=0.0.0.0:11434 ollama-tinyllama
```