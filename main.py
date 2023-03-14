import requests
import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

from utils.mapper import map_residence_status, map_occupation, map_user_mb

with st.container():
    st.title('KewScore')

    left_column, right_column = st.columns(2)

    with left_column:
        with st.form("scoring_form"):
            name = st.text_input('Applicant Name', value='Roki Salim')
            application_id = st.text_input('Loan Application ID', value='APP126')
            residence_status = st.selectbox('Residence Status', ['OWNER', 'TENANT', 'SHARED', 'RENT'])
            occupation = st.selectbox('Occupation', ['PRIVATE SECTOR', 'GOVERMENT AGENCY', 'HEALTH SECTOR', 'ENTREPRENEUR', 'ENGINEERING', 'MILITARY'])
            is_user_mb = st.radio('Employment Status', ['EMPLOYEE', 'SELF-EMPLOYED'])
            os_dpk = st.number_input('Savings Amount (in IDR)', min_value=1000000, step=500000)
            nom_idr = st.number_input('Requested Loan Amount (in IDR)', min_value=1000000, step=500000)
            age = st.number_input('Age', min_value=21, max_value=80, step=1)

            submitted = st.form_submit_button("SCORE",
                                            type='primary',
                                            use_container_width=True)

    with right_column:
        if submitted:
            residence_status = map_residence_status(residence_status)
            occupation = map_occupation(occupation)
            is_user_mb = map_user_mb(is_user_mb)

            data = {
                "application_id": application_id, 
                "usia_tahun": age, 
                "jenis_pekerjaan": occupation, 
                "residence_status": residence_status, 
                "os_dpk": os_dpk,
                "nom_idr": nom_idr, 
                "punya_user_mb": is_user_mb, 
                "bag_prod_type": "KPR",
                "tenor": 120, 
                "min_tenor": 60, 
                "max_tenor": 300, 
                "min_nom_idr": 1000000, 
                "max_nom_idr": 10000000000, 
                "branch_name": "KCP MAGELANG", 
                "noa_dpk": 1, 
                "marital_status": "MARRIED",
                "name": name, 
                "nik": "159121234012001", 
                "slik_score": "B+", 
                "pefindo_score": "A-", 
                "telco_score": "A+", 
                "province_code": "JK",
                "income_grade": 5, 
                "income_range": "IDR 20Jt - 30Jt", 
                "phone_no_verif": True,
                "phone_id_verif": True, 
                "workplace_verif": True, 
                "neg_rec_verif": True, 
                "education": "S1/D4", 
                "industry": "FMCG", 
                "gender": "MALE"
            }
            

            payload = {
                "product_type": "general",
                "category": "bank",
                "input": {
                    "columns": list(data.keys()),
                    "data": [list(data.values())]
                }
            }

            json_payload = json.dumps(payload)

            result = requests.post('http://149.129.212.129:8080/predict', 
                                   data=json_payload,
                                   headers={'Content-Type': 'application/json'})

            #st.success('Scoring Result', icon="✅")

            result_json = result.json()
            if result_json['status'] != 200:
                st.error(result_json['message'], icon="🚨")
            elif result_json['status'] == 200:

                risk_score = result_json['message']['score'][0]
                risk_level = result_json['message']['risk_level'][0]
                is_approve = result_json['message']['approve'][0]
                kri_score = result_json['message']['kri'][0]

                if risk_level != 'high':
                    st.subheader(':large_orange_diamond: Recommendation')
                    st.header(':green[Approve] :white_check_mark:')

                    st.subheader(':large_orange_diamond: Credit Score')
                    st.metric(label="Credit Score", 
                            value=risk_score,
                            delta=f"-{risk_level} risk".upper(),
                            delta_color='inverse',
                            label_visibility='collapsed')
                else:
                    st.subheader(':large_orange_diamond: Recommendation')
                    st.header(':red[Reject] :x:')

                    st.subheader(':large_orange_diamond: Credit Score')
                    st.metric(label="Credit Score", 
                            value=risk_score,
                            delta=f"{risk_level} risk".upper(),
                            delta_color='inverse',
                            label_visibility='collapsed')
                    
                df = pd.DataFrame({'variable': list(kri_score.keys()),
                                'score': list(kri_score.values())})
                df['variable'] = df['variable'].map({'jenis_pekerjaan': 'Occupation', 
                                                    'residence_status': 'Residence Status', 
                                                    'os_dpk': 'Savings Amount',
                                                    'nom_idr': 'Requested Loan Amount',
                                                    'punya_user_mb': 'Employment Status'})
                
                df['color'] = df['score'].map({'poor': 'red', 'fair':'orange', 'good':'green'})
                df['level'] = df['score'].map({'poor': 1, 'fair':2, 'good':3})
                df.sort_values(by=['level'], ascending=True, inplace=True)
                
                fig, ax = plt.subplots(dpi=150, figsize=(3,4))
                ax.barh(y=df['variable'], width=df['level'], color=df['color'])
                plt.xticks([0,1,2,3], ['Score', 'Poor', 'Fair', 'Good'])
                ax.spines['top'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                st.pyplot(fig)
                st.dataframe(df.drop(['level', 'color'], axis=1).reset_index(drop=True), use_container_width=True)

