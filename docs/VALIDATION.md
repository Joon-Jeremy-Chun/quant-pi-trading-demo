# Validation evidence

[Home](../README.md) · [Repairs](REPAIRS.md) · [Public boundary](PUBLIC_BOUNDARY.md)

## Commands

```console
python -m unittest discover -s tests -v
python tools/verify_classroom.py
node tests/test_dashboard_state.cjs
node --check examples/dashboard_3d/app.js
python tools/validate_documentation.py
python tools/check_publication.py --history
```

The Python tests and demos use only the standard library. Node is optional for JS checks. The [results JSON](validation/results.json) and three CLI previews in docs/validation preserve the 2026-10-21 run. The current reference runner writes new evidence to a dated outputs/classroom-check folder, or checks the historical previews read-only with --check. Those previews contain only synthetic fixture output; outbox tests use temporary folders.

## Observed checks

The 2026-10-21 pass used Python 3.11.5 and passed 22 Python cases plus nine JavaScript validation cases. Cases cover numeric contracts, decision/action timing, prefix causality, date endpoints, local output and the four-file server allowlist. Source syntax and documentation structure were checked separately.

An automated browser pass used a new headless Chrome profile with software WebGL rendering and the actual public local server. Eleven checks passed: intentional 2D, four teammate buttons, Next step, manual selection, Play/Pause, Reset, no CDN requests in the intentional 2D path, mobile width without overflow, usable default route, WebGL canvas and default-route progression. The default route rendered 3D successfully. [Browser evidence](validation/browser.json).

The [3D screenshot](../assets/dashboard-3d.png), [2D screenshot](../assets/dashboard-2d.png) and [mobile screenshot](../assets/dashboard-mobile.png) show invented data only. Source and screenshots were manually reviewed; publication checks also reviewed text blobs in this public repository's own history. No private repository, device or account was accessed for the demo.

These checks establish the stated classroom behaviors in the observed environment. They do not validate investment performance, market execution, message delivery, device deployment or every browser/platform combination. CDN availability can vary; the local 2D path remains a separate tested option.

## 2026-10-29 automated continuity

Current local checks pass 25 Python cases and nine JS state cases. The [ZIP rehearsal](STUDENT_CHECK.md) uses a new package-free virtual environment and preserves the prior evidence. [CI](CI.md) runs the public checks on Linux/Windows; actual hosted-run status is confirmed separately after publication. These are operational verification measurements, not a new trading or model-comparison experiment.

Publication verification: [run 40967897157](https://github.com/Joon-Jeremy-Chun/quant-pi-trading-demo/actions/runs/40967897157) completed successfully for `b34b1cde99fb33098e3aef51b90db94f7d72131f`, including all four Python/OS combinations and the Node job. The [machine-readable record](validation/ci-20261029.json) preserves the observed conclusions. Original checkout HEAD/status and 20 original file hashes remained unchanged.
