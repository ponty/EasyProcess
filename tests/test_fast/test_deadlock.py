import os
import sys
import threading
from time import sleep

import pytest
from pyvirtualdisplay.display import Display

from easyprocess import EasyProcess

python = sys.executable
# requirement:  apt install imagemagick

# deadlock
# popen.communicate() hangs
# no deadlock with temp_files

PROG = """
from PIL import Image
Image.new("RGB",(99, 99)).show()
"""

EASYPROCESS_USE_TEMP_FILES = os.environ.get("EASYPROCESS_USE_TEMP_FILES")


def test_dummy():
    pass


# skip these tests for Windows/Mac
# and when 'use_temp_files' is forced by env variable
if sys.platform.startswith("linux") and not EASYPROCESS_USE_TEMP_FILES:

    def test_has_imagemagick():
        assert EasyProcess(["display", "-version"]).call().return_code == 0

    @pytest.mark.timeout(120)
    def test_deadlock_temp_files():
        with Display():
            p = EasyProcess(
                [
                    python,
                    "-c",
                    PROG,
                ],
                use_temp_files=True,
            )
            p.start()
            sleep(2)
            # hangs with pipes
            p.stop()

    @pytest.mark.timeout(120)
    def test_deadlock_pipe():
        with Display():
            p = EasyProcess(
                [
                    python,
                    "-c",
                    PROG,
                ],
                use_temp_files=False,
            )
            p.start()
            sleep(2)

            def start():
                # hangs with pipes
                p.stop()

            thread = threading.Thread(target=start)
            thread.start()

            sleep(6)
            assert thread.is_alive()

        thread.join()
