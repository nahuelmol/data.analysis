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

def buildPlot(data, namefile):
    import matplotlib.pyplot as plt
    data['temperature']
    data['progresiva']
    plt.plot(data['progresiva'], data['temperature'], 
             marker='o',
             color='blue')
    plt.xlabel('Locations (m)')
    plt.ylabel('Temperature (C°)')
    plt.title('Temperature vs Distance')
    plt.grid(True)
    plt.savefig(namefile, dpi=300)

def fileexists(filename):
    import os
    if os.path.exists(filename):
        return True
    else:
        return False

def imageConverter(filename):
    filename = filename + '.png'
    try:
        with open(filename, 'r') as f:
            encoded_str = base64.b64encode(filename.read()).decode('utf-8')
            return True, encode_str
    except:
        return False, None


def do2dGraph(data):
    import json
    data = setType(data)
    DICT = {
            "name":"",
            "image_base64":"",
            "message": ""
    }
    data['progresiva'] = Progresiva(data['lat'], data['lon'])
    filename = 'tvd.png'
    buildPlot(data, filename)
    if not fileexists(filename):
        message = 'plot file cannot be created'
    else:
        print('plot file was created: ', filename, '.png')
        #convert to binary
        #send json with binary injected
        res, str_png = imageConverter(filename)
        if res:
            DICT['imagen_base64'] = str_png
            DICT['name'] = filename
            DICT['message'] = "file converted successfully"
        else:
            DICT['imagen_base64'] = None
            DICT['name'] = filename
            DICT['message'] = "file cannot be converted"
    json_str = json.dumps(DICT)   
    return data, json_str

