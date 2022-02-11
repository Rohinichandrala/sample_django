from django import forms


class AddForm(forms.Form):
    port_name = forms.CharField(max_length=100, label="Port Name", widget=forms.TextInput,
                                error_messages={
                                    "required": "Port name cannot be empty"
                                })
    temperature = forms.IntegerField(max_value=30, min_value=-30, widget=forms.TextInput, label="Temp",
                                     error_messages={
                                         "required": "Temperature should not be empty",
                                         "max_value": "Temperature should be less than 30",
                                         "min_value": "Temperature should be greater than -30",
                                     })
    latitude = forms.DecimalField(max_value=90, min_value=-90, widget=forms.TextInput, label="Latitude",
                                  error_messages={
                                      "required": "Temperature should not be empty",
                                      "max_value": "Latitude values should be less than 90",
                                      "min_value": "Latitude values should be greater than -90"

                                  })
    longitude = forms.DecimalField(max_value=180, min_value=-180, widget=forms.TextInput, label="Latitude",
                                   error_messages={
                                       "required": "Longitude values should be between -180 and 180",
                                       "max_value": "Longitude values should be less than 180",
                                       "min_value": "Longitude values should be greater than -180"
                                   })


class BatchImportPortForm(forms.Form):
    import_ports = forms.FileField(label="Upload csv file with ports information")
