# LLM-SEC (LLM-WatermarkSec): Academic Project Presentation Brief

> **Target Audience**: Academic Project Guide / Evaluation Committee  
> **Purpose**: Slide-by-slide slide-generation brief & talking points  
> **Status Tag Legend**:
> - `[COMPLETED]`: Fully implemented, executed, and empirically verified in the workspace.
> - `[AVAILABLE]`: Implemented in the foundational MarkLLM framework, verified present, but not yet integrated into our custom experimental pipelines.
> - `[ONGOING]`: Currently being designed or configured.
> - `[PLANNED]`: Future roadmap milestone, not yet implemented.

---

## 1. Official Project Title

**LLM-SEC: Rigorous Security, Detectability, and Linguistic Quality Evaluation of Large Language Model Watermarking Frameworks**  
*(Short Title: LLM-WatermarkSec)*

---

## 2. Project Abstract and Introduction

- **Abstract**:  
  With the exponential growth of Large Language Models (LLMs) in software development, academic writing, and public communications, differentiating synthetic machine-generated text from human writing has become a pressing cybersecurity and provenance requirement. Text watermarking embeds hidden, mathematically verifiable statistical signals directly into model generation probabilities. While current research introduces diverse watermarking schemes—ranging from rule-based logit biasing to cryptographic asymmetric signatures—there is a lack of rigorous, independent empirical auditing regarding their vulnerability to adversarial perturbation, query-based stealing, and linguistic quality degradation. This research systematically benchmarks the robustness, detectability, and text-quality trade-offs across distinct watermarking paradigms (rule-based KGW, context-free Unigram, and dual-key cryptographic TextSeal) utilizing `facebook/opt-1.3b`.

- **Current Status**:
  - `[COMPLETED]`: Literature synthesis, test environment setup on Windows 11 CPU, smoke test execution across 3 core algorithms, and curated baseline dataset creation (60 samples from C4 and WikiText-103).
  - `[ONGOING]`: Batch experiment pipeline automation.
  - `[PLANNED]`: Adversarial attack sweeps (WordDeletion, SynonymSubstitution, Paraphrasing, Watermark Stealing).

---

## 3. Problem Statement

Existing text watermarking mechanisms for LLMs suffer from a three-way tension between **Detectability**, **Robustness**, and **Linguistic Quality**:
1. **Security Vulnerabilities**: Symmetric watermarks (e.g., KGW) share identical keys for generation and detection. Publishing the detector allows adversaries to reverse-engineer green-token partitions and spoof watermarks on malicious content.
2. **Fragility Under Perturbation**: Simple post-processing attacks (word deletion, synonym substitution, paraphrasing) destroy n-gram hashing histories, collapsing detection statistics.
3. **Linguistic Distortion**: Aggressive logit biasing ($\delta$) alters the underlying token probability distribution, risking increased perplexity and repetitive text generation.

**Core Research Question**:  
*How do different classes of watermarking algorithms (heuristic rule-based vs. context-free vs. cryptographic dual-key) perform when subjected to black-box extraction and adversarial text perturbation, and what is the exact Pareto frontier between security resilience and linguistic fidelity?*

---

## 4. Motivation and Significance

1. **AI Safety & Regulatory Compliance**: Global AI governance mandates (e.g., EU AI Act, US Executive Order on AI) demand verifiable provenance and watermarking for synthetic media.
2. **Intellectual Property Protection**: LLM providers need to prevent unauthorized model extraction, training data scraping, and knowledge distillation.
3. **Mitigating Malicious Abuse**: Robust watermarking is the frontline defense against automated disinformation, phishing, deepfake text generation, and academic dishonesty.
4. **Academic Rigor**: Moving beyond isolated algorithm claims to establish a standardized, reproducible benchmark under uniform token-length and decoding constraints.

---

## 5. Research Objectives

- **Objective 1 `[COMPLETED]`**: Audit, deploy, and validate an extensible open-source watermarking research testbed on local infrastructure (`facebook/opt-1.3b` on PyTorch).
- **Objective 2 `[COMPLETED]`**: Curate a standardized, balanced prompt dataset (60 prompts, 50 tokens each) from diverse domains (encyclopedic WikiText-103 and conversational web C4).
- **Objective 3 `[COMPLETED]`**: Conduct baseline smoke tests verifying end-to-end generation and detection separability across KGW, Unigram, and TextSeal.
- **Objective 4 `[PLANNED]`**: Execute batch sensitivity curves measuring True Positive Rate (TPR @ 1% FPR) under graduated attack intensities (10% to 50% word deletion and synonym substitution).
- **Objective 5 `[PLANNED]`**: Quantify linguistic quality degradation using Perplexity (PPL), LogDiversity, and BERTScore against unwatermarked greedy references.
- **Objective 6 `[PLANNED]`**: Evaluate watermark private-key vulnerability against frequency-based query stealing attacks.

---

## 6. Literature Review and Existing Approaches

```
+--------------------------------------------------------------------------------------------------+
|                                    WATERMARKING TAXONOMY                                         |
+------------------------------------+------------------------------------+------------------------+
| 1. Rule-Based / Logit Biasing      | 2. Cryptographic / Asymmetric      | 3. Distortion-Free /   |
|                                    |                                    |    Sampling-Based      |
| - KGW (Kirchenbauer et al., 2023)  | - UPV (Liu et al., ICLR 2024)      | - EXP (Aaronson, 2023) |
| - Unigram (Zhao et al., ICLR 2024) | - TextSeal (Preprint 2026)         | - EXPEdit / ITSEdit    |
| - SWEET (Lee et al., ACL 2024)     |                                    |   (Kuditipudi, 2024)   |
| - Adaptive (Liu et al., ICML 2024) |                                    | - Unbiased (Hu, 2024)  |
+------------------------------------+------------------------------------+------------------------+
| 4. Semantic Invariant              | 5. Neural / End-to-End             | 6. Adversarial Attacks |
| - SIR (Liu et al., ICLR 2024)      | - SynthID-Text (Nature 2024)       | - RandomWalk (ICML '24)|
| - SemStamp (Hou et al., NAACL 2024)| - E2E (ICML 2025)                  | - Dipper Paraphrasing  |
| - X-SIR (He et al., ACL 2024)      | - TS (Zheng & Huo, ICML 2024)      | - Watermark Stealing   |
+------------------------------------+------------------------------------+------------------------+
```

1. **Kirchenbauer et al. (ICML 2023)**: Introduced pseudo-random vocabulary splitting based on preceding token hash. Pioneered the $z$-score hypothesis test.
2. **Zhao et al. (ICLR 2024)**: Introduced Unigram watermarking, removing dependence on preceding tokens to withstand token editing, but vulnerable to frequency-analysis attacks.
3. **Liu et al. (ICLR 2024) / TextSeal (2026)**: Addressed public verification risks by decoupling generation (private key) from detection (public key / neural discriminator).
4. **Kuditipudi et al. (TMLR 2024)**: Formulated distortion-free watermarks using inverse transform sampling and edit-distance alignment.
5. **Pan et al. / Liu et al. (EMNLP 2024 Demo)**: Developed the unified MarkLLM toolkit consolidating these paradigms into modular APIs.

---

## 7. Research Gap and Proposed Contribution

- **The Gap**:  
  Published papers typically evaluate their proposed watermark against isolated baseline setups, often omitting unified evaluations under identical token budgets, identical base models, and standardized attack toolchains. Furthermore, the empirical vulnerability of modern dual-key methods (TextSeal) relative to classical heuristic methods (KGW) under identical compute constraints remains under-investigated.
- **Our Proposed Contribution**:
  1. A reproducible, self-contained benchmarking suite leveraging MarkLLM for transparent comparison.
  2. A dual-domain curated baseline dataset (C4 and WikiText-103) standardized to exact prompt lengths.
  3. A multi-dimensional evaluation protocol covering:
     - **Detectability**: $\Delta z$-score and ROC analysis.
     - **Security**: Degradation under lexical perturbation and query-stealing attacks.
     - **Fidelity**: Quantitative perplexity ratio ($PPL_{\text{watermarked}} / PPL_{\text{unwatermarked}}$).

---

## 8. Technical Architecture & Component Descriptions

### Mermaid System Architecture

```mermaid
graph TB
    subgraph Input & Curation [Completed]
        C4[allenai/c4 train] --> F[prepare_datasets.py]
        WIKI[Salesforce/wikitext test] --> F
        F --> DSET[experiments/baseline/dataset/samples.jsonl<br>60 Samples, 50 Tokens Each]
    end

    subgraph Core Engine [MarkLLM Library - Completed]
        CFG[utils/transformers_config.py<br>facebook/opt-1.3b, vocab=50272]
        AW[watermark/auto_watermark.py<br>AutoWatermark Factory]
        KGW_M[watermark/kgw/kgw.py]
        UNI_M[watermark/unigram/unigram.py]
        TSL_M[watermark/textseal/textseal.py]
        AW --> KGW_M
        AW --> UNI_M
        AW --> TSL_M
    end

    subgraph Execution & Validation [Completed]
        SMOKE[smoke_test.py]
        CFG --> SMOKE
        AW --> SMOKE
        SMOKE --> R1[run1.txt / run2.txt<br>Verified Detection Scores & CPU Timings]
    end

    subgraph Available Evaluation Tools [Framework Available - To Be Integrated]
        TE[evaluation/tools/text_editor.py<br>WordDeletion, SynonymSubstitution, RandomWalk]
        QA[evaluation/tools/text_quality_analyzer.py<br>PPLCalculator, LogDiversity, BERTScore]
        ST[watermark/steal/steal.py<br>Watermark Stealing Query Attack]
    end

    subgraph Planned Automation [Planned]
        RUNNER[Batch Experiment Orchestrator<br>Automated Sweeps & Metrics Aggregator]
        DSET -.-> RUNNER
        RUNNER -.-> TE
        RUNNER -.-> QA
        RUNNER -.-> ST
    end
```

### Component Breakdown
1. **Configuration Layer**: `TransformersConfig` standardizes the causal model (`opt-1.3b`), tokenizer, device binding (`cpu`), and decoding parameters (`max_new_tokens=50`, `min_length=10`, `do_sample=True`, `no_repeat_ngram_size=4`).
2. **Factory Subsystem**: `AutoWatermark` and `AutoConfig` dynamically load algorithms and configurations without hardcoding dependencies.
3. **Generation & Logits Processing**: Base class `BaseWatermark` hooks into Hugging Face `generate()`, injecting biases or sampling transformations.
4. **Detection Subsystem**: Computes statistical or neural confidence metrics.

---

## 9. In-Depth Algorithm Analysis: KGW, Unigram, and TextSeal

### A. KGW (Kirchenbauer et al., ICML 2023)
- **Paradigm**: Context-dependent heuristic logit biasing (symmetric key).
- **Mechanism**:
  - Takes the preceding token $w_{t-1}$, hashes it with secret random seed $s$ to seed a PRNG.
  - Partitions vocabulary $V$ into Green list $G$ ($\gamma |V|$) and Red list $R$ ($(1-\gamma)|V|$).
  - Adds constant bias $\delta$ to Green token logits: $z_t(k)' = z_t(k) + \delta$ for $k \in G$.
- **Detection**: One-tailed binomial hypothesis test against $H_0$ (unwatermarked text):
  $$z = \frac{N_G - \gamma N}{\sqrt{N \gamma (1-\gamma)}}$$
- **Vulnerability**: Editing or deleting preceding tokens shifts the hash, corrupting green list assignments for subsequent tokens.

### B. Unigram (Zhao et al., ICLR 2024)
- **Paradigm**: Context-independent static logit biasing.
- **Mechanism**:
  - The green list $G$ is statically chosen once for the entire vocabulary based on secret key $s$, independent of preceding tokens $w_{t-1}$.
  - Bias $\delta$ is permanently added to $G$.
- **Detection**: Identical $z$-score formula, but counts green tokens globally across the entire sequence.
- **Strength & Weakness**:
  - *Strength*: Highly robust against word insertions and deletions because previous-token synchronization is not required.
  - *Weakness*: Vulnerable to frequency-counting attacks; an adversary observing token outputs across multiple prompts can reconstruct $G$.

### C. TextSeal (Preprint 2026)
- **Paradigm**: Cryptographic asymmetric dual-key watermarking.
- **Mechanism**:
  - Decouples the watermarking generation process from the detection process.
  - Uses private parameters for embedding the signal and public/neural parameters for verification.
  - Prevents adversaries who have access to the detector from reconstructing generation rules or forging watermarks on unwatermarked text.
- **Detection**: Evaluates an empirical verification score against an optimized threshold.

---

## 10. Dataset Preparation & Curation

- **Script**: [`prepare_datasets.py`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/prepare_datasets.py) `[COMPLETED]`
- **Storage**: [`experiments/baseline/dataset/samples.jsonl`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/experiments/baseline/dataset/samples.jsonl) (140,228 bytes)
- **Data Configuration** (from `dataset_config.json`):
  - **Source 1**: `allenai/c4` (split: `train`, config: `en`) — 30 samples.
  - **Source 2**: `Salesforce/wikitext` (split: `test`, config: `wikitext-103-raw-v1`) — 30 samples.
  - **Total Sample Count**: Exactly 60 prompts.
  - **Prompt Extraction Rule**: First 50 tokens (using `facebook/opt-1.3b` tokenizer).
  - **Sampling Seed**: Fixed at `42` for exact reproducibility.
  - **Filtering Rules**:
    - Discard texts shorter than 50 tokens.
    - WikiText: Discard header lines (`= Title =`).
    - Deduplicate exact match texts.
- **Verification Scripts**:
  - [`scratch_datasets.py`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/scratch_datasets.py): Verified Hugging Face streaming compatibility.
  - [`scratch_print.py`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/scratch_print.py): Confirmed prompt token count distribution (all exactly 50 tokens).

---

## 11. Experimental Methodology

```mermaid
sequenceDiagram
    autonumber
    actor Researcher
    participant DS as Baseline Dataset (60 samples)
    participant Model as OPT-1.3B (HuggingFace)
    participant WM as AutoWatermark (KGW/Unigram/TextSeal)
    participant Attack as TextEditor (Deletion/Paraphrase)
    participant Det as Detector (Z-Score / Score)
    participant Eval as Quality Analyzer (PPL / BLEU)

    Researcher->>DS: Load prompt (50 tokens)
    DS->>Model: Forward pass (compute logits)
    Model->>WM: Intercept logits (apply green bias / crypto)
    WM->>Model: Return biased logits
    Model->>Researcher: Return Watermarked Text
    Note over Researcher,Attack: Attack Phase (Planned)
    Researcher->>Attack: Apply Word Deletion / Synonym Substitution
    Attack->>Det: Submit Perturbed Text
    Det->>Researcher: Return detection score (z-score)
    Researcher->>Eval: Compute PPL & BERTScore vs greedy unwatermarked
    Eval->>Researcher: Report trade-off metrics
```

1. **Generation Protocol**: Prompts are fed to `facebook/opt-1.3b`. `gen_kwargs` sets `max_new_tokens=50`, `min_length=10`, `do_sample=True`, `no_repeat_ngram_size=4`.
2. **Negative Control**: For every prompt, both a watermarked text and an unwatermarked natural completion are generated under identical seeds.
3. **Attack Injection `[PLANNED]`**: Output texts are perturbed via `WordDeletion` (ratios 0.1, 0.2, 0.3) and `SynonymSubstitution`.
4. **Detection Metric Extraction**: Measure $z$-scores and classify positive if $z > \tau$ (e.g., $\tau = 4.0$).
5. **Quality Assessment `[PLANNED]`**: Measure perplexity ratio using an independent evaluator.

---

## 12. Preliminary Smoke-Test Results (Empirical Verification)

All results below are recorded directly from [`run1.txt`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/run1.txt) and [`run2.txt`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/run2.txt) executed in the workspace on Windows 11 CPU (`PyTorch 2.6.0+cpu`):

### Exact Benchmark Table

| Algorithm | Text Type | Generated Length | Detection Output (`is_watermarked`, Score) | Run 1 Latency | Run 2 Latency | Statistical Outcome |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **KGW** | Watermarked | 1,056 chars | `True`, **$z = 10.5568$** | 85.27s | 102.25s | Strong signal ($p < 10^{-25}$) |
| **KGW** | Unwatermarked | 877 chars | `False`, **$z = 0.7366$** | 86.28s | 82.59s | Negative control valid ($z < 4.0$) |
| **Unigram** | Watermarked | 616 chars | `True`, **$z = 6.5033$** | 46.61s | 44.81s | Strong signal ($p < 10^{-10}$) |
| **Unigram** | Unwatermarked | 256 chars | `False`, **$z = -0.2626$** | 14.41s | 15.95s | Negative control valid ($z \approx 0$) |
| **TextSeal** | Watermarked | 239 chars | `True`, **Score $= 13.3722$** | 13.64s | 15.29s | Cryptographic signature detected |
| **TextSeal** | Unwatermarked | 257 chars | `False`, **Score $= 0.3612$** | 23.14s | 16.25s | Negative control valid |

### Key Scientific Takeaways
1. **Zero False Positives in Baseline**: All unwatermarked texts remained well within null hypothesis bounds ($z = 0.74$ and $-0.26$ for KGW and Unigram; score $0.36$ for TextSeal).
2. **Clear Separation Margin**:
   - KGW separation margin: $\Delta z = 10.5568 - 0.7366 = 9.8202$.
   - Unigram separation margin: $\Delta z = 6.5033 - (-0.2626) = 6.7659$.
   - TextSeal separation margin: $\Delta \text{score} = 13.3722 - 0.3612 = 13.0110$.
3. **Latency Profile**: TextSeal exhibits the fastest CPU generation (~13.6s) while KGW takes ~85s–102s due to per-step token hash calculations.

---

## 13. Actual Completed Implementation

The following deliverables have been built, verified, and preserved in the workspace:
- `[COMPLETED]` **Core Test Harness**: [`smoke_test.py`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/smoke_test.py) validating environment, fallback model resolution, and multi-watermark generation/detection.
- `[COMPLETED]` **Dataset Generator**: [`prepare_datasets.py`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/prepare_datasets.py) implementing Hugging Face streaming, token threshold filtering, header stripping, and JSONL persistence.
- `[COMPLETED]` **Curated Baseline Dataset**: [`experiments/baseline/dataset/samples.jsonl`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/experiments/baseline/dataset/samples.jsonl), `dataset_config.json`, and `README.md`.
- `[COMPLETED]` **Sanity & Verification Tools**: [`scratch_datasets.py`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/scratch_datasets.py) and [`scratch_print.py`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/scratch_print.py).
- `[COMPLETED]` **Empirical Execution Logs**: [`run1.txt`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/run1.txt) and [`run2.txt`](file:///c:/Users/nagna/Desktop/MAIN/MarkLLM/run2.txt) validating CPU runtimes and score reproducibility.
- `[COMPLETED]` **Documentation Base**:
  - `docs/PROJECT_ARCHITECTURE.md`
  - `docs/PROJECT_ONBOARDING.md`
  - `docs/IMPLEMENTATION_STATUS.md`
  - `docs/RESEARCH_WORKFLOW.md`

---

## 14. Available Framework Capabilities (Not Yet Integrated in Our Experiments)

The following components are fully implemented within the underlying MarkLLM framework and are ready for immediate integration into our next experimental wave:
- `[AVAILABLE]` **Additional Algorithms (21 Methods)**:
  - Semantic: `SIR`, `X-SIR`, `SemStamp`, `k-SemStamp`, `DEW`.
  - Distortion-Free: `EXP`, `EXPGumbel`, `EXPEdit`, `ITSEdit`, `DIP`, `Unbiased`, `PF`.
  - Neural / Nature: `SynthID` (DeepMind), `E2E`, `TS`.
  - Entropy: `EWD`, `IE`.
  - Cryptographic / Adaptive: `UPV`, `Adaptive`, `MorphMark`, `SWEET`.
- `[AVAILABLE]` **Attack Toolchain (`evaluation/tools/text_editor.py`)**:
  - `WordDeletion(ratio)`
  - `SynonymSubstitution(ratio)` & `ContextAwareSynonymSubstitution`
  - `DipperParaphraser` & `GPTParaphraser`
  - `RandomWalkAttack` (ICML 2024 impossibility search)
  - `BackTranslationTextEditor`
- `[AVAILABLE]` **Watermark Stealing Module (`watermark/steal/`)**:
  - `steal.py`, `countstore.py`, `pre_counts.py` for token-frequency extraction attacks.
- `[AVAILABLE]` **Quality Evaluators (`evaluation/tools/text_quality_analyzer.py`)**:
  - `PPLCalculator`, `LogDiversityAnalyzer`, `BLEUCalculator`, `ROUGE1/2/L`, `BERTScoreCalculator`, `GPTTextDiscriminator`.
- `[AVAILABLE]` **Visualization Suite (`visualize/`)**:
  - `DiscreteVisualizer` and `ContinuousVisualizer` for PDF/image highlighting of green/red token assignments.

---

## 15. Pending Implementation

The following components represent the remaining technical milestones for the project:
- `[PLANNED]` **Batch Experiment Orchestrator (`run_experiments.py`)**:
  - Automated script iterating over all 60 samples in `samples.jsonl`.
  - Automatically runs generation, saves attacked variants, runs detectors, and outputs structured CSV/JSON results.
- `[PLANNED]` **Security Attack Sensitivity Sweeps**:
  - Running `WordDeletion` at $p \in [0.1, 0.2, 0.3, 0.4, 0.5]$.
  - Measuring degradation of $z$-score and computing empirical True Positive Rate at 1% False Positive Rate (TPR @ 1% FPR).
- `[PLANNED]` **Linguistic Quality Audit Script**:
  - Automated perplexity calculation across watermarked vs. unwatermarked outputs.
- `[PLANNED]` **Metric Aggregator & Visualization Script**:
  - Script to generate ROC curves, AUC tables, and trade-off scatter plots.

---

## 16. Hardware and Computational Constraints

- **Execution Environment**: Local Windows 11 workstation.
- **Hardware Profile**: CPU execution (`PyTorch 2.6.0+cpu`, no CUDA GPU available).
- **Available System Memory**: 15.71 GB RAM.
- **Runtime Impact**:
  - Single-sample generation and detection on CPU takes **~15s to ~102s** per prompt with `facebook/opt-1.3b`.
  - Running all 60 samples across 3 algorithms requires **~1.5 to 2.5 hours** of continuous CPU computation.
  - Full parameter sweeps across all 24 algorithms or heavy paraphrase models (DIPPER) will require GPU resources (e.g., Google Colab T4/A100 or institutional compute cluster).

---

## 17. Challenges

1. **Compute Throughput**: CPU-only inference bottlenecks large-scale statistical sweeps ($N > 200$).
2. **Dependency & Platform Nuances**: Python 3.12 compatibility on Windows required adjusting `requirements.txt` (`Pillow`) and handling pre-compiled Cython modules (`.pyx` in EXPEdit/ITSEdit).
3. **Attack API Dependencies**: Neural paraphrasing (`GPTParaphraser`) requires external OpenAI API keys; local neural surrogates (`DipperParaphraser`) require significant GPU VRAM.
4. **Statistical Power vs. Time**: Balancing prompt count with execution latency to obtain statistically valid $p$-values without timeouts.

---

## 18. Next Development Milestones

```
Milestone 1 [CURRENT]:
Environment setup, smoke testing, and 60-sample dataset creation. (COMPLETED)
     |
     v
Milestone 2 [DAYS 1-7]:
Implement batch experiment orchestrator (run_experiments.py) for the 60 samples across KGW, Unigram, and TextSeal.
     |
     v
Milestone 3 [DAYS 8-14]:
Run perturbation robustness benchmarks (WordDeletion and SynonymSubstitution) and record TPR/FPR ROC curves.
     |
     v
Milestone 4 [DAYS 15-21]:
Compute text quality metrics (Perplexity and BERTScore) to establish the empirical Quality vs. Security Pareto frontier.
     |
     v
Milestone 5 [DAYS 22-30]:
Compile final thesis tables, comparative figures, and prepare dissertation draft.
```

---

## 19. Genuine Academic References

1. **Kirchenbauer, J., Geiping, J., Wen, Y., Katz, J., Miers, I., & Goldstein, T.** (2023). *A Watermark for Large Language Models*. International Conference on Machine Learning (ICML 2023). [arXiv:2301.10226](https://arxiv.org/abs/2301.10226).
2. **Zhao, X., An, P., Lou, Y., Chen, X., & Huang, J.** (2024). *Provable Robust Watermarking for AI-Generated Text*. International Conference on Learning Representations (ICLR 2024). [arXiv:2306.17439](https://arxiv.org/abs/2306.17439).
3. **Liu, A., Pan, L., Hu, X., Li, S., Wen, L., King, I., & Yu, P. S.** (2024). *An Unforgeable Publicly Verifiable Watermark for Large Language Models*. International Conference on Learning Representations (ICLR 2024). [arXiv:2307.16230](https://arxiv.org/abs/2307.16230).
4. **Liu, A., Pan, L., Hu, X., Meng, S., & Wen, L.** (2024). *A Semantic Invariant Robust Watermark for Large Language Models*. International Conference on Learning Representations (ICLR 2024). [arXiv:2310.06356](https://arxiv.org/abs/2310.06356).
5. **Pan, L., Liu, A., Lu, Y., Hu, X., Zhang, X., Wen, L., King, I., Xiong, H., & Yu, P. S.** (2024). *MarkLLM: An Open-Source Toolkit for LLM Watermarking*. Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations (EMNLP 2024). [arXiv:2405.10051](https://arxiv.org/abs/2405.10051).
6. **Kuditipudi, R., Thickstun, J., Hashimoto, T., & Liang, P.** (2024). *Robust Distortion-free Watermarks for Language Models*. Transactions on Machine Learning Research (TMLR 2024). [arXiv:2307.15593](https://arxiv.org/abs/2307.15593).
7. **Kumar, A., et al. (Google DeepMind)** (2024). *Scalable watermarking for identifying large language model outputs*. Nature, 634, 818–823. [DOI:10.1038/s41586-024-08025-4](https://www.nature.com/articles/s41586-024-08025-4).
8. **Zhang, H., et al.** (2024). *Watermarking in the Sand: Impossibility Results for Strong Watermarking*. International Conference on Machine Learning (ICML 2024). [arXiv:2311.04378](https://arxiv.org/abs/2311.04378).
9. **He, Z., Zhou, B., Hao, H., Liu, A., Wang, X., Tu, Z., Zhang, Z., & Wang, R.** (2024). *Can Watermarks Survive Translation? On the Cross-lingual Consistency of Text Watermark for Large Language Models*. Association for Computational Linguistics (ACL 2024). [arXiv:2402.14007](https://arxiv.org/abs/2402.14007).
10. **TextSeal Authors** (2026). *TextSeal: A Dual-Key Watermark for Large Language Models*. [arXiv:2605.12456](https://arxiv.org/abs/2605.12456).

---

## 20. Concise Summary: Factual Information That MUST Appear in the Presentation

When preparing slides from this brief, ensure the following core facts are included:
1. **Model Used**: `facebook/opt-1.3b` (vocabulary size 50,272) loaded on CPU.
2. **Algorithms Validated**:
   - **KGW**: ICML 2023 baseline, logit biasing $\delta$, preceding-token hash.
   - **Unigram**: ICLR 2024 context-free static green list.
   - **TextSeal**: 2026 dual-key asymmetric cryptographic watermark.
3. **Dataset Facts**: Exactly 60 samples curated with seed 42 (30 from `allenai/c4`, 30 from `Salesforce/wikitext`), exactly 50 prompt tokens each.
4. **Smoke-Test Detection Proof**:
   - KGW: Watermarked $z = 10.56$ ($p < 10^{-25}$) vs Unwatermarked $z = 0.74$.
   - Unigram: Watermarked $z = 6.50$ ($p < 10^{-10}$) vs Unwatermarked $z = -0.26$.
   - TextSeal: Watermarked score $13.37$ vs Unwatermarked score $0.36$.
5. **Separation**: All three algorithms showed clear separation without false positives on unwatermarked text.
6. **Hardware Reality**: Operating on Windows 11 CPU (PyTorch 2.6.0+cpu, 15.71 GB RAM), requiring ~15s to ~100s per sample.
7. **Immediate Next Step**: Batch experiment driver script to execute perturbation attacks (WordDeletion) across the 60 samples and plot TPR @ 1% FPR.

