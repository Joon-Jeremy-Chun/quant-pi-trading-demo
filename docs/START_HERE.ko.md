# 학생용 시작 안내 — 설치 확인부터 결과 해석까지

[처음 화면](../README.md) · [English](START_HERE.md) · [실습 과제](LABS.ko.md) · [해설](SOLUTIONS.ko.md)

## 이 실습에서 배우는 것

파일 읽기 → 입력 확인 → 간단한 계산 → 시간에 따른 상태 변화 → 결과 설명 → 테스트 순서를 익힙니다. 모든 자료는 합성 가격·가상 일정·가상 캐릭터입니다. 개인 PC에서 끝나는 예제이므로 Raspberry Pi나 원격 컴퓨터에 접속할 필요가 없습니다.

처음에는 평균·조건문·함수·리스트를 조금 읽을 수 있으면 충분합니다. 낯선 부분은 [코드 읽기 안내](CODE_WALKTHROUGH.md)와 함께 진행하세요. Python 실행 파일과 브라우저 외에 별도 패키지·계정·API 키·환경변수 설정은 필요하지 않습니다.

## 1단계 · Python과 실습 폴더 확인

Python 3.10 이상이 필요합니다. 터미널에서 확인합니다.

```console
python --version
```

Windows에 Python launcher가 있으면 다음 명령도 가능합니다.

```console
py -3 --version
```

GitHub의 **Code → Download ZIP**으로 내려받아 압축을 풀거나, Git을 사용하는 경우 다음을 실행합니다.

```console
git clone https://github.com/Joon-Jeremy-Chun/quant-pi-trading-demo.git
cd quant-pi-trading-demo
```

README.md·src·examples가 보이는 폴더에서 터미널을 여세요. Windows 파일 탐색기에서는 해당 폴더의 주소 표시줄에 `powershell`을 입력해 열 수 있습니다. ZIP 내부가 아니라 압축 해제한 폴더여야 합니다. 명령이 없으면 Python을 설치한 뒤 새 터미널을 열어 확인합니다. [Python 공식 사이트](https://www.python.org/).

## 2단계 · 평균 계산 하나부터 실행

```console
python src/demo_signal.py --prices examples/synthetic_prices.csv
```

기본 파일을 바꾸지 않았다면 출력은 다음과 같습니다.

```text
signal: BUY
short_average: 102.6333
long_average: 101.51
demo_only: True
```

CSV에는 날짜와 close라는 두 열, 관측값 10개가 있습니다. 마지막 세 값은 102.60·102.20·103.10이며 평균은 약 102.6333입니다. 전체 10개 평균은 101.51입니다. 앞 값이 더 크므로 공개된 간단한 조건식이 BUY라는 **문자열**을 반환합니다. 값이 같거나 더 작으면 HOLD입니다. 여기서 계산은 끝나며 어떤 계정에도 전달하지 않습니다.

확인할 질문: 가격 2개만 넣으면 왜 오류일까요? 0·음수·무한대·NaN을 가격으로 넣지 못하게 하는 이유는 무엇일까요? [함수 안내](CODE_WALKTHROUGH.md).

## 3단계 · 판단과 가상 처리 시점을 구분

```console
python src/demo_backtest.py --prices examples/synthetic_prices.csv
```

이번 프로그램은 짧은 창 3개·긴 창 5개를 비교합니다. 앞 단계의 “전체 평균”과 다른 정의입니다. 매일 출력되는 행의 의미:

| 필드 | 뜻 |
| --- | --- |
| date / close | 그 행의 가상 날짜와 관측값 |
| signal | 현재 행까지 보고 계산한 판단 |
| executed_signal | 이전 행에서 만들어 이번 행에서 처리한 판단 |
| action | NONE·ENTER·EXIT 중 이번 행의 상태 변경 |
| equity | 가상 현금 + 가상 보유 수량 × 현재 관측값 |

처음 4개 행은 긴 창이 부족하여 WAIT입니다. 1월 8일 다섯 번째 관측값에서 BUY가 나와도 그날 바로 처리하지 않습니다. 다음 관측일인 1월 9일의 101.20을 사용해 가상 수량을 계산합니다. 이 프로그램의 가정은 `next_observation_close`입니다. 다음 날 시가 체결을 흉내 낸 것이 아니며 날짜 사이의 실제 장 운영도 모델링하지 않습니다.

기본 결과는 가상 단위 10000 → 10187.75, 약 1.88%입니다. 이것은 수정 후 프로그램의 정답 확인용 숫자입니다. 합성 가격·비용 0·소수 수량 허용·완전 체결 가정이므로 투자 성과로 해석하지 않습니다. [상태와 계산 상세](BACKTEST.md).

## 4단계 · 날짜를 고정해 가상 일정 보고서 만들기

```console
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14
```

오늘 날짜 옵션을 생략하면 실행한 PC의 오늘을 사용하여 예시 일정과 다른 결과가 나올 수 있습니다. 비교 실습에서는 위의 고정 날짜를 유지합니다. 5월 21일부터 6월 4일까지 양 끝을 포함하며 DEMO-A·B·C·D 네 개가 선택됩니다. 6월 12일의 DEMO-E는 제외됩니다. 이름·일정은 모두 가상이고 출처 모양의 example.com 주소에 접속하지 않습니다.

보고서는 터미널에 표시되는 텍스트입니다. 파일로 보고 싶으면 다음을 실행합니다.

```console
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14 --outbox outputs/classroom
```

`outputs/classroom/email_message.txt`와 `slack_message.txt` 두 파일이 생깁니다. 다시 실행하면 같은 이름의 미리보기를 덮어씁니다. 이 파일들은 로컬 미리보기이며 이메일·Slack 발송 설정은 없습니다. [보고서 해설](event_alert_demo.md).

## 5단계 · 같은 PC에서 대시보드 열기

```console
python src/demo_dashboard.py
```

브라우저 주소에 **http://127.0.0.1:8000/**를 입력합니다. `127.0.0.1`은 지금 사용 중인 자기 PC를 가리키는 loopback 주소입니다. 소유자의 Pi 주소가 아닙니다. 터미널은 켜 둔 채 브라우저를 사용하고 종료할 때 터미널에서 **Ctrl+C**를 누릅니다.

포트가 사용 중이면:

```console
python src/demo_dashboard.py --port 8001
```

이번에는 터미널에 표시된 **http://127.0.0.1:8001/**로 엽니다. 3D 모듈을 인터넷에서 받을 수 없는 경우 **http://127.0.0.1:8000/?view=2d**를 사용합니다. 지정한 포트도 함께 맞추세요. 파일을 더블클릭해 여는 대신 서버를 사용하는 이유는 브라우저가 JSON을 가져오는 방식 때문입니다.

첫 3D 화면은 pinned Three.js 0.160.0 모듈을 jsDelivr에서 가져옵니다. CDN 요청에는 일반적인 네트워크 메타데이터가 따릅니다. 명시적 2D 경로에서는 해당 요청을 하지 않습니다. 샘플 JSON은 로컬 서버에서만 가져오며 프로그램에 업로드 기능은 없습니다.

Pip·Nova·Remy·Fern을 선택해 입력·출력·역할을 읽고, Next step·Play/Pause·Reset을 눌러 보세요. 활동은 정해진 예시 대본이며 실제 작업자·프로세스 상태를 읽은 것이 아닙니다. [화면/JSON 수정 안내](dashboard_3d.ko.md).

## 6단계 · 테스트하고 설명하기

```console
python -m unittest discover -s tests -v
```

현재 버전의 Python 집중 테스트는 22개입니다. 평균의 경계값, 다음 관측 처리, 시간 순서, 날짜 필터, 로컬 파일 출력, 공개 파일 제공 범위를 검사합니다. 테스트 통과는 실제 거래 성과나 모든 환경에서의 동작을 보장하는 말과 다릅니다.

선택 사항: Node.js가 있으면 `node tests/test_dashboard_state.cjs`로 JSON 상태 검사 9개를 실행할 수 있습니다. Node는 기본 Python 실습과 대시보드 사용에 필수는 아닙니다.

## 자주 만나는 문제

| 증상 | 먼저 확인할 것 |
| --- | --- |
| python 명령을 찾지 못함 | Windows의 `py -3`; 설치 버전과 새 터미널 |
| 파일이 없다는 오류 | 저장소 루트인지, ZIP을 풀었는지, 전체 폴더를 받았는지 |
| 3.10 문법 관련 오류 | 실행 중인 Python 버전과 다른 Python이 선택되었는지 |
| 브라우저 연결 실패 | 서버 터미널이 실행 중인지, 같은 PC인지, 포트가 일치하는지 |
| 포트가 이미 사용 중 | `--port 8001`로 바꾸고 브라우저 주소도 변경 |
| 3D 대신 2D가 보임 | WebGL/CDN 사용 가능 여부; 2D에서도 기본 실습 가능 |
| JSON을 고친 뒤 샘플 오류 | 따옴표·쉼표·배열·중복 id·steps의 agent 참조 확인 |
| 일정 결과가 비어 있음 | `--today 2026-05-21`을 포함했는지 |
| 가격/날짜 ValueError | 양수·유한 값, 오름차순의 중복 없는 YYYY-MM-DD 날짜 |
| Node 명령을 찾지 못함 | 선택 검사만 생략 가능; Python 기본 실습에는 필요 없음 |

실습 중 막혔을 때는 **실행 명령·오류 메시지·합성 입력**만 함께 정리하면 재현에 도움이 됩니다. 계정·비밀번호·개인 문서·장치 접속 설정을 붙여 넣을 필요가 없습니다. 다음은 [과제](LABS.ko.md), 풀이 후에는 [해설](SOLUTIONS.ko.md)로 이어가세요.
