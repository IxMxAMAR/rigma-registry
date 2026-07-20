# rigma-registry

Community registry of **verified model + quant + flag combos** for
[Rigma](https://github.com/IxMxAMAR/rigma) — hardware-aware local LLM deployment.
`rigma update` pulls this repo; `rigma up` then resolves your exact GPU/RAM to a combo from here.

## Layout

```
gpus.json                          GPU name matchers -> vendor/arch/preferred backends
models/<slug>.json                 model architecture metadata (KV math inputs, GGUF ladder)
combos/<vendor>/<gpu-slug>/ram-<gb>/<use-case>.json    exact-profile combos
combos/_class/vram-<gb>/ram-<gb>/<use-case>.json       tier fallbacks
schema/                            JSON Schemas (CI-enforced)
evidence/                          benchmark evidence attached to verified combos
```

## Verified vs provisional

- A combo **with** a `verified` block was benchmarked on real hardware (`rigma bench` evidence).
- A combo **without** one is *provisional*: research-seeded via the methodology in
  [CONTRIBUTING.md](CONTRIBUTING.md), fit-math checked, but not yet measured. Run it and
  PR your numbers to upgrade it.

## Contributing

1. One combo per PR, validating against `schema/` (`python scripts/validate.py`).
2. Every claim needs a source URL; never fabricate `verified`/`expected` data.
3. To verify a provisional combo: run it via Rigma, attach evidence (tokens/sec, llama.cpp build,
   OS) in `evidence/`, add the `verified` block.

Full research methodology for seeding new combos: [CONTRIBUTING.md](CONTRIBUTING.md).

Data license: **CC-BY-4.0**.
