import os
import json
import logging
import datasets
from transformers import AutoTokenizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prepare_datasets")

SEED = 42
datasets.config.STREAMING_READ_MAX_RETRIES = 5
datasets.config.STREAMING_READ_RETRY_INTERVAL = 2

def is_wikitext_header(text):
    t = text.strip()
    if not t:
        return True
    if t.startswith('=') and t.endswith('='):
        return True
    return False

def main():
    out_dir = "experiments/baseline/dataset"
    os.makedirs(out_dir, exist_ok=True)
    
    try:
        tokenizer = AutoTokenizer.from_pretrained("facebook/opt-1.3b")
        model_name = "facebook/opt-1.3b"
    except:
        tokenizer = AutoTokenizer.from_pretrained("facebook/opt-125m")
        model_name = "facebook/opt-125m"

    samples = []
    stats = {
        "c4_rejected": 0,
        "c4_duplicates": 0,
        "wiki_rejected": 0,
        "wiki_duplicates": 0,
        "prompt_lengths": []
    }
    seen_texts = set()

    def process_dataset(ds_id, config, split, target_count, name, is_wiki=False):
        logger.info(f"Loading {ds_id}...")
        try:
            ds = datasets.load_dataset(ds_id, config, split=split, streaming=True)
            ds = ds.shuffle(seed=SEED, buffer_size=10000)
            
            count = 0
            for row in ds:
                text = row['text']
                
                if is_wiki and is_wikitext_header(text):
                    stats[f"{name}_rejected"] += 1
                    continue
                    
                if not text.strip():
                    stats[f"{name}_rejected"] += 1
                    continue
                    
                if text in seen_texts:
                    stats[f"{name}_duplicates"] += 1
                    continue
                    
                tokens = tokenizer.encode(text, add_special_tokens=False)
                if len(tokens) < 50:
                    stats[f"{name}_rejected"] += 1
                    continue
                    
                prompt_tokens = tokens[:50]
                prompt_text = tokenizer.decode(prompt_tokens)
                
                sample_id = f"{name}_{count}"
                samples.append({
                    "sample_id": sample_id,
                    "dataset": ds_id,
                    "dataset_config": config,
                    "split": split,
                    "original_text": text,
                    "prompt_text": prompt_text,
                    "source": row.get('url', row.get('title', '')),
                    "seed": SEED,
                    "prompt_token_count": len(prompt_tokens)
                })
                seen_texts.add(text)
                stats["prompt_lengths"].append(len(prompt_tokens))
                count += 1
                if count >= target_count:
                    break
            return count
        except Exception as e:
            print(f"\nNETWORK_ERROR on {ds_id}: {e}\n")
            import sys
            sys.exit(1)

    c4_count = process_dataset("allenai/c4", "en", "train", 30, "c4")
    wiki_count = process_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", "test", 30, "wiki", is_wiki=True)

    with open(os.path.join(out_dir, "samples.jsonl"), "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")
            
    config_data = {
        "dataset_ids": ["allenai/c4", "Salesforce/wikitext"],
        "configurations": ["en", "wikitext-103-raw-v1"],
        "splits": ["train", "test"],
        "sampling_seed": SEED,
        "requested_sample_count": 60,
        "actual_sample_count": len(samples),
        "preprocessing_rules": "C4: remove < 50 tokens. WikiText: remove headers (= Title =) and < 50 tokens.",
        "model_tokenizer": model_name
    }
    with open(os.path.join(out_dir, "dataset_config.json"), "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)
        
    readme_content = f"""# Baseline Dataset
60 samples selected (30 C4, 30 WikiText-103).
Seed: {SEED}
Tokenizer: {model_name}
Prompt extraction: First 50 tokens.
"""
    with open(os.path.join(out_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("=== VALIDATION ===")
    print(f"C4: {c4_count} valid samples")
    print(f"WikiText-103: {wiki_count} valid samples")
    print(f"Total: {len(samples)} samples")
    if stats["prompt_lengths"]:
        print(f"Minimum prompt token count: {min(stats['prompt_lengths'])}")
        print(f"Maximum prompt token count: {max(stats['prompt_lengths'])}")
        print(f"Average prompt token count: {sum(stats['prompt_lengths'])/len(stats['prompt_lengths']):.2f}")
    print(f"Number of rejected samples (C4): {stats['c4_rejected']}")
    print(f"Number of rejected samples (Wiki): {stats['wiki_rejected']}")
    print(f"Number of duplicate samples: {stats['c4_duplicates'] + stats['wiki_duplicates']}")
    print(f"Dataset path: {os.path.abspath(out_dir)}")

if __name__ == "__main__":
    main()
