def grapher(V3D):
    fig, ax1 = plt.subplots(ncols=1, figsize=(15, 8))
    V3D.data.transpose("ILINE_3D", "CROSSLINE_3D", "ShotPoint", "samples", transpose_coords=True
    ).sel(
        ILINE_3D=1290, CROSSLINE_3D=1150
    ).plot(yincrease=False, cmap="gray")

    plt.ylabel("TWT")
    plt.xlabel("XLINE")
    #plt.show()

def graph_traces(V3D):
    air1 = V3D.isel(ILINE_3D=0, CROSSLINE_3D=0).data
    #para una misma imagen sismica (air1) puedo pintar cada traza
    plt.figure(figsize=(15, 8))

    plt.subplot(4, 1, 1)
    plt.plot(air1[0])

    plt.subplot(4, 1, 2)
    plt.plot(air1[1])

    plt.subplot(4, 1, 3)
    plt.plot(air1[2])

    plt.show()

def convolve_traces(V3D):
    pass
