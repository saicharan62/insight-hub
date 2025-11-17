import time
import torch
from transformers import pipeline

def benchmark_pipeline(model_name, device):
    print(f"\n🚀 Benchmarking: {model_name} | Device: {'GPU' if device == 0 else 'CPU'}")

    summarizer = pipeline("summarization", model=model_name, device=device)
    content = (
        "Today I decided to re-start DSA and almost got started but somehow deviated towards projects environment setup. "
        "I installed Oracle XE in Docker, configured PostgreSQL, debugged multi-version Python issues, and integrated SQLAlchemy ORM. "
        "Finally, I connected HuggingFace transformers to summarize text with GPU acceleration."
    )

    warmup_runs, test_runs = 1, 5
    # Warmup (to cache model)
    summarizer(content, max_length=130, min_length=30, do_sample=False)

    times = []
    for i in range(test_runs):
        start = time.time()
        result = summarizer(content, max_length=130, min_length=30, do_sample=False)
        end = time.time()
        times.append(end - start)
        print(f"Run {i+1}: {round(times[-1], 3)}s → {result[0]['summary_text'][:60]}...")

    avg_time = sum(times) / len(times)
    print(f"\n✅ Avg inference time: {round(avg_time, 3)}s over {test_runs} runs")
    print(f"🔥 Speed gain factor vs CPU (if compared): {(5.5 / avg_time):.1f}x approx\n")

    if torch.cuda.is_available():
        print(f"VRAM Usage: {torch.cuda.memory_allocated() / 1e9:.2f} GB / {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB\n")
    else:
        print("Running on CPU (no VRAM stats available)\n")

if __name__ == "__main__":
    device = 0 if torch.cuda.is_available() else -1
    benchmark_pipeline("facebook/bart-large-cnn", device)
