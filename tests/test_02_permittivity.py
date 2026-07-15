import pytest
import subprocess
import os
import xarray as xr
import pandas as pd
import sys


@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10 or later.")
def test_case(datadir):
    os.chdir(datadir)

    assert subprocess.run(
        [
            "yadg",
            "extract",
            "touchstone.snp",
            "touchstone-s1p.zip",
            "touchstone-s1p.nc",
        ],
        check=True,
    )
    assert os.path.exists("touchstone-s1p.nc")

    dt = xr.open_datatree("touchstone-s1p.nc")
    assert dt.dims == {"uts": 5, "frequency": 10001}
    dt.close()

    assert subprocess.run(
        [
            "dgpost",
            "--patch",
            "touchstone-s1p",
            "recipe.Qf.yml",
        ],
        check=True,
    )
    assert os.path.exists("touchstone-s1p.Qf.pkl")
    assert os.path.exists("touchstone-s1p.Qf.xlsx")
    assert os.path.exists("touchstone-s1p.Qf.png")

    ret = pd.read_pickle("touchstone-s1p.Qf.pkl")
    ref = pd.read_pickle("ref.touchstone-s1p.Qf.pkl")
    pd.testing.assert_frame_equal(ret, ref, check_exact=False)
