"""Repeat synthetic fixture calculations and save public-only result evidence."""
from datetime import date
from datetime import datetime, timezone
import argparse
import io
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'src'))
import demo_signal
import demo_backtest
import demo_event_alert


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='Compare CLI previews with published fixtures; write no files.')
    parser.add_argument('--output-dir', type=Path,
                        help='Optional new evidence directory; defaults to a dated outputs folder.')
    args = parser.parse_args()
    snapshot=demo_signal.build_demo_signal(demo_signal.load_closes(ROOT/'examples/synthetic_prices.csv'))
    result=demo_backtest.run_demo_backtest(demo_backtest.load_prices(ROOT/'examples/synthetic_prices.csv'),3,5,10000)
    events=demo_event_alert.upcoming_events(demo_event_alert.load_events(ROOT/'examples/corporate_events.csv'),date(2026,5,21),14)
    assert snapshot['short_average']==102.6333 and snapshot['long_average']==101.51
    assert result['final_equity']==10187.75 and result['execution_assumption']=='next_observation_close'
    assert [e.symbol for e in events]==['DEMO-A','DEMO-B','DEMO-C','DEMO-D']
    text=(ROOT/'docs/SOLUTIONS.ko.md').read_text(encoding='utf-8')
    blocks=re.findall(r'```python\n(.*?)\n```',text,re.S)
    assert len(blocks)==1
    namespace={'__name__':'student_answer'}
    exec(compile(blocks[0],'student_answer','exec'),namespace)
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(namespace['DateBoundary'])
    answer=unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    assert answer.wasSuccessful()
    target = args.output_dir or (ROOT/'outputs'/'classroom-check'/
                                datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    if not args.check:
        target.mkdir(parents=True, exist_ok=True)
    commands=[
        ('signal.txt',['src/demo_signal.py','--prices','examples/synthetic_prices.csv']),
        ('backtest.txt',['src/demo_backtest.py','--prices','examples/synthetic_prices.csv']),
        ('event_report.txt',['src/demo_event_alert.py','--calendar','examples/corporate_events.csv','--today','2026-05-21','--lookahead-days','14']),
    ]
    for filename,command_args in commands:
        completed=subprocess.run([sys.executable,*command_args],cwd=ROOT,encoding='utf-8',text=True,capture_output=True,timeout=10,check=True)
        assert not completed.stderr
        if args.check:
            expected=(ROOT/'docs/validation'/filename).read_text(encoding='utf-8')
            assert completed.stdout == expected, f'Published preview changed: {filename}'
        else:
            (target/filename).write_text(completed.stdout,encoding='utf-8')
    report={'date':date.today().isoformat(),'python':platform.python_version(),'synthetic_only':True,
            'signal':snapshot,'backtest':result,'selected_events':[e.symbol for e in events],
            'answer_snippet_tests':answer.testsRun,'cli_previews':[name for name,_ in commands],
            'all_passed':True,'scope':'Local synthetic calculations only; no external accounts, devices or delivery.'}
    if not args.check:
        (target/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'mode':'check' if args.check else 'save','synthetic_only':True,
                      'cli_previews':len(commands),'answer_snippet_tests':answer.testsRun,
                      'all_passed':True}))


if __name__=='__main__':main()
