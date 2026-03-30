# Containerfile for packaging Quadlet manifests as OCI image
# FlightCtl agent will extract and deploy these quadlet files as systemd units

FROM scratch

# Metadata labels for image identification
LABEL org.opencontainers.image.title="Inference Stack Quadlet"
LABEL org.opencontainers.image.description="Systemd quadlet files for deploying model-car, vLLM, OpenWebUI, and vllm-bench with 6-minute timer"
LABEL app.type="quadlet"
LABEL app.runtime="podman"

# Copy quadlet container definitions
COPY model-car.container /model-car.container
COPY vllm-server.container /vllm-server.container
COPY vllm-bench.container /vllm-bench.container
COPY vllm-bench.timer /vllm-bench.timer
COPY openwebui.container /openwebui.container

# Copy quadlet volume definitions
COPY model-storage.volume /model-storage.volume
COPY openwebui-data.volume /openwebui-data.volume

# Copy quadlet network definition
COPY mlops.network /mlops.network

