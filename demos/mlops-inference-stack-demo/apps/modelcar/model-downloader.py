from huggingface_hub import snapshot_download

# Specify the Hugging Face repository containing the model
model_repo = "RedHatAI/Llama-3.2-1B-Instruct-quantized.w8a8"
snapshot_download(
    repo_id=model_repo,
    local_dir="/models",
    allow_patterns=["*.safetensors", "*.json", "*.txt"],
)
