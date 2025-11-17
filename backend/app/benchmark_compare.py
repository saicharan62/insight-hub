import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# move one level up to access the 'app' package correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import torch
from transformers import pipeline
from app.db import SessionLocal
from app.models.benchmark import BenchmarkResult



def benchmark(model_name, device, runs=3):
    """
    Benchmark summarization pipeline on specified device (CPU=-1, GPU=0)
    """
    label = "GPU" if device == 0 else "CPU"
    print(f"\n🚀 Benchmarking: {model_name} | Device: {label}")

    summarizer = pipeline("summarization", model=model_name, device=device)
    text = (
        "Today I decided to re-start DSA and almost got started but somehow deviated towards projects environment setup. "
        "I installed Oracle XE in Docker, configured PostgreSQL, debugged multi-version Python issues, and integrated SQLAlchemy ORM. "
        "Finally, I connected HuggingFace transformers to summarize text with GPU acceleration."
    )

    # Warm-up (model caching)
    summarizer(text, max_length=130, min_length=30, do_sample=False)

    times = []
    for i in range(runs):
        start = time.time()
        summarizer(text, max_length=130, min_length=30, do_sample=False)
        duration = time.time() - start
        times.append(duration)
        print(f"   Run {i+1}: {round(duration, 3)}s")

    avg_time = sum(times) / len(times)
    print(f"✅ Avg inference time ({label}): {round(avg_time, 3)}s")

    if device == 0 and torch.cuda.is_available():
        vram_used = torch.cuda.memory_allocated() / 1e9
        vram_total = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"🧠 VRAM: {vram_used:.2f} GB / {vram_total:.2f} GB")

    return avg_time


def compare_cpu_gpu():
    model_name = "facebook/bart-large-cnn"

    print("⚙️  Starting InsightHub NLP Benchmark...\n")
    if torch.cuda.is_available():
        print(f"Detected GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️  No CUDA-compatible GPU detected — only CPU mode will run.")

    print("-" * 70)
    cpu_time = benchmark(model_name, device=-1)  # ✅ assign to variable
    print("-" * 70)
    gpu_time = benchmark(model_name, device=0 if torch.cuda.is_available() else -1)  # ✅ assign to variable
    print("-" * 70)

    if torch.cuda.is_available():
        gain = cpu_time / gpu_time
        print(f"⚡ Performance Boost: {gain:.1f}x faster on GPU vs CPU 🚀")

        # ✅ Save results to DB
        from app.db import SessionLocal
        from app.models.benchmark import BenchmarkResult

        db = SessionLocal()
        try:
            entry_gpu = BenchmarkResult(
                model_name=model_name,
                device="GPU",
                avg_time=round(gpu_time, 3),
                vram_used_gb=round(torch.cuda.memory_allocated() / 1e9, 2),
                vram_total_gb=round(torch.cuda.get_device_properties(0).total_memory / 1e9, 2)
            )
            entry_cpu = BenchmarkResult(
                model_name=model_name,
                device="CPU",
                avg_time=round(cpu_time, 3)
            )
            db.add_all([entry_cpu, entry_gpu])
            db.commit()
            print("📦 Logged benchmark results to database successfully!")
        finally:
            db.close()
    else:
        print("💻 CPU-only mode completed successfully.")




if __name__ == "__main__":
    compare_cpu_gpu()
