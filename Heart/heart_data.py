import pandas as pd

translation = {
    'age' : 'age',
    'anaemia' : 'anémie',
    'creatinine_phosphokinase' : 'créatine kinase',
    'diabetes' : 'diabète',
    'ejection_fraction' : "fraction d'éjection",
    'high_blood_pressure' : 'hypertension',
    'platelets' : 'plaquettes',
    'serum_creatinine' : 'creatinine',
    'serum_sodium' : 'sodium',
    'sex' : 'sexe',
    'smoking' : 'fumeur',
    'time' : 'temps',
    'DEATH_EVENT' : 'mort'
}

def import_heart_data(x_and_y = False, translate = False, include_time=True):
    '''Loads the data from the accompanying .csv file.

    Parameters
    ----------
    x_and_y (bool): separate features from the labels. In this case a tuple is returned.
    translate (bool): (mutually exclusive with x_and_y) : translate the columns in french.
        This option is only used for the plotting.
    include_time (bool): whether to include the time column.'''
    data = pd.read_csv("heart_failure_clinical_records_dataset.csv")
    if not include_time:
        data = data.drop(columns='time')
    if x_and_y:
        X, y = data.drop(columns='DEATH_EVENT'), data["DEATH_EVENT"]
        data = (X, y)
    elif translate:
        from heart import Translate
        data = Translate(translation).fit_transform(data)
    return data

