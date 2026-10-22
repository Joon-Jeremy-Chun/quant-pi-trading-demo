# Instructor guide — a small, inspectable software lesson

[Home](../README.md) · [Student start](START_HERE.md) · [한국어 과제](LABS.ko.md) · [Answer notes](SOLUTIONS.ko.md)

## Intended learning outcomes

Students should be able to separate file I/O from pure calculations; trace time-dependent state; distinguish a current observation, a decision and a later action; test inclusive date boundaries; explain a scripted dashboard; and record assumptions alongside an output.

Prerequisites are elementary Python variables, lists, conditions and functions. A browser and Python 3.10+ are enough for the core work. Node is optional for JS validation. No accounts, external datasets, paid models or hardware are required.

## Suggested 90-minute lesson plan

This is an instructor planning estimate, not a measured completion time.

| Segment | Suggested time | Activity | Check understanding |
| --- | --- | --- | --- |
| Setup and arithmetic | 15 min | Open a local copy; run the snapshot script | Which rows enter each average? |
| Time and state | 20 min | Trace the fifth decision and sixth action | Which value was available at decision time? |
| Date filters and report | 20 min | Use fixed dates and vary endpoints | Is the end date included; is anything delivered? |
| Visual state | 20 min | Select teammates, change a synthetic JSON field, use 2D | Which file controls the screen? |
| Explain and test | 15 min | Add a boundary test and write assumptions | What does the passing test establish? |

한국어: 학생이 실행 화면을 복사하는 데서 끝내지 않고, 입력을 하나 바꾸기 전에 결과를 예상하도록 유도하세요. 3D가 제한된 실습실에서는 처음부터 2D 경로를 사용해도 동일한 상태 실습을 진행할 수 있습니다.

## Assessment rubric

| Criterion | Evidence of understanding |
| --- | --- |
| Reproducible setup | Command, version, exact synthetic input and fixed report date |
| Calculation | Correct averages and explicit comparison/equality rule |
| Time ordering | Current decision and next-observation action are separated |
| Testing | One small boundary test with an independently justified expectation |
| Explanation | Assumptions, remaining limits and source of each displayed value |
| Public hygiene | Only invented fixtures; no personal/access/operational records |

Use [the six exercises](LABS.ko.md), followed by [answers](SOLUTIONS.ko.md). Optional extensions should change one assumption at a time. Do not grade a larger toy return as evidence of a better model.

## Boundaries for instructors

The public moving averages are intentionally elementary and independent of private work. Do not infer or request real parameters, positions, device routes, account snapshots or a production topology. The dashboard's fictional roles are not a map of an actual team or private agent system. Lessons stop at local calculations, preview files and browser controls.

The [validation record](VALIDATION.md) documents the tested environment. Re-run local checks when you modify the material; a classroom example is not a deployment template or evidence of profitable trading.
