from datasets import load_dataset_builder, load_dataset

def inspect(ds_name):
    print(f"\n--- {ds_name} ---")
    try:
        # c4 needs explicit config, usually 'en' for English C4, wikitext needs 'wikitext-103-raw-v1' or similar
        if ds_name == 'allenai/c4':
            config_name = 'en'
        elif ds_name == 'Salesforce/wikitext':
            config_name = 'wikitext-103-raw-v1'
        else:
            config_name = None
            
        builder = load_dataset_builder(ds_name, config_name)
        print("Configs:", builder.builder_configs.keys() if builder.builder_configs else "Default")
        print("Info:", builder.info.description[:200])
        
        ds = load_dataset(ds_name, config_name, split="train", streaming=True)
        sample = next(iter(ds))
        print("Keys:", sample.keys())
        for k, v in sample.items():
            print(f"Sample [{k}]: {str(v)[:200]}")
    except Exception as e:
        print("Error:", e)

inspect('allenai/c4')
inspect('Salesforce/wikitext')
