import streamlit as st
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
title = Image.open('title.png')
icon = Image.open('icon1.png')
layout = Image.open('HangarLayout.png')
st.set_page_config(page_title="Hangars", page_icon=icon, layout="wide", initial_sidebar_state="auto", menu_items=None)
title1, title2, title3 = st.columns(3)
title1.image(title, use_column_width='always')
st.title("JGG Hangar Dashboard")
st.image(layout)
#hangarColumns = ['Tenant', 'Tail Number', 'Type']
#indices = ['A', 'B', 'C', 'D', '1A', '2B', '3C', '4D', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '38', '39', '40', '41', '42', '43', '44', '45', '46', '46A', '47', '48', '49', '50', '51', '52', '53', '54', '55', '55A']
#hangarData = pd.DataFrame(columns=hangarColumns, index=indices)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=True, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def updateImage(xcor, ycor):
    edit = ImageDraw.Draw(layout)
    edit.text((xcor, ycor), "test", fill=(0, 0, 0))
    layout.save("HangarLayout.png")



col1, col2 = st.columns(2)
hangarData = pd.read_pickle('HangarData.pkl') 
form = col1.form("HangarEdit")
form.write("Use this form to update the tenant, tail number, and type of aircraft in each hangar. To clear a hangar, enter in the Hangar ID and leave the rest of the fields blank. Click the sidebar on the left for additional tools.")
hangarId = form.text_input("Enter the hangar code of the hangar you would like to modify:")
tenant = form.text_input("Enter the name of the new tenant:")
tail = form.text_input("Enter the tail number of the aircraft:")
type = form.text_input("Enter the type of aircraft:")
col2.write(hangarData)




if form.form_submit_button("Update Hangar info"):
    if hangarId in hangarData.index:
        st.success(f"Hangar {hangarId} Updated")
        hangarData.at[hangarId, 'Tenant'] = tenant
        hangarData.at[hangarId, 'Tail Number'] = tail
        hangarData.at[hangarId, 'Type'] = type
        hangarData.to_pickle('HangarData.pkl')
        col2.write(hangarData)
    else:
        st.error("Enter a valid Hangar ID")





with st.sidebar:
    st.subheader("Additional tools")
    df_xlsx = to_excel(hangarData)
    st.download_button(label='Download hangar data as Excel file', data=df_xlsx , file_name= 'HangarData.xlsx')
  