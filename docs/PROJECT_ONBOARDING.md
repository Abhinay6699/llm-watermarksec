# LLM-SEC / LLM-WatermarkSec: Onboarding & Developer Guide

## 1. Guided Tour: From Beginner to Advanced

### Level 1: Beginner — What is LLM Watermarking?
Large Language Models generate text one token at a time by outputting probability distributions (logits) over a vocabulary $V$ of size $\sim 50,000$.
- **Without Watermark**: The model selects tokens strictly based on learned probability: $P(w_t \mid w_{<t}) = \text{softmax}(z_t)$.
- **With Watermark**: A hidden, mathematically verifiable signal is embedded directly into the generation process so that downstream detectors can distinguish machine-generated text from human writing without needing to store every generated text in a database.

```
                      Prompt: "The future of AI is..."
                                    |
                                    v
                     +-------------------------------+
                     |          Base LLM             |
                     |      (facebook/opt-1.3b)      |
                     +-------------------------------+
                                    |
                            Raw Logits Vector [V]
                                    |
                                    v
                     +-------------------------------+
                     |   Watermark LogitsProcessor   |
                     |  - Hash preceding token(s)    |
                     |  - Partition: Green & Red     |
                     |  - Add delta bias to Green    |
                     +-------------------------------+
                                    |
                           Modified Logits
                                    |
                                    v
                            Sample Next Token
                                    |
                                    v
                   Output: High fraction of Green tokens
```

---

### Level 2: Intermediate — The KGW Mechanism & Detection Math

The fundamental baseline in the project is **KGW** (Kirchenbauer et al., ICML 2023):
1. **Splitting the Vocabulary**:
   At step $t$, the algorithm hashes the previous token $w_{t-1}$ using a secret seed $s$:
   $$\text{seed} = \text{Hash}(w_{t-1}) \oplus s$$
   Using this pseudorandom seed, vocabulary $V$ is partitioned into a **Green list** $G$ of size $\gamma |V|$ and a **Red list** $R$ of size $(1-\gamma) |V|$ (typically $\gamma = 0.5$ or $0.25$).
2. **Logit Perturbation**:
   A constant bias $\delta > 0$ is added to the logits of tokens in the Green list:
   $$z_t(k)' = \begin{cases} z_t(k) + \delta & \text{if } k \in G \\ z_t(k) & \text{if } k \in R \end{cases}$$
3. **Statistical Detection ($z$-score)**:
   For an unwatermarked text of length $N$, the number of tokens falling into $G$, denoted $N_G$, follows a Binomial distribution $B(N, \gamma)$ with mean $\mu = \gamma N$ and variance $\sigma^2 = N \gamma (1-\gamma)$.
   The detection statistic is the standard normal $z$-score:
   $$z = \frac{N_G - \gamma N}{\sqrt{N \gamma (1-\gamma)}}$$
   - If $z > 4.0$ (or configured threshold), the null hypothesis ($H_0$: text is natural/unwatermarked) is rejected with $p < 0.00003$.

---

### Level 3: Advanced — Beyond KGW (Security, Robustness & Cryptography)

While KGW is simple and effective, it has three critical security weaknesses:
1. **Vulnerability to Paraphrasing**: Replacing words with synonyms destroys the exact $w_{t-1} \to w_t$ hash dependency.
2. **Key Leaking / Watermark Stealing**: By querying the model repeatedly and counting token frequencies across different contexts, an adversary can reverse-engineer which tokens belong to the green list (`watermark/steal/steal.py`).
3. **Public Verification Vulnerability**: If the detector key is exposed to the public to verify AI text, attackers can use that key to spoof watermarks on malicious text.

To address these vulnerabilities, our workspace includes advanced paradigms:
- **`TextSeal` & `UPV` (Cryptographic Asymmetric Watermarking)**: Uses dual keys (private generation key, public verification key) so anyone can verify the watermark without being able to forge it.
- **`SIR` & `SemStamp` (Semantic Invariant Watermarking)**: Uses small sentence-transformers to condition the watermark on high-level sentence embeddings rather than brittle single-token hashes. Paraphrases retain the semantic embedding and thus retain the watermark!
- **`EXP` / `EXPGumbel` / `Unbiased` (Distortion-Free Watermarking)**: Changes sampling without changing the marginal probability distribution, guaranteeing zero degradation in perplexity.

---

## 2. File-by-File Breakdown: Workspace Artifacts

### `smoke_test.py` (Custom Pipeline Validation)
- **Lines 14-34 (`print_env`)**: Checks and logs OS, Python version, PyTorch version, CUDA status, and system memory.
- **Lines 35-81 (`test_watermark`)**: Takes an algorithm name (`KGW`, `Unigram`, `TextSeal`), loads it via `AutoWatermark.load()`, generates watermarked text, detects it, records execution time, generates unwatermarked text, and detects that as a negative control.
- **Lines 82-118 (`main`)**: Initializes `facebook/opt-1.3b` (with automatic fallback to `facebook/opt-125m` on CPU memory constraint) wrapped in `TransformersConfig`, and executes the benchmark over `KGW`, `Unigram`, and `TextSeal`.

### `prepare_datasets.py` (Dataset Curation)
- **Lines 10-21**: Sets seed `42` and defines `is_wikitext_header` to filter structural artifacts like `= = = Section = = =`.
- **Lines 43-95 (`process_dataset`)**: Streams data from HuggingFace (`allenai/c4` and `Salesforce/wikitext`), enforces a minimum length of 50 tokens, slices the first 50 tokens as the prompt, deduplicates texts, and stores 30 samples from C4 and 30 samples from WikiText-103.
- **Lines 99-124**: Writes `samples.jsonl`, `dataset_config.json`, and `README.md` into `experiments/baseline/dataset/`.

### `run1.txt` & `run2.txt` (Empirical Execution Logs)
- Prove actual execution on Windows 11 with CPU PyTorch 2.6.0.
- Benchmark timings on CPU:
  - **KGW**: ~85s - 102s (Watermarked $z=10.56$, Unwatermarked $z=0.74$).
  - **Unigram**: ~45s - 47s (Watermarked $z=6.50$, Unwatermarked $z=-0.26$).
  - **TextSeal**: ~13s - 15s (Watermarked score=13.37, Unwatermarked score=0.36).
- Confirm that detection works cleanly: Watermarked texts have extremely high scores ($>6.5$), and unwatermarked texts remain near zero ($\le 0.74$).

---

## 3. How to Run the Workspace

### Step 1: Run Environment & Smoke Test
```powershell
cd MarkLLM
python smoke_test.py
```

### Step 2: Regenerate or Extend Baseline Dataset
```powershell
cd MarkLLM
python prepare_datasets.py
```

### Step 3: Run Full Evaluation Pipeline (Robustness to Word Deletion)
```python
from watermark.auto_watermark import AutoWatermark
from utils.transformers_config import TransformersConfig
from evaluation.dataset import C4Dataset
from evaluation.pipelines.detection import WatermarkedTextDetectionPipeline, UnWatermarkedTextDetectionPipeline, DetectionPipelineReturnType
from evaluation.tools.text_editor import WordDeletion
from evaluation.tools.success_rate_calculator import DynamicThresholdSuccessRateCalculator

# Configure model and watermark, load dataset, and evaluate pipeline
```

---

## 4. Academic Guide Meeting FAQ & Defense Strategy

### Q1: "What is your baseline model and why did you choose it?"
> **Answer**: "We are using `facebook/opt-1.3b` (Open Pre-trained Transformer 1.3B) with a fallback to `opt-125m`. It is the canonical baseline adopted in major watermarking literature (Kirchenbauer et al., Aaronson et al., MarkLLM benchmark) because it is fully open-source, standard across papers, fits in memory, and allows reproducible evaluation of logit-level modifications."

### Q2: "What is the statistical significance of your watermark detection?"
> **Answer**: "Under the null hypothesis $H_0$ that the text is unwatermarked, token selections are modeled as independent Bernoulli trials where each token has probability $\gamma$ of falling into the green list. For a sequence of length $N$, the count $N_G$ yields a standard normal $z$-score. In our empirical smoke tests (`run1.txt`), KGW achieved $z = 10.56$ for watermarked text versus $z = 0.74$ for unwatermarked text. A $z$-score of $10.56$ corresponds to a p-value $< 10^{-25}$, indicating near-zero false positive probability."

### Q3: "What attacks against watermarks exist, and what does this codebase test?"
> **Answer**: "Attacks fall into two categories:
> 1. **Robustness attacks (Watermark Removal)**: Word deletion, synonym substitution, back-translation, and neural paraphrasing (e.g., DIPPER, GPT). The codebase implements these in `evaluation/tools/text_editor.py`.
> 2. **Security attacks (Watermark Forgery / Stealing)**: Watermark stealing attacks where an attacker reverse-engineers the green list by querying the API and tracking token frequencies. The codebase implements this in `watermark/steal/steal.py`."

### Q4: "What have you accomplished so far, and what remains for the next stage?"
> **Answer**: "We have validated our experimental environment, verified that the end-to-end generation and detection pipelines work for KGW, Unigram, and TextSeal, and created a curated 60-sample baseline dataset across C4 and WikiText-103. Our immediate next phase is to run systematic robustness curves (evaluating detection degradation against increasing attack intensity) and benchmark quality trade-offs (Perplexity and BLEU) across KGW vs. semantic/cryptographic algorithms."

