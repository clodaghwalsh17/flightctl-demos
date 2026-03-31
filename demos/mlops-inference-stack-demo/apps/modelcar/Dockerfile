# Stage 1: Download model
FROM registry.access.redhat.com/ubi9/python-311:latest AS base

USER root

# Install huggingface-hub
RUN pip install huggingface-hub

# Copy the model download script
COPY model-downloader.py .

# Download the model (HF_TOKEN via build secret or env var)
RUN --mount=type=secret,id=HF_TOKEN,env=HF_TOKEN \
    python model-downloader.py

# Stage 2: Final minimal image with model files
FROM registry.access.redhat.com/ubi9/ubi-micro:9.7

# Copy only the model files from the build stage
COPY --from=base /models /models

USER 1001
