from pathlib import Path
import pandas as pd
import numpy as np
import logging

#patching
import unittest
try:
    # python 3.4+ should use builtin unittest.mock not mock package
    from unittest.mock import patch
except ImportError:
    from mock import patch

#app
import methylcheck

TESTPATH = 'tests'
PROCESSED_450K = Path('docs/example_data/GSE69852')
PROCESSED_MOUSE = Path('docs/example_data/mouse_test')
PROCESSED_EPIC = Path('docs/example_data/epic')

class TestControlsReporterForMouse(): #unittest.TestCase):

    mouse = methylcheck.reports.ControlsReporter(PROCESSED_MOUSE)
    mouse.process()
    mouse.save()

    def test_mouse(self):
        expected_outfile = 'mouse_test_QC_Report.xlsx'
        if not Path(PROCESSED_MOUSE, expected_outfile).exists():
            raise FileNotFoundError(f"QC Report file missing for folder: {PROCESSED_MOUSE}")
        results = pd.read_excel(Path(PROCESSED_MOUSE, expected_outfile))
        if results.shape != (7,33):
            raise AssertionError(f"Result file shape differs: {results.shape} should be (7,33)")
            # float("NaN")
        if not all(results['Result'].values[1:] == ['FAIL (0.59)', 'FAIL (0.52)', 'FAIL (0.47)', 'FAIL (0.39)', 'FAIL (0.47)', 'FAIL (0.49)']):
            # first value is NaN and NaN cannot be equal to NaN, so skipping.
            #v0.8.1 --> ['FAIL (0.59)', 'FAIL (0.52)', 'FAIL (0.47)', 'FAIL (0.39)', 'FAIL (0.47)', 'FAIL (0.49)']
            #v0.7.5 --> print('v0.7.5', results['Result'].values[1:5], ['FAIL (0.62)', 'FAIL (0.56)', 'FAIL (0.46)', 'FAIL (0.47)'])
            #v0.7.4 --> print(results['Result'].values[1:5], ['FAIL (0.7)', 'FAIL (0.64)', 'FAIL (0.53)', 'MARGINAL (0.56)'])
            import pdb;pdb.set_trace()
            raise AssertionError(f"Values in result column differ: Found {results['Result'].values}")
        if Path(PROCESSED_MOUSE,expected_outfile).exists():
            Path(PROCESSED_MOUSE,expected_outfile).unlink()
