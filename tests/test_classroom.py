"""Offline checks of the public classroom examples; no external accounts."""
from datetime import date, timedelta
from functools import partial
import http.client
from http.server import ThreadingHTTPServer
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import threading
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'tools'))
import demo_backtest as backtest
import demo_dashboard as dashboard
import demo_event_alert as alerts
import demo_signal as signal
import check_publication as publication


def prices(values):
    start=date(2026,1,1)
    return [backtest.PriceRow((start+timedelta(days=i)).isoformat(),float(v)) for i,v in enumerate(values)]


class SignalTests(unittest.TestCase):
    def test_known_fixture_averages(self):
        result=signal.build_demo_signal(signal.load_closes(ROOT/'examples/synthetic_prices.csv'))
        self.assertEqual(result,{'signal':'BUY','short_average':102.6333,'long_average':101.51,'demo_only':True})

    def test_equal_average_is_hold(self):
        self.assertEqual(signal.build_demo_signal([100,100,100])['signal'],'HOLD')

    def test_invalid_values(self):
        for values in [[],[100,101],[100,0,101],[100,-1,101],[100,float('nan'),101],[100,float('inf'),101]]:
            with self.subTest(values=values),self.assertRaises(ValueError):signal.build_demo_signal(values)

    def test_bom_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'prices.csv';path.write_text('date,close\n2026-01-01,10\n',encoding='utf-8-sig')
            self.assertEqual(signal.load_closes(path),[10.0])


class BacktestTests(unittest.TestCase):
    def run_example(self,values,**kwargs):
        return backtest.run_demo_backtest(prices(values),3,5,kwargs.get('cash',10000))

    def test_window_boundaries(self):
        self.assertIsNone(backtest.moving_average([1,2],3))
        self.assertEqual(backtest.moving_average([1,2,3],2),2.5)
        for window in [0,-1,True,1.5]:
            with self.assertRaises(ValueError):backtest.moving_average([1,2,3],window)

    def test_decision_does_not_fill_at_same_close(self):
        result=self.run_example([100,100,100,100,200])
        self.assertEqual(result['events'][-1]['signal'],'BUY')
        self.assertEqual(result['events'][-1]['action'],'NONE')
        self.assertEqual(result['final_equity'],10000)

    def test_fill_uses_next_observation_price(self):
        result=self.run_example([100,100,100,100,200,50])
        event=result['events'][-1]
        self.assertEqual(event['action'],'ENTER')
        self.assertEqual(event['shares'],200)
        self.assertEqual(event['decision_date'],'2026-01-05')
        self.assertEqual(result['execution_assumption'],'next_observation_close')

    def test_exit_uses_previous_decision(self):
        result=self.run_example([100,100,100,100,200,50,40,30])
        self.assertEqual(result['events'][-2]['signal'],'FLAT')
        self.assertEqual(result['events'][-1]['action'],'EXIT')
        self.assertEqual(result['final_equity'],6000)

    def test_prefix_causality(self):
        prefix=[100,100,100,100,200,50]
        short=self.run_example(prefix)
        longer=self.run_example(prefix+[2,900,3])
        self.assertEqual(short['events'],longer['events'][:len(prefix)])

    def test_constant_series_and_benchmark(self):
        result=self.run_example([100]*8)
        self.assertEqual(result['final_equity'],10000)
        self.assertEqual(result['buy_hold_equity'],10000)
        self.assertTrue(all(e['action']=='NONE' for e in result['events']))

    def test_cash_and_price_contracts(self):
        for cash in [0,-1,float('inf'),float('nan')]:
            with self.assertRaises(ValueError):self.run_example([100]*6,cash=cash)
        for value in [0,-1,float('nan')]:
            with self.assertRaises(ValueError):self.run_example([100]*5+[value])

    def test_date_order_and_window_contracts(self):
        for rows in [prices([1]*6)[::-1],[backtest.PriceRow('2026-01-01',100)]*6]:
            with self.assertRaises(ValueError):backtest.run_demo_backtest(rows,3,5,10000)
        with self.assertRaises(ValueError):backtest.run_demo_backtest(prices([100]*6),5,3,10000)
        with self.assertRaises(ValueError):self.run_example([100]*3)


class ReportTests(unittest.TestCase):
    def test_inclusive_window(self):
        today=date(2026,5,21)
        events=[alerts.CorporateEvent('DEMO',today+timedelta(days=d),'example',str(d),'https://example.com') for d in [-1,0,14,15]]
        self.assertEqual([e.title for e in alerts.upcoming_events(events,today,14)],['0','14'])

    def test_zero_and_negative_window(self):
        today=date(2026,5,21)
        events=alerts.load_events(ROOT/'examples/corporate_events.csv')
        self.assertEqual(alerts.upcoming_events(events,today,0),[])
        with self.assertRaises(ValueError):alerts.upcoming_events(events,today,-1)

    def test_fixed_date_and_fictional_fixtures(self):
        selected=alerts.upcoming_events(alerts.load_events(ROOT/'examples/corporate_events.csv'),date(2026,5,21),14)
        self.assertEqual([e.symbol for e in selected],['DEMO-A','DEMO-B','DEMO-C','DEMO-D'])

    def test_text_and_local_outbox(self):
        email=alerts.render_email([],date(2026,5,21),14)
        slack=alerts.render_slack([],date(2026,5,21),14)
        self.assertIn('No events',email)
        with tempfile.TemporaryDirectory() as folder:
            alerts.write_outbox(Path(folder),email,slack)
            self.assertEqual((Path(folder)/'email_message.txt').read_text(encoding='utf-8'),email+'\n')
            self.assertEqual(len(list(Path(folder).iterdir())),2)


class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.previous_root=dashboard.DASHBOARD_ROOT
        dashboard.DASHBOARD_ROOT=Path(cls.temp.name).resolve()
        for name in dashboard.PUBLIC_ASSETS:shutil.copyfile(cls.previous_root/name,dashboard.DASHBOARD_ROOT/name)
        (dashboard.DASHBOARD_ROOT/'not-public.txt').write_text('classroom fixture',encoding='utf-8')
        class QuietHandler(dashboard.DashboardHandler):
            def log_message(self,*args):pass
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(dashboard.DASHBOARD_ROOT)))
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
        dashboard.DASHBOARD_ROOT=cls.previous_root;cls.temp.cleanup()

    def request(self,path,method='GET'):
        conn=http.client.HTTPConnection('127.0.0.1',self.server.server_port,timeout=3)
        conn.request(method,path);response=conn.getresponse()
        result=response.status,dict(response.getheaders()),response.read();conn.close();return result

    def test_four_public_assets_and_root(self):
        for path in ['/',*('/'+n for n in dashboard.PUBLIC_ASSETS)]:
            with self.subTest(path=path):self.assertEqual(self.request(path)[0],200)

    def test_existing_unlisted_file_is_blocked(self):
        self.assertEqual(self.request('/not-public.txt')[0],404)

    def test_traversal_and_source_are_blocked(self):
        for path in ['/../README.md','/%2e%2e/README.md','/src/demo_signal.py','/.env','/.git/config','/extra/']:
            with self.subTest(path=path):self.assertEqual(self.request(path)[0],404)

    def test_head_and_headers(self):
        status,headers,body=self.request('/?view=2d','HEAD')
        self.assertEqual(status,200);self.assertEqual(body,b'')
        self.assertEqual(headers['Cache-Control'],'no-store')
        self.assertEqual(headers['Referrer-Policy'],'no-referrer')


class PublicationTests(unittest.TestCase):
    def test_localhost_is_permitted(self):
        self.assertEqual(publication.inspect_text('fixture','http://127.0.0.1:8000/'),[])

    def test_non_loopback_and_token_locations_only(self):
        address='.'.join(['10','23','45','67'])
        token='g'+'hp_'+'A'*36
        findings=publication.inspect_text('fixture',address+'\n'+token)
        self.assertEqual({f['rule'] for f in findings},{'non-localhost-address','github-token'})
        self.assertTrue(all(set(f)=={'path','line','rule'} for f in findings))


if __name__=='__main__':unittest.main()
