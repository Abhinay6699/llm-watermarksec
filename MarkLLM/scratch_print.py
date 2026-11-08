import json
lines = open('experiments/baseline/dataset/samples.jsonl', encoding='utf-8').readlines()
d = [json.loads(L) for L in lines]
c4 = [x for x in d if 'c4' in x['dataset']]
wiki = [x for x in d if 'wiki' in x['dataset']]
print(f'C4 count: {len(c4)}, Wiki count: {len(wiki)}, Tokens: {set(x["prompt_token_count"] for x in d)}')
for x in c4[:3] + wiki[:3]:
    print(f'\n--- {x["sample_id"]} ---')
    print(f'Dataset: {x["dataset"]}')
    print(f'URL/Source: {x["source"]}')
    print(f'Prompt: {repr(x["prompt_text"])}')
    print(f'Original (first 100): {repr(x["original_text"][:100])}')
