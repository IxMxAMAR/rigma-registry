# Evidence

Benchmark evidence backing `verified` combos. One JSON file per verification:
`<gpu-slug>--<model-slug>--<date>.json`, produced by `rigma bench --evidence` (lands in Rigma M5).
Until then, a minimal hand-written record is fine:

```json
{
  "combo": "amd/amd-radeon-rx-9070-xt-16g/ram-16/coding.json",
  "date": "2026-07-06",
  "llamacpp": "b9867",
  "os": "windows",
  "measured": {"tg_tps": 57.1, "pp_tps": 689, "prompt_tokens": 4020}
}
```
