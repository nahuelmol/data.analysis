def Progresiva(lats, lons):
    import math
    x_ax = [0.0]
    y_ax = [0.0]
    aux_x = 0.0
    aux_y = 0.0
    i = 0
    for lat, lon in zip(lats, lons):
        if(i != 0):
            aux_x = abs(abs(lat) - abs(prev_lat))
            aux_y = abs(abs(lon) - abs(prev_lon))
            x_ax.append(aux_x)
            y_ax.append(aux_y)
        prev_lat = lat
        prev_lon = lon
        i += 1
    #convert to meters
    x_ax_m = []
    y_ax_m = []
    for x, y in zip(x_ax, y_ax):
        #xrads = math.radians(x)
        xm = x * 111.320
        x_ax_m.append(xm)
        xrads = math.radians(x)
        y_ax_m.append(111.32 * math.cos(xrads))

    distance = []
    for x, y in zip(x_ax_m, y_ax_m):
        d = math.sqrt(pow(x,2) + pow(y,2))
        distance.append(d)
    progresiva = [0.0]
    for i in range(len(distance)):
        if (i != 0):
            res = distance[i] + progresiva[-1]
            progresiva.append(res)
    return progresiva

def setType(data):
    current = ''
    if (data['lat'].dtype != 'float64'):
        current = data['lat'].dtype
    lats = []
    lons = []
    for col in data.columns:
        for idx, dat in data[col].items():
            data[col][idx] = float(dat)
    return data

def buildPlots(data):
    pass

def do2dGraph(data):
    lats = []
    lons = []

    data = setType(data)
    data['progresiva'] = Progresiva(data['lat'], data['lon'])
    buildPlot(data)

    return data
