from django import forms

PVMODELS= [('open_rack_cell_glassback', 'open_rack_cell_glassback'),
           ('roof_mount_cell_glassback', 'roof_mount_cell_glassback'),
           ('open_rack_cell_polymerback', 'open_rack_cell_polymerback'),
           ('insulated_back_polymerback', 'insulated_back_polymerback'),
           ('open_rack_polymer_thinfilm_steel', 'open_rack_polymer_thinfilm_steel'),
           ('22x_concentrator_tracker', '22x_concentrator_tracker')]


class QueryForm(forms.Form):

    PVmodel = forms.ChoiceField(choices=PVMODELS,
                                required=True,
                                label="PV_Model")