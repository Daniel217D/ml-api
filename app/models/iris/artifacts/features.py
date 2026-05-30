import pandas as pd

def make_areas(df):
    return pd.DataFrame({
        'sepal_area': df['sepal length (cm)'] * df['sepal width (cm)'],
        'petal_area': df['petal length (cm)'] * df['petal width (cm)'],
    })

def areas_feature_names_out(self, input_features):
    return ['sepal_area', 'petal_area']