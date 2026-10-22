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

The Python tests and demos use only the standard library. Node is optional for JS checks. The reference runner writes a scoped [results JSON](validation/results.json) and three CLI output previews in docs/validation. Those previews contain only synthetic fixture output; outbox tests use temporary folders.

## Observed checks

The 2026-10-21 pass used Python 3.11.5 and passed 22 Python cases plus nine JavaScript validation cases. Cases cover numeric contracts, decision/action timing, prefix causality, date endpoints, local output and the four-file server allowlist. Source syntax and documentation structure were checked separately.

An automated browser pass used a new headless Chrome profile with software WebGL rendering and the actual public local server. Eleven checks passed: intentional 2D, four teammate buttons, Next step, manual selection, Play/Pause, Reset, no CDN requests in the intentional 2D path, mobile width without overflow, usable default route, WebGL canvas and default-route progression. The default route rendered 3D successfully. [Browser evidence](validation/browser.json).

The [3D screenshot](../assets/dashboard-3d.png), [2D screenshot](../assets/dashboard-2d.png) and [mobile screenshot](../assets/dashboard-mobile.png) show invented data only. Source and screenshots were manually reviewed; publication checks also reviewed text blobs in this public repository's own history. No private repository, device or account was accessed for the demo.

These checks establish the stated classroom behaviors in the observed environment. They do not validate investment performance, market execution, message delivery, device deployment or every browser/platform combination. CDN availability can vary; the local 2D path remains a separate tested option.
