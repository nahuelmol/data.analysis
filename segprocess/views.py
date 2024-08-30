import numpy as np
import matplotlib.pyplot as plt
import segysak
import pathlib
import xarray as xr
import pandas as pd

from segysak.segy import segy_header_scan
from segysak.segy import segy_loader

from google.colab import drive
from django.shortcuts import render


filename = '/content/drive/MyDrive/samples/3D_gathers_pstm_nmo.sgy'
V3D_path = pathlib.Path(filename)

scan = segy_header_scan(long_data)
with pd.option_context("display.max_rows", 91):
    display(scan)

V3D = xr.open_dataset(
    V3D_path,
    dim_byte_fields={"ILINE_3D":189, "CROSSLINE_3D":193, "ShotPoint":197 },
    extra_byte_fields={"CDP_X":181, "CDP_Y":185 },
)

graph_image(V3D)
graph_traces(V3D)

convolve_traces(V3D)
