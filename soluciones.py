import pandas as pd
import requests
from typing import Set

def ej_1_cargar_datos_demograficos() -> pd.DataFrame:
    url = "https://public.opendatasoft.com/explore/dataset/us-cities-demographics/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B"
    df = pd.read_csv(url, sep=';')
    return df

def ej_2_cargar_calidad_aire(ciudades: Set[str]) -> pd.DataFrame:
    api_url = 'https://api-ninjas.com/api/airquality'
    datos = []
    for ciudad in ciudades:
        response = requests.get(api_url, headers={'X-Api-Key': 'fW5jff7UEUV6t17lAh7Nlg==RZidVHOwCEGUrIwb'}, params={'city': ciudad})
        if response.status_code == 200 and response.text.strip():
            try:
                data = response.json()
                for entry in data:
                    datos.append({
                        'Ciudad': ciudad,
                        'Fecha': entry['date'],
                        'Concentracion': entry['concentration']
                    })
            except ValueError:
                print(f'No se pudo decodificar la respuesta de la API para la ciudad {ciudad}')
    df = pd.DataFrame(datos)
    return df

df_demograficos = ej_1_cargar_datos_demograficos()
df_demograficos.drop(columns=['Race', 'Count', 'Number of Veterans'], inplace=True)
df_demograficos.drop_duplicates(inplace=True)

ciudades = set(df_demograficos['City'])
df_calidad_aire = ej_2_cargar_calidad_aire(ciudades)


