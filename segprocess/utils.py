
def ImageToBase64():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    image = base64.b64encode(buffer.read()).decode('utf-8')
    return image

def grapher(V3D):
    fig, ax1 = plt.subplots(ncols=1, figsize=(15, 8))
    V3D.data.transpose("ILINE_3D", "CROSSLINE_3D", "ShotPoint", "samples", transpose_coords=True
    ).sel(
        ILINE_3D=1290, CROSSLINE_3D=1150
    ).plot(yincrease=False, cmap="gray")

    plt.ylabel("TWT")
    plt.xlabel("XLINE")

    image = ImageToBase64(fig)
    return image

def graph_trace(V3D):
    image = V3D.isel(ILINE_3D=0, CROSSLINE_3D=0).data
    plt.figure(figsize=(15, 8))
    print("select image: ")
    input(imagen)
    trace = image[imagen]
    plt.subplot(4, 1, 1)
    plt.plot(trace)
    plt.subplot(4, 1, 2)
    plt.plot(trace)
    plt.subplot(4, 1, 3)
    plt.plot(trace)

    image = ImageToBase64(fig)
    return image

def convolve_traces(V3D, IL, XL):
    image = V3D.isel(ILINE_3D=IL, CROSSLINE_3D=XL).data
    convolved_signals = []
    for i in range(image):
        trace = image[i]
        convolved = np.convolve(trace)
        convolved_signals.append(convolved)

    return convolved_signals
