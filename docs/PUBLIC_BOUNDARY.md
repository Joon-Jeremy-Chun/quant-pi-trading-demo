# Public classroom boundary

[Home](../README.md) · [Implemented architecture](architecture.md)

## What this repository is allowed to teach

Local software organization, CSV/JSON contracts, elementary public arithmetic, time-ordering in a toy simulation, inclusive date filtering, text rendering, tests and a fictional browser scene. All examples are understandable from this repository alone.

## What must remain outside it

Private strategy logic or parameters; actual training/optimization/model artifacts; account identifiers and holdings; orders and operational logs; credentials, keys and recipients; device addresses, hostnames, remote-access instructions, network routes and deployment configuration. None is needed for these lessons. Do not copy from private folders, machines or screenshots when extending the demo.

The only server address used in the guide is the student's own localhost. It identifies no owner's device. A Raspberry Pi is neither required nor contacted. The repository name records the original public-demo theme, not an invitation or procedure to connect to an operational device.

## Concrete code boundaries

- Python scripts read only caller-supplied local fixtures; no broker, mail or remote-shell library is imported.
- Event renderers return text; outbox creation is explicitly requested and stays local.
- The server binds to loopback and allows only four known classroom assets.
- The browser fetches local sample JSON; optional 3D imports come from a pinned public CDN. Intentional 2D mode skips those imports.
- `.env.example` is explanatory and is not loaded by the programs.

## Publication review

`python tools/check_publication.py` inspects the public working tree and reports file/line/rule locations without echoing suspected content. `--history` also reviews public-repository text blobs in its own Git history. It does not inspect any private repository. The check looks for known credential/key shapes, non-localhost addresses, private path patterns and unreviewed URL hosts; manual source and screenshot review remains part of publication.

한국어: 자료의 출처를 합성 fixture와 이미 공개된 코드로 제한합니다. 실제 장치 접속·전략·계정·운영 기록은 교육용 예시에 필요하지 않습니다. 오류를 질문할 때도 합성 입력과 관련 코드만 공유하세요.

## Archive copies and CI

The current-tree publication check supports Download ZIP without Git. Full-history review requires a non-shallow Git checkout; it fails with an explanation if history is unavailable. [CI](CI.md) uses full public history, read-only permissions and no secrets. Neither ZIP rehearsal nor CI accesses private devices or operational files.
