import math
import pandas as pd
import streamlit as st
import datetime as datetime

st.write(datetime.datetime.strptime("2013-1-25", '%Y-%m-%d'))

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:


    # Can be used wherever a "file-like" object is accepted:
    df_dateVaccine = pd.read_csv(uploaded_file)
    st.write(df_dateVaccine)
    #  df_dateVaccine = pd.read_csv("Aefi_serious.csv")
    x = datetime.datetime.now()
    df_dateVaccine["date"] = df_dateVaccine.apply(lambda x: datetime.datetime.strptime(x["date"], '%d/%m/%Y'), axis=1)
    # except:
    #     df_dateVaccine["date"] = df_dateVaccine.apply(lambda x: datetime.datetime.strptime(x["date"], '%d-%m-%y'), axis=1)

    # df_dateVaccine.to_csv("generated/"+"aefi_serious_"+str(x.strftime("%Y-%m-%d"))+".csv", index= False)
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(df_dateVaccine)

    st.download_button(
    "Press to Download",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
    )