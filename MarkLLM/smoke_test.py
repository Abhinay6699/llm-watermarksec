import sys
import psutil
import platform
# pyrefly: ignore [missing-import]
import torch
import transformers
import time
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smoke_test")

def print_env():
    print("=" * 50)
    print("ENVIRONMENT")
    print("=" * 50)
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"PyTorch: {torch.__version__}")
    print(f"Transformers: {transformers.__version__}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"GPU Model: {torch.cuda.get_device_name(0)}")
        t = torch.cuda.get_device_properties(0).total_memory
        print(f"GPU VRAM: {t / (1024**3):.2f} GB")
    else:
        print("GPU Model: N/A")
        print("GPU VRAM: N/A")
    mem = psutil.virtual_memory()
    print(f"System RAM: {mem.total / (1024**3):.2f} GB")
    print("=" * 50)

def test_watermark(method_name, transformers_config):
    from watermark.auto_watermark import AutoWatermark
    print(f"\n[{method_name}] Starting Smoke Test")
    
    try:
        my_watermark = AutoWatermark.load(
            method_name, 
            algorithm_config=f'config/{method_name}.json',
            transformers_config=transformers_config
        )
        print(f"[{method_name}] Loaded successfully.")
    except Exception as e:
        print(f"[{method_name}] Failed to load: {e}")
        return
        
    prompt = "The quick brown fox jumps over the lazy dog. Today, we are exploring the impact of artificial intelligence on modern computing. "
    
    # 1. Watermarked
    t0 = time.time()
    try:
        w_text = my_watermark.generate_watermarked_text(prompt)
        t1 = time.time()
        w_detect = my_watermark.detect_watermark(w_text)
        w_time = t1 - t0
        print(f"[{method_name}] Watermarked Text length: {len(w_text)} chars")
        print(f"[{method_name}] Watermarked Detection: {w_detect}, Runtime: {w_time:.2f}s")
    except Exception as e:
        print(f"[{method_name}] Failed in watermarked generation/detection: {e}")

    # 2. Unwatermarked
    t2 = time.time()
    try:
        if hasattr(my_watermark, 'generate_unwatermarked_text'):
            u_text = my_watermark.generate_unwatermarked_text(prompt)
        else:
            inputs = transformers_config.generation_tokenizer(prompt, return_tensors="pt").to(transformers_config.device)
            gen = transformers_config.generation_model.generate(**inputs, **transformers_config.gen_kwargs)
            u_text = transformers_config.generation_tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
            
        t3 = time.time()
        u_detect = my_watermark.detect_watermark(u_text)
        u_time = t3 - t2
        print(f"[{method_name}] Unwatermarked Text length: {len(u_text)} chars")
        print(f"[{method_name}] Unwatermarked Detection: {u_detect}, Runtime: {u_time:.2f}s")
    except Exception as e:
        print(f"[{method_name}] Failed in unwatermarked generation/detection: {e}")

def main():
    print_env()
    
    from utils.transformers_config import TransformersConfig
    from transformers import AutoModelForCausalLM, AutoTokenizer
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Using facebook/opt-1.3b as recommended, or fallback if memory is an issue
    model_name = "facebook/opt-1.3b" 
    
    print(f"\nLoading model {model_name} on {device}...")
    try:
        model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except Exception as e:
        print(f"Failed to load model {model_name}: {e}")
        print("Falling back to facebook/opt-125m...")
        model_name = "facebook/opt-125m"
        model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    transformers_config = TransformersConfig(
        model=model,
        tokenizer=tokenizer,
        vocab_size=50272,
        device=device,
        max_new_tokens=50,
        min_length=10,
        do_sample=True,
        no_repeat_ngram_size=4
    )
    
    test_watermark('KGW', transformers_config)
    test_watermark('Unigram', transformers_config)
    test_watermark('TextSeal', transformers_config)

if __name__ == "__main__":
    main()
