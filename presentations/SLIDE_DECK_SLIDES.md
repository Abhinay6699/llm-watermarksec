# LLM-SEC: Slide-by-Slide Presentation Deck & Speaker Script

> **Format**: Ready-to-use slide outline for PowerPoint, Google Slides, Marp, or AI Presentation Tools.  
> **Target Duration**: 10–12 minutes (approx. 1 minute per slide).

---

### Slide 1: Title & Metadata
- **Slide Title**: LLM-SEC: Security, Detectability, and Linguistic Quality Evaluation of LLM Watermarking Frameworks
- **Subtitle**: Systematic Benchmarking of Heuristic, Context-Free, and Cryptographic Text Watermarks
- **Presenter**: [Your Name / Research Candidate]
- **Guide / Advisor**: [Guide Name & Department]
- **Institution / Date**: [University / Academic Year 2026]
- **Key Visual**: Side-by-side icon representation: AI Text Generation $\to$ Watermark Injection $\to$ Adversarial Attacks $\to$ Verification
- **Speaker Notes**:
  > *"Good morning respected guide and committee members. Today I am presenting my research project, LLM-SEC. Our research focuses on auditing the security, detectability, and linguistic trade-offs of modern text watermarking techniques for Large Language Models. We evaluate how different watermarking families survive real-world adversarial attacks and query extraction."*

---

### Slide 2: Background & Research Motivation
- **Slide Title**: Why LLM Watermarking Matters
- **Bullet Points**:
  - **Proliferation of Synthetic Text**: Explosive adoption of generative LLMs across academic writing, code generation, and journalism.
  - **Threat Vectors**: Disinformation campaigns, phishing, academic dishonesty, and unauthorized model distillation.
  - **Regulatory Imperatives**: EU AI Act and US Executive Order on AI mandate transparent provenance and watermarking for synthetic media.
  - **Core Challenge**: Post-hoc AI detectors (e.g., perplexity classifiers) suffer high false positive rates. In-generation watermarking provides a mathematically verifiable alternative.
- **Speaker Notes**:
  > *"As LLMs become pervasive, distinguishing AI-generated text from human writing is critical. Traditional post-hoc classifiers like DetectGPT or RoBERTa-based detectors often fail on out-of-domain text and have high false positive rates. Text watermarking solves this by embedding an undetectable, statistically provable signal directly into the token probability distribution during text generation."*

---

### Slide 3: Problem Statement & Research Gap
- **Slide Title**: The Fundamental Trilemma in Text Watermarking
- **Bullet Points**:
  - **The Trilemma**:
    1. *Detectability*: High confidence separation with zero false positives.
    2. *Robustness*: Signal survival under edits, paraphrasing, and query attacks.
    3. *Quality*: Zero distortion of language fluency and perplexity.
  - **The Research Gap**:
    - Existing literature evaluates algorithms in isolation with disparate token budgets.
    - Symmetric watermarks (KGW) leak detection rules; vulnerability of asymmetric dual-key schemes (TextSeal) under identical constraints remains unverified.
- **Key Visual**: Triangular diagram with vertices: *High Detectability*, *Adversarial Robustness*, and *Low Linguistic Distortion*.
- **Speaker Notes**:
  > *"Every watermarking method faces a trilemma between detectability, robustness, and linguistic quality. If you bias logits too heavily, you degrade text perplexity. If you bias lightly, simple word substitutions destroy the watermark. Furthermore, classical symmetric schemes like KGW expose the generation key during detection. Our research bridges this gap by benchmarking classical rule-based methods against modern dual-key cryptographic approaches under a standardized experimental setup."*

---

### Slide 4: Research Objectives & Scope
- **Slide Title**: Objectives of the Study
- **Bullet Points**:
  - **Obj 1 [COMPLETED]**: Establish and validate a unified testbed using open-source `facebook/opt-1.3b`.
  - **Obj 2 [COMPLETED]**: Curate a balanced 60-sample dataset (30 C4 web text, 30 WikiText-103 encyclopedic) with standardized 50-token prompts.
  - **Obj 3 [COMPLETED]**: Empirically verify baseline detectability on KGW, Unigram, and TextSeal without attack.
  - **Obj 4 [PLANNED]**: Sweep adversarial perturbations (`WordDeletion` 10%–50%, `SynonymSubstitution`) to plot TPR @ 1% FPR.
  - **Obj 5 [PLANNED]**: Quantify linguistic degradation via Perplexity (PPL) and BERTScore.
- **Speaker Notes**:
  > *"Our primary objectives are structured into two phases: First, establishing the testbed, standardizing datasets, and verifying zero-attack detection baselines—which we have completed. Second, running systematic adversarial attack sweeps and measuring linguistic quality degradation across algorithms to establish the empirical Pareto frontier."*

---

### Slide 5: System Architecture & Workflow
- **Slide Title**: LLM-SEC Architecture & Testbed Pipeline
- **Bullet Points**:
  - Built on top of the modular **MarkLLM** foundation (EMNLP 2024).
  - **Decoupled Engine**: Factory pattern (`AutoWatermark`) dynamically loading 24 algorithms via JSON configs.
  - **Standardized Execution**: Unified `TransformersConfig` wrapping causal LM, tokenizer, and sampling hyper-parameters.
  - **Attacks & Evaluation Subsystem**: Modular text editors (`WordDeletion`, `Paraphrasing`) and statistical success rate calculators.
- **Key Visual**: Pipeline flowchart: `Dataset (C4/WikiText) -> OPT-1.3B -> Watermark Logits Processor -> Adversarial Editor -> Detector (z-score)`.
- **Speaker Notes**:
  > *"Our architecture leverages MarkLLM. We use a factory pattern where AutoWatermark dynamically instantiates the algorithm and injects the generation configuration. The causal model outputs logits, the watermark LogitsProcessor applies green-list biasing or cryptographic transforms, and the text is then evaluated by the detector and attack modules."*

---

### Slide 6: Watermark Algorithms Under Evaluation
- **Slide Title**: Key Paradigms: KGW vs. Unigram vs. TextSeal
- **Bullet Points**:
  - **KGW (Kirchenbauer et al., ICML 2023)**:
    - *Mechanism*: Preceding token $w_{t-1}$ hashes to pseudo-randomly partition vocabulary into Green ($G$) and Red ($R$). Green logits receive $+\delta$ bias.
    - *Pros/Cons*: Strong detectability; brittle under token deletion.
  - **Unigram (Zhao et al., ICLR 2024)**:
    - *Mechanism*: Fixed, context-free Green list applied globally across all generation steps.
    - *Pros/Cons*: Highly resilient to token deletion; vulnerable to token frequency extraction.
  - **TextSeal (Preprint 2026)**:
    - *Mechanism*: Cryptographic dual-key architecture (private generation key, public verification key).
    - *Pros/Cons*: Prevents watermark forgery and stealing; requires neural verification.
- **Speaker Notes**:
  > *"We focus on three representative paradigms: KGW represents context-dependent logit biasing where preceding tokens dictate the green list. Unigram removes previous-token dependency, making it resilient to word deletions but vulnerable to frequency attacks. TextSeal represents modern dual-key cryptographic watermarking, preventing attackers from reverse-engineering the watermark even if the detector is public."*

---

### Slide 7: Dataset Curation & Preprocessing
- **Slide Title**: Controlled Experimental Dataset
- **Bullet Points**:
  - **Curated Dataset**: 60 samples stored at `experiments/baseline/dataset/samples.jsonl`.
  - **Balanced Sources**:
    - **30 Prompts**: `allenai/c4` (unstructured open-web text).
    - **30 Prompts**: `Salesforce/wikitext` (structured encyclopedic text).
  - **Rigorous Standardization**:
    - Minimum length threshold: $\ge 50$ tokens.
    - Extracted prompt: Exactly the first 50 tokens using `opt-1.3b` tokenizer.
    - Noise filtering: Stripped WikiText section headers (`= = = Title = = =`).
    - Fixed seed: `42` for strict academic reproducibility.
- **Key Visual**: Table summarizing sample IDs, source datasets, token counts (50), and verification status.
- **Speaker Notes**:
  > *"To ensure scientific validity, we avoided arbitrary prompts. We wrote a custom dataset preparation pipeline that streamed data from both C4 and WikiText-103, filtered out headers and short texts, extracted exactly 50 tokens per prompt under fixed seed 42, and generated a 60-sample benchmark dataset."*

---

### Slide 8: Detection Mathematics & Hypothesis Testing
- **Slide Title**: How Watermarks Are Statistically Proven
- **Bullet Points**:
  - **Null Hypothesis ($H_0$)**: The text is natural/unwatermarked; tokens fall into Green list $G$ with probability $\gamma$ (e.g., $\gamma = 0.5$).
  - **Test Statistic**: For text of length $N$ with $N_G$ green tokens:
    $$z = \frac{N_G - \gamma N}{\sqrt{N \gamma (1-\gamma)}} \sim \mathcal{N}(0, 1)$$
  - **Decision Rule**: Reject $H_0$ if $z > \tau$ (typically $\tau = 4.0$, yielding $p < 0.00003$).
  - **Empirical Baseline Target**: Large separation margin $\Delta z = z_{\text{watermarked}} - z_{\text{unwatermarked}}$ with zero false positives.
- **Speaker Notes**:
  > *"Watermark detection relies on binomial hypothesis testing approximated by a standard normal distribution. Under the null hypothesis that text is human, tokens fall into the green list purely by chance with probability gamma. If the text is watermarked, the green token count spikes significantly. With a decision threshold of tau = 4.0, the false positive rate is less than 0.003%."*

---

### Slide 9: Preliminary Experimental Results
- **Slide Title**: Empirical Verification: Smoke Test Results
- **Bullet Points**:
  - Run on local Windows 11 workstation using `facebook/opt-1.3b` on CPU.
  - **Exact Empirical Results (from `run1.txt` / `run2.txt`)**:
    - **KGW**: Watermarked $z = \mathbf{10.56}$ ($p < 10^{-25}$) vs Unwatermarked $z = \mathbf{0.74}$.
    - **Unigram**: Watermarked $z = \mathbf{6.50}$ ($p < 10^{-10}$) vs Unwatermarked $z = \mathbf{-0.26}$.
    - **TextSeal**: Watermarked Score $= \mathbf{13.37}$ vs Unwatermarked Score $= \mathbf{0.36}$.
  - **Outcome**: **100% detection separation** with zero false positives across all three paradigms.
- **Key Visual**: Benchmark comparison bar chart showing massive separation between Watermarked vs. Unwatermarked scores.
- **Speaker Notes**:
  > *"Here are our actual empirical results from run1.txt and run2.txt. For KGW, watermarked text yielded an extraordinary z-score of 10.56, while unwatermarked text scored only 0.74. For Unigram, the score was 6.50 versus negative 0.26. For TextSeal, the cryptographic score was 13.37 versus 0.36. In all three cases, the separation margin is wide and clean, confirming our pipeline functions flawlessly."*

---

### Slide 10: Implementation Audit: Completed vs. Available
- **Slide Title**: Current Implementation Audit
- **Bullet Points**:
  - **Completed & Verified in Workspace `[COMPLETED]`**:
    - Environment test harness (`smoke_test.py`) with memory fallbacks.
    - Dataset curation pipeline (`prepare_datasets.py`) & verified 60-sample JSONL.
    - Execution logs (`run1.txt`, `run2.txt`) verifying CPU runtimes (13s–102s).
  - **Available in Framework Engine `[AVAILABLE]`**:
    - 21 additional algorithms (SIR, SemStamp, SynthID, EXP, EWD, UPV, etc.).
    - Attack editors: `WordDeletion`, `SynonymSubstitution`, `RandomWalkAttack`, `GPTParaphraser`.
    - Evaluation tools: `PPLCalculator`, `LogDiversityAnalyzer`, `BERTScore`.
- **Speaker Notes**:
  > *"To be transparent about our progress: the foundation testbed, dataset pipeline, smoke tests, and execution logs are completely implemented and verified. Additionally, the underlying framework already contains 21 additional algorithms and the full adversarial attack library, meaning we do not have to write attack algorithms from scratch—we only need to integrate them into our batch runner."*

---

### Slide 11: Computational Constraints & Challenges
- **Slide Title**: Workstation Constraints & Research Solutions
- **Bullet Points**:
  - **Hardware Profile**: Local execution on Windows 11 AMD64, 15.71 GB RAM, PyTorch CPU (`CUDA Available: False`).
  - **Throughput Latency**: Single-sample generation on CPU takes ~15s to ~102s per prompt for `opt-1.3b`.
  - **Batch Time Estimation**: 60 samples $\times$ 3 methods $\approx 2.0$ hours per sweep on CPU.
  - **Mitigation Strategy**:
    - Curate 60 highly representative samples for local statistical validity.
    - Migrate large-scale sweeps ($N > 200$) and neural paraphrasers (DIPPER) to Google Colab T4/A100 GPU compute.
- **Speaker Notes**:
  > *"Our primary technical constraint is that our local workstation is running on CPU. Each generation takes 15 to 102 seconds. While running 60 samples locally is manageable within two hours, running extensive multi-model sweeps with hundreds of samples will require moving to a GPU cluster or Colab T4 environment in our next phase."*

---

### Slide 12: Next Milestones & Research Roadmap
- **Slide Title**: Next Steps & Deliverables
- **Bullet Points**:
  - **Milestone 2 (Weeks 1–2)**: Implement automated batch runner (`run_experiments.py`) to execute all 60 samples across KGW, Unigram, and TextSeal.
  - **Milestone 3 (Weeks 3–4)**: Execute perturbation attack sweeps (`WordDeletion` at 10%–50%) and plot empirical TPR @ 1% FPR curves.
  - **Milestone 4 (Weeks 5–6)**: Measure Perplexity (PPL) and BERTScore trade-offs; test query-stealing attack module.
  - **Milestone 5 (Weeks 7–8)**: Compile experimental findings into thesis chapters and submit manuscript.
- **Speaker Notes**:
  > *"Looking ahead, our next immediate deliverable is writing the batch orchestrator script to sweep our 60 samples across word deletion attacks and plot ROC curves. Following that, we will quantify perplexity inflation and evaluate watermark stealing resistance. Thank you, and I look forward to your questions."*

---
