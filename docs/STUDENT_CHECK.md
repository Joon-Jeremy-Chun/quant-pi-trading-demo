# Student-guide rehearsal — 2026-10-29

[한국어 시작 안내](START_HERE.ko.md) · [English start](START_HERE.md) · [CI](CI.md)

This was an agent-performed technical rehearsal of the guide, not feedback from a real student. The [record](validation/student-archive-20261029.json) preserves the observed environment, checks and limitations.

## Scenario and result

A public ZIP copy was extracted without Git metadata. A new Python virtual environment was created without pip or inherited third-party packages. The three documented CLI examples, answer snippet, 25 Python cases, documentation check and public-file review ran inside that copy. The documented dashboard CLI started on localhost; its public files were available and an unlisted repository document returned 404. Historical published evidence hashes stayed unchanged.

## Problems corrected

- The public-file checker previously assumed a Git checkout, although the guide offered Download ZIP. It now supports archive mode; `--history` gives an explicit Git-only explanation.
- The reference runner previously overwrote dated evidence and reused a fixed report date. CI now uses read-only `--check`; new saved runs use a dated ignored outputs folder and the actual run date.
- Student instructions now distinguish optional maintainer/history checks from the package-free classroom path.

한국어: 새 ZIP과 제3자 패키지 0개인 환경에서 안내 명령을 따라 실행했습니다. 실제 학생에게 사용성 평가를 받은 것은 아닙니다. 학습 설명의 난이도·소요 시간·이해도는 미확인입니다. 이 검사는 WebGL이나 외부 CDN을 실행하지 않으며, 기존 브라우저 검증과 구분합니다.

## Repeat the technical check

```console
python tools/check_student_archive.py
```

This creates temporary copies/venvs outside the worktree and removes its own temporary files on completion. It prints a location-free JSON summary. Optional `--output` saves a new evidence JSON. It does not contact an owner's device or private operational repository.
