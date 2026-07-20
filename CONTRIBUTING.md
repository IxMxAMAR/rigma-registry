# Contributing

1. One combo per PR, validating against `schema/` (`python scripts/validate.py`).
2. Every claim needs a source URL; never fabricate `verified`/`expected` data.
3. To verify a provisional combo: run it via Rigma, attach evidence (tokens/sec, llama.cpp build,
   OS) in `evidence/`, add the `verified` block.

## Combo research methodology

Input: hardware profile (GPU model, VRAM GB, RAM GB, OS) + use-case (coding | general | agentic).
Output: `combos/<vendor>/<gpu-slug>/ram-<gb>/<use-case>.json` (+ `models/<slug>.json` if the
chosen model is new), validating against `schema/`, every claim carrying a source URL.

### Hard rules

1. Never assume — verify every model's existence, GGUF availability, llama.cpp support status,
   and file sizes via web search + HF API (`HfApi().model_info(repo, files_metadata=True)`).
2. Never fabricate `verified` or `measured` fields — freshly researched combos are provisional
   (no `verified` block). Only real benchmark evidence upgrades them.
3. Every combo carries `sources` (min 1 URL) and dated `notes`.

### Procedure

1. **Candidate models**: search "best local LLM <use-case> <VRAM>GB VRAM <current month+year>"
   (r/LocalLLaMA, benchmark guides). Shortlist 2-3; confirm each is supported in current
   llama.cpp (search "<model> llama.cpp support GGUF").
2. **Architecture math** (for new models, fill models/*.json):
   - From the model card: n_layers, full-attention layer count, kv_heads, head_dim, MoE
     total/active params and expert weight fraction, native context.
   - KV bytes/token = 2 x full_attn_layers x kv_heads x head_dim x cache_bytes
     (f16=2.0, q8_0=1.0625, q4_0=0.5625).
3. **Budget fit** (mirror rigma's resolver, src/rigma/resolve.py):
   - usable_vram = VRAM_MB - os_reserve (win 1200 / linux 400 / mac 0) - 900 compute buffer
   - usable_ram = free_ram_estimate - 2048 (free ~= total - 6GB Windows / - 3GB Linux)
   - dense fits if file+kv <= usable_vram; MoE: offload n_cpu_moe = ceil(overflow / per-layer
     expert MB, where per-layer = file_mb * expert_weight_fraction / n_layers), offloaded part
     must fit usable_ram. Walk quant ladder largest->smallest; ctx from use-case
     (coding 32768, else 16384), halve to 8192 floor.
4. **Backend per GPU arch**: search current "<gpu arch> llama.cpp vulkan vs rocm/cuda benchmark
   <year>". Known verified (2026-07): RDNA4 -> vulkan (ROCm ~20-29% slower); NVIDIA -> cuda.
   Check open llama.cpp issues for arch-specific crashes before recommending anything exotic.
5. **Per-family cache policy**: DeltaNet/hybrid-linear families (qwen3.6) -> k=q8_0 floor
   (q4 K-cache desyncs recurrent state). Plain GQA dense -> q8_0/q8_0 acceptable, f16 if
   VRAM-rich.
6. **Expected perf**: only from published benchmarks of comparable hardware, as a [low, high]
   range, with the source. If none found, omit `expected` entirely.
7. **Validate**: `python scripts/validate.py` must pass. One combo per commit.

### Coverage priorities

Given the coverage matrix (VRAM {8,12,16,24,32} x vendor {nvidia,amd} x RAM {16,32,64}),
the common-hardware cells come first: RTX 3060 12G, RTX 4060 8G, RTX 4070 12G, RTX 4090 24G,
RTX 5090 32G, RX 6600 8G, RX 6700 XT 12G, RX 7800 XT 16G, RX 9070 XT 16G. One combo file per
(profile x use-case); reuse existing models/*.json wherever the fit math allows.

### Slug caveat

Combo directory names must equal rigma's probe slug: lowercase driver-reported device name,
non-alphanumerics -> "-", plus "-<round(vram_mb/1024)>g" (e.g. "amd-radeon-rx-9070-xt-16g").
When seeding without access to the physical card, use the marketing name pattern
("nvidia-geforce-rtx-3060-12g") and note that the directory may need renaming after a real
probe report.
