from django.shortcuts import render
from .forms import QueryForm
from chart.models import Data
import pandas as pd
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import Http404, HttpResponseNotFound
from django.views.generic import View

tempdata = Data.objects.values('temperature_surface')
ghidata = Data.objects.values('ghi')
timedata = Data.objects.values('time')
winddata = Data.objects.values('wind_speed')

temp_air = []
for key in tempdata:
    temp_air.append(key['temperature_surface'])

poa_global = []
for key in ghidata:
    poa_global.append(key['ghi'])

wind_speed = []
for key in winddata:
    wind_speed.append(key['wind_speed'])

time_list = []
for key in timedata:
    time_list.append(key['time'])


def home(request):
    if request.method == 'POST':
        query_form = QueryForm(request.POST)

        if query_form.is_valid():
            clean_query = query_form.cleaned_data

            pvmodel = clean_query['PVmodel']

            SF = 1
            Eo = 1000
            Epoa = poa_global
            g_poa_effective_list = [x / Eo for x in Epoa]
            g_poa_effective = g_poa_effective_list * SF

            celltemp = sapm_celltemp(poa_global, wind_speed, temp_air, pvmodel)


            global dcp
            dcp = pvwatts_dc(g_poa_effective, celltemp['temp_cell'], pdc0=1100, gamma_pdc=-.005, temp_ref=25)

            return render(request, 'results.html', {'PVmodel': pvmodel, 'DC Power': dcp})

        else:
            raise Http404


    else:
        query_form = QueryForm()
        return render(request, 'home.html', {'query_form': query_form})


def results(request):
    return render(request, 'results.html')


class PVPowerData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        home(request)
        pvdata = dcp
        pvlist = []
        for key in pvdata:
            pvlist.append(key)

        timedata = Data.objects.values('time')
        time_list = []
        for key in timedata:
            time_list.append(key['time'])

        data2 = {

            'Time': timedata,
            'PVData': pvlist,
        }

        return Response(data2)


def sapm_celltemp(poa_global, wind_speed, temp_air,
                  model):
    temp_models = {'open_rack_cell_glassback': [-3.47, -.0594, 3],
                   'roof_mount_cell_glassback': [-2.98, -.0471, 1],
                   'open_rack_cell_polymerback': [-3.56, -.0750, 3],
                   'insulated_back_polymerback': [-2.81, -.0455, 0],
                   'open_rack_polymer_thinfilm_steel': [-3.58, -.113, 3],
                   '22x_concentrator_tracker': [-3.23, -.130, 13]
                   }

    if isinstance(model, str):
        model = temp_models[model.lower()]
    elif isinstance(model, list):
        model = model
    elif isinstance(model, (dict, pd.Series)):
        model = [model['a'], model['b'], model['deltaT']]

    a = model[0]
    b = model[1]
    deltaT = model[2]

    Eo = 1000  # Reference irradiance

    g_poa_effective_list = [x / Eo for x in poa_global]
    expo = [a + b * y for y in wind_speed]

    temp_module = list(pd.Series(poa_global * np.exp(expo) + temp_air))

    temp_cell = temp_module + g_poa_effective_list * deltaT

    # return pd.DataFrame({'temp_cell': temp_cell, 'temp_module': temp_module})
    tempcm = {'temp_cell': temp_cell, 'temp_module': temp_module}

    return tempcm


def pvwatts_dc(g_poa_effective, temp_cell, pdc0, gamma_pdc, temp_ref=25):
    dc_poa = [0.001 * pdc0 * z for z in g_poa_effective]
    tempnorm = []
    for x in temp_cell:
        tempnorm.append((1 + gamma_pdc) * (x - temp_ref))
    # pdc = (g_poa_effective * 0.001 * pdc0 *
    #        (1 + gamma_pdc * (temp_cell - temp_ref)))
    pdc = [a * b for a, b in zip(dc_poa, tempnorm)]

    return pdc
