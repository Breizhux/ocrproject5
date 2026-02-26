#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import pandas as pd

def load_data():
    """Charge et fusionne les trois sources de données SIRH."""
    print("⏳ Chargement des données...")

    sirh = pd.read_csv(
        "https://s3.eu-west-1.amazonaws.com/course.oc-static.com/projects/1047_Data+Scientist+ML/P4_DSML_1047/extrait_sirh.csv"
    )
    eval_perf = pd.read_csv(
        "https://s3.eu-west-1.amazonaws.com/course.oc-static.com/projects/1047_Data+Scientist+ML/P4_DSML_1047/extrait_eval.csv"
    )
    sondage = pd.read_csv(
        "https://s3.eu-west-1.amazonaws.com/course.oc-static.com/projects/1047_Data+Scientist+ML/P4_DSML_1047/extrait_sondage.csv"
    )

    eval_perf['eval_number'] = eval_perf['eval_number'].str.replace('E_', '').astype(int)

    df = (sirh.merge(eval_perf, left_on='id_employee', right_on='eval_number')
           .merge(sondage, left_on='eval_number', right_on='code_sondage'))

    df = df.drop(columns=['eval_number', 'code_sondage'])

    if 'augementation_salaire_precedente' in df.columns:
        df['augementation_salaire_precedente'] = (
            df['augementation_salaire_precedente'].str.rstrip(' %').astype(float)
        )

    print(f"✅ Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    return df

if __name__ == "__main__":
    df = load_data()
    print(df.head())
