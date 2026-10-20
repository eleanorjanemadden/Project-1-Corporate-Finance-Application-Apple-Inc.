import unittest
import pandas  # Import dependencies before starting Streamlit script timeout.
import pyarrow
from pathlib import Path
from streamlit.testing.v1 import AppTest

class WorkbenchChecks(unittest.TestCase):
    def test_controls_reset_and_real_failure_demo(self):
        app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=60).run()
        self.assertEqual(len(app.exception),0)
        base=app.metric[0].value
        app.slider[0].set_value(2.).run()
        self.assertNotEqual(app.metric[0].value,base)
        app.button(key="reset_base").click().run()
        self.assertEqual(app.metric[0].value,base)
        app.button(key="run_demo").click().run()
        self.assertTrue(any('DEMONSTRATION CHECK FAILED' in x.value for x in app.error))
        app.button(key="clear_demo").click().run()
        self.assertFalse(any('DEMONSTRATION CHECK FAILED' in x.value for x in app.error))
        app.slider[1].set_value(-2.).run()
        self.assertLess(float(app.metric[0].value.strip('$')),float(base.strip('$')))
        self.assertEqual(len(app.error),0)
        app.button(key="reset_base").click().run()
        self.assertEqual(app.metric[0].value,base)
        self.assertEqual(len(app.exception),0)

    def test_basis_selector_preserves_each_baseline(self):
        app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=60).run()
        dated=app.metric[0].value
        app.selectbox[0].set_value('Retrospective FY2025 illustration').run()
        self.assertEqual(app.metric[0].value,'$125.23')
        app.slider[0].set_value(2.).run()
        self.assertEqual(app.metric[0].value,'$134.95')
        app.button(key='reset_base').click().run()
        self.assertEqual(app.metric[0].value,'$125.23')
        app.selectbox[0].set_value('Dated July 31, 2026').run()
        self.assertEqual(app.metric[0].value,dated)
        self.assertEqual(len(app.exception),0)
