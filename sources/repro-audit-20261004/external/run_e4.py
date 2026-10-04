"""Run byte-preserved E4 controller with at most two simultaneous downloads."""
import concurrent.futures
import pathlib
import runpy
import sys
original = concurrent.futures.ThreadPoolExecutor
class CappedThreadPoolExecutor(original):
    def __init__(self, max_workers=None, *args, **kwargs):
        super().__init__(min(max_workers or 2, 2), *args, **kwargs)
concurrent.futures.ThreadPoolExecutor = CappedThreadPoolExecutor
root = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'scripts'))
runpy.run_path(str(root / 'scripts/external_validation.py'), run_name='__main__')
