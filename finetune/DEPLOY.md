# Deploy fine-tuned model on RunPod (GPU, cheapest for real inference speed)

Why RunPod not Railway: Railway has no GPU, Ollama would run CPU-only (very slow
for a 7B model). RunPod gives per-second GPU billing.

## 1. Get your GGUF file
From the Colab notebook, either:
- Download `my-coder-model/*.gguf` directly, or
- Push it to your Hugging Face account (`push_to_hub_gguf` cell) — easier to
  pull from RunPod later.

## 2. Spin up a RunPod GPU pod
- Go to runpod.io -> Deploy -> Pod
- Template: search "Ollama" (community template) or use a plain
  `runpod/pytorch` image
- GPU: RTX 4090 ($0.30-0.40/hr) is enough for a 7B q4_k_m model
- Attach a volume (20GB+) so the model persists across restarts

## 3. Inside the pod
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &

# pull your gguf (from HF) or scp it in, then:
ollama create my-coder-model -f Modelfile
ollama run my-coder-model "write a go function to reverse a linked list"
```

## 4. Expose an OpenAI-compatible API
Ollama already serves an OpenAI-compatible endpoint at
`http://<pod-ip>:11434/v1/chat/completions`. Point your editor / CLI tool
(e.g. Continue.dev, aider, custom script) at this URL instead of the
Anthropic/OpenAI API to cut costs.

## 5. Cost control
- Stop the pod when not coding (RunPod bills per second while running)
- For steady 24/7 usage, compare RunPod Serverless (worker-ollama template)
  which scales to zero when idle: https://github.com/runpod-workers/worker-ollama

## Alternative (CPU-only, free-ish): Railway + llama.cpp template
If speed doesn't matter (e.g. batch jobs, not interactive coding), Railway's
LLaMA.cpp template can run a small quantized GGUF on CPU. Not recommended for
interactive "senior dev" style coding assistance — latency will be high.
