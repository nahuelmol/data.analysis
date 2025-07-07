import pandas as pd
import segysak
import xarray as xr

def filetype(filename, form):
    ending = ''
    for each in filename[::-1]:
        ending.push(each)
        if each == '.':
            break
    myformat = ending[::-1]
    if(myformat == form):
        return true
    else:
        return false

def CSVreader(fileobject):
    df = pd.read_csv(fileobjetc, sep=';', encoding='utf-8')
    print(df.info())
    print(df.head())
    print(df.describe())

def SEGYreader(fileobject):
    from segysak.segy import segy_header_scan
    from segysak.segy import segy_loader
    
    filepath = fileobject #maybe I have to download the file first and later include it here

    header = segy_header_scan(filpath)
    with pd.option_context("display.max_rows", 91):
        pass
    dt = header.loc["TRACE_SAMPLE_INTERVAL"]["mean"] /100
    sr = 1000 /dt

    print("Trace sample interval -> ", header.loc["TRACE_SAMPLE_INTERVAL"]["count"])
    print("intervalo -> " , dt)
    print("sampling rate -> ", sr)
    print("offset -> ", header.loc["offset"]["count"])
    print("CDP ->", header.loc["CDP"]["count"])

    xr.open_dataset(
            V3D_path,
            dim_byte_fields={"ILINE_3D":189, "CROSSLINE_3D":193,"ShotPoint":197},
            extra_byte_fields={"CDP_X":181, "CDP_Y":185},
    }
    V3D.data.transpose("ILINE_3D", "CROSSLINE_3D", "ShotPoint", "samples", transpose_coords=True).sel(
        ILINE_3D=1290, CROSSLINE_3D=1150
    ).plot(yincrease=False, cmap="seismic_r")

    plt.ylabel("TWT")
    plt.xlabel("XLINE")

    ## segio
    import segyio
    with segyio.open(V2D_path, ignore_geometry=True) as segyfile:
        traces = segyfile.trace
        xr_traces = xr.DataArray(traces).transpose("dim_1", "dim_0")
        xr_traces.plot()
        plt.gca().invert_yaxis()
        plt.show()
    
def DATreader(fileobject):
    pass
def ZIPreader(fileobject):
    pass
def TARreader(fileobject):
    pass

def FileReader(fileobject):
    filename = fileobject.filename
    if filetype(filename, 'csv'):
        CSVreader(fileobject)
    elif filetype(filename, 'dat'):
        DATreader(fileobject)
    elif filetype(filename, 'segy'):
        SEGYreader(fileobject)
    elif filetype(filename, 'zip'):
        ZIPreader(fileobject)
    elif filetype(filename, 'tar'):
        TARreader(fileobject)
    else:
        print("filetype is not recognized")

        

