# Classroom continuous checks

[Home](../README.md) · [Workflow](../.github/workflows/classroom-ci.yml) · [Student rehearsal](STUDENT_CHECK.md)

The workflow runs on pushes to main, pull requests targeting main, and manual dispatch. It checks the public classroom repository only. It uses GitHub-hosted Linux/Windows runners, Python 3.10/3.13, and a separate Node.js 22 job.

| Check | Purpose |
| --- | --- |
| 25 Python cases | Numeric contracts, time ordering, dates, local files/server boundaries, ZIP support and evidence preservation |
| `verify_classroom.py --check` | Match three published CLI previews and execute the answer snippet without overwriting historical evidence |
| `check_student_archive.py` | Create a public ZIP, run the instructions in a zero-package venv, and start the documented local server |
| Documentation/source check | Local Markdown targets, fences, UTF-8, Python syntax and SVG XML |
| Publication/history check | Sensitive-pattern and URL-host review of current public text and complete public Git history |
| Node syntax / nine state cases | Browser-source parsing and synthetic JSON contracts |

The only workflow permission is contents:read. Checkout does not persist credentials. Official actions are pinned to reviewed full commit IDs, and complete history is fetched for the history check. No repository secrets, device connection, remote deployment or message delivery are configured. Browser WebGL/CDN rendering remains the separately recorded manual/automated browser evidence from 2026-10-21; the new CI exercises the local 2D HTTP entry point without CDN access.

Read the run result in [Actions](https://github.com/Joon-Jeremy-Chun/quant-pi-trading-demo/actions/workflows/classroom-ci.yml). A passing workflow is an automated check, not a configured branch-protection rule or a substitute for source/screenshot review. If the teaching fixture changes intentionally, review and update its expected preview separately.

```console
python -m unittest discover -s tests -v
python tools/verify_classroom.py --check
python tools/check_student_archive.py
python tools/validate_documentation.py
python tools/check_publication.py --history
node tests/test_dashboard_state.cjs
```

For a ZIP copy, omit `--history`; current public-file review works without Git. Ordinary verification is recorded in logs/handoffs, not relabeled as a model-research experiment.

References: [GitHub Python CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/python), [workflow security](https://docs.github.com/en/actions/reference/security/secure-use).
