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


