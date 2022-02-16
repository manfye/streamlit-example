import math
import pandas as pd
import streamlit as st
import datetime as datetime
from openpyxl import load_workbook

st.title("AeFI Daily File maker")
uploaded_file_1 = st.file_uploader("Excel File")
if uploaded_file_1 is not None:
    uploaded_file_2 = st.file_uploader("CSV File")
    if uploaded_file_2 is not None:
        x = datetime.datetime.now()
        df_dateVaccine = pd.read_csv(uploaded_file_2)
        xl = pd.ExcelFile(uploaded_file_1)
        xl.sheet_names
        try:
            df_dateVaccine["date"] = df_dateVaccine.apply(lambda x: datetime.datetime.strptime(x["date"], '%d/%m/%y'), axis=1)
        except:
            df_dateVaccine["date"] = df_dateVaccine.apply(lambda x: datetime.datetime.strptime(x["date"], '%d-%m-%y'), axis=1)

        df_aefi_raw_Comirnaty = pd.read_excel(xl, sheet_name=xl.sheet_names[0])

        df_aefi_raw_CoronaVac = pd.read_excel(xl, sheet_name=xl.sheet_names[1])
        df_aefi_raw_Az = pd.read_excel(xl, sheet_name=xl.sheet_names[2])
        df_aefi_raw_Cansino = pd.read_excel(xl, sheet_name=xl.sheet_names[3])
        df_aefi_raw_Covilo= pd.read_excel(xl, sheet_name=xl.sheet_names[4])
        df_aefi_raw_Comirnaty["date"] = df_aefi_raw_Comirnaty["date"].astype("datetime64[ns]")
        df_aefi_raw_CoronaVac["date"] = df_aefi_raw_CoronaVac["date"].astype("datetime64[ns]")
        df_aefi_raw_Az["date"] = df_aefi_raw_Az["date"].astype("datetime64[ns]")
        df_aefi_raw_Cansino["date"] = df_aefi_raw_Cansino["date"].astype("datetime64[ns]")
        df_aefi_raw_Covilo["date"] = df_aefi_raw_Covilo["date"].astype("datetime64[ns]")

        df_aefi_raw_all = df_aefi_raw_Comirnaty.append([df_aefi_raw_CoronaVac,df_aefi_raw_Az,df_aefi_raw_Cansino,df_aefi_raw_Covilo])
        # st.write(df_aefi_raw_all)
        df_aefi_raw_all["date"] = df_aefi_raw_all["date"].dt.strftime('%Y-%m-%d').astype('datetime64[ns]')


        df_dateVaccine['date1'] = df_dateVaccine['date'] -  pd.to_timedelta(1, unit='d')
        df_dateVaccine['date_original'] = df_dateVaccine['date']
        df_dateVaccine['date'] = df_dateVaccine['date1']



        df_merged_raw = df_dateVaccine.merge(df_aefi_raw_all, how="left", on = ["date","Vaccine"])
        df_merged_raw["date"]= pd.to_datetime(df_merged_raw.date)
        df_merged_raw = df_merged_raw.fillna(0)
        df_merged_raw["date"] = df_merged_raw["date"].dt.strftime('%Y-%m-%d').astype('datetime64[ns]')


        df_merged_raw["mysj_total"] = df_merged_raw["DOSE1_AEFI_REPORTED_YES"] + df_merged_raw["DOSE2_AEFI_REPORTED_YES"]


        df_merged_raw["non_serious_daily"] = df_merged_raw["R-Harian"] + df_merged_raw["mysj_total"]
        df_merged_raw["non_serious_NPRA_daily"] = df_merged_raw["R-Harian"]
        df_merged_raw["serious_daily"] = df_merged_raw["S-Harian"]
        df_merged_raw["total_daily"] = df_merged_raw["serious_daily"] + df_merged_raw["non_serious_daily"]


        df_merged_raw.columns

        final_csv = df_merged_raw.reindex(['date', 'Vaccine','non_serious_daily',"serious_daily","total_daily", 'non_serious_NPRA_daily',
                                        'DOSE1_AEFI_REPORTED_YES', 'DOSE1_INJECTION_SITE_PAIN_1',
                                        'DOSE1_INJECTION SITE SWELLING', 'DOSE1_INJECTION SITE REDNESS',
                                        'DOSE1_TIREDNESS', 'DOSE1_HEADACHE', 'DOSE1_MUSCLE_PAIN',
                                        'DOSE1_JOINT PAIN', 'DOSE1_BODY WEAKNESS', 'DOSE1_FEVER',
                                        'DOSE1_VOMITING', 'DOSE1_CHILLS', 'DOSE1_SKIN_RASH',
                                        'DOSE2_AEFI_REPORTED_YES', 'DOSE2_INJECTION_SITE_PAIN_1',
                                        'DOSE2_INJECTION SITE SWELLING', 'DOSE2_INJECTION SITE REDNESS',
                                        'DOSE2_TIREDNESS', 'DOSE2_HEADACHE', 'DOSE2_MUSCLE_PAIN',
                                        'DOSE2_JOINT PAIN', 'DOSE2_BODY WEAKNESS', 'DOSE2_FEVER',
                                        'DOSE2_VOMITING', 'DOSE2_CHILLS',"DOSE2_SKIN_RASH"], axis="columns")


        final_csv[['non_serious_daily',"serious_daily","total_daily",
                                        'DOSE1_AEFI_REPORTED_YES', 'DOSE1_INJECTION_SITE_PAIN_1',
                                        'DOSE1_INJECTION SITE SWELLING', 'DOSE1_INJECTION SITE REDNESS',
                                        'DOSE1_TIREDNESS', 'DOSE1_HEADACHE', 'DOSE1_MUSCLE_PAIN',
                                        'DOSE1_JOINT PAIN', 'DOSE1_BODY WEAKNESS', 'DOSE1_FEVER',
                                        'DOSE1_VOMITING', 'DOSE1_CHILLS', 'DOSE1_SKIN_RASH',
                                        'DOSE2_AEFI_REPORTED_YES', 'DOSE2_INJECTION_SITE_PAIN_1',
                                        'DOSE2_INJECTION SITE SWELLING', 'DOSE2_INJECTION SITE REDNESS',
                                        'DOSE2_TIREDNESS', 'DOSE2_HEADACHE', 'DOSE2_MUSCLE_PAIN',
                                        'DOSE2_JOINT PAIN', 'DOSE2_BODY WEAKNESS', 'DOSE2_FEVER',
                                        'DOSE2_VOMITING', 'DOSE2_CHILLS',"DOSE2_SKIN_RASH", 'non_serious_NPRA_daily']] = final_csv[['non_serious_daily',"serious_daily","total_daily",
                                        'DOSE1_AEFI_REPORTED_YES', 'DOSE1_INJECTION_SITE_PAIN_1',
                                        'DOSE1_INJECTION SITE SWELLING', 'DOSE1_INJECTION SITE REDNESS',
                                        'DOSE1_TIREDNESS', 'DOSE1_HEADACHE', 'DOSE1_MUSCLE_PAIN',
                                        'DOSE1_JOINT PAIN', 'DOSE1_BODY WEAKNESS', 'DOSE1_FEVER',
                                        'DOSE1_VOMITING', 'DOSE1_CHILLS', 'DOSE1_SKIN_RASH',
                                        'DOSE2_AEFI_REPORTED_YES', 'DOSE2_INJECTION_SITE_PAIN_1',
                                        'DOSE2_INJECTION SITE SWELLING', 'DOSE2_INJECTION SITE REDNESS',
                                        'DOSE2_TIREDNESS', 'DOSE2_HEADACHE', 'DOSE2_MUSCLE_PAIN',
                                        'DOSE2_JOINT PAIN', 'DOSE2_BODY WEAKNESS', 'DOSE2_FEVER',
                                        'DOSE2_VOMITING', 'DOSE2_CHILLS',"DOSE2_SKIN_RASH", 'non_serious_NPRA_daily']].astype(int)



        # final_csv.to_csv("generated/"+"aefi_overall_"+str(x.strftime("%Y-%m-%d"))+".csv", index= False)
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')


        csv = convert_df(final_csv)

        st.download_button(
        "Download AeFI Overall",
        csv,
        "aefi_overall_"+str(x.strftime("%Y-%m-%d"))+".csv",
        "text/csv",
        key='download-csv'
        )







st.markdown("""---""")


st.title("AeFI Serious File maker")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df_dateVaccine = pd.read_csv(uploaded_file)
    st.write(df_dateVaccine)
    #  df_dateVaccine = pd.read_csv("Aefi_serious.csv")
    x = datetime.datetime.now()
    try:
        df_dateVaccine["date"] = df_dateVaccine.apply(lambda x: datetime.datetime.strptime(x["date"], '%d-%m-%Y'), axis=1)
    except:
        df_dateVaccine["date"] = df_dateVaccine.apply(lambda x: datetime.datetime.strptime(x["date"], '%d/%m/%Y'), axis=1)
    # except:
    #   
    # df_dateVaccine.to_csv("generated/"+"aefi_serious_"+str(x.strftime("%Y-%m-%d"))+".csv", index= False)
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(df_dateVaccine)

    st.download_button(
    "Download AeFI Serious",
    csv,
    "aefi_serious_"+str(x.strftime("%Y-%m-%d"))+".csv",
    "text/csv",
    key='download-csv'
    )

