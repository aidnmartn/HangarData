from sys import addaudithook
import streamlit as st
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from datetime import datetime
title = Image.open('title.png')
icon = Image.open('icon1.png')
layout = Image.open('HangarLayout.png')
st.set_page_config(page_title="Hangars", page_icon=icon, layout="centered", initial_sidebar_state="expanded", menu_items=None)
title1, title2, title3 = st.columns(3)
title1.image(title, use_column_width='always')
st.title("JGG Hangar Dashboard")
#hangarColumns = ['Tenant', 'Tail Number', 'Type']
ids = ['A', 'B', 'C', '1A', '2B', '3C', '4D', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '38', '39', '40', '41', '42', '43', '44', '45', '46', '46A', '47', '48', '49', '50', '51', '52', '53', '54', '55', '55A']
#hangarData = pd.DataFrame(columns=hangarColumns, index=ids)

#coordColumns = ['x', 'y']
#coordIndices = ['A', 'B', 'C', 'D', '1A', '2B', '3C', '4D', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '38', '39', '40', '41', '42', '43', '44', '45', '46', '46A', '47', '48', '49', '50', '51', '52', '53', '54', '55', '55A']
#coords = pd.DataFrame(columns=coordColumns, index=coordIndices)
coords = pd.read_csv('coords.csv', index_col=0)
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


def updateImage(xy, data):
    temp=layout.copy()
    myFont = ImageFont.truetype('times new roman.ttf', 20)
    edit = ImageDraw.Draw(temp)
    for i in data.index:
        text = data.at[i,'Tenant'] + '\n' + data.at[i,'Tail Number'] + '\n' + data.at[i,'Type']
        edit.text((xy.at[i,'x'], xy.at[i,'y']), text, font=myFont, fill=(0, 0, 0))
    edit.text((1450, 650), "46A:", font=myFont, fill=(0, 0, 0))
    edit.text((100, 630), "55A:", font=myFont, fill=(0, 0, 0))
    temp.save("temp.png")
    filled = Image.open("temp.png")
    container.image(filled)

hangarData = pd.read_pickle('HangarData.pkl') 
container = st.container()

help = st.expander('Help')
form = st.form("HangarEdit")
help.write("Use this form to update the *tenant*, *tail number*, and *type of aircraft* in each hangar.")
help.write('**To clear a hangar**, enter in the Hangar ID, leave the rest of the fields blank, and click "Update Hangar Info"')
help.write("Click the sidebar on the left for additional tools.")
help.write("You can right-click on the hangar chart to save to your computer")
help.write("The data table at the bottom is interactive, for example: click the 'Tenant' column to sort alphabetically by tenant name")
help.write("*Note: Longer names may need to be abbreviated to fit*")
hangarId = form.selectbox("Choose the Hangar ID of the hangar you would like to modify:", ids)
tenant = form.text_input("Enter the last name of the new tenant:")
tail = form.text_input("Enter the tail number of the aircraft:")
type = form.text_input("Enter the type of aircraft:")
if form.form_submit_button("Update Hangar Info"):
    if hangarId in hangarData.index:

        st.success(f"Hangar {hangarId} Updated")
        hangarData.at[hangarId, 'Tenant'] = tenant
        hangarData.at[hangarId, 'Tail Number'] = tail
        hangarData.at[hangarId, 'Type'] = type
        hangarData.to_pickle('HangarData.pkl')
    else:
        st.error("Enter a valid Hangar ID")
    st.write(hangarData)
    updateImage(coords,hangarData)
else:
    st.write(hangarData)
    updateImage(coords,hangarData)



with st.sidebar:
    st.subheader("Additional tools")
    df_xlsx = to_excel(hangarData)
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H.%M.%S")
    st.download_button(label='Download hangar data as Excel file', data=df_xlsx , file_name= f'HangarData_{dt_string}.xlsx')
    clear = st.button("Clear All Data")
    if clear:
        hangarColumns = ['Tenant', 'Tail Number', 'Type']
        indices = ['A', 'B', 'C', '1A', '2B', '3C', '4D', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '38', '39', '40', '41', '42', '43', '44', '45', '46', '46A', '47', '48', '49', '50', '51', '52', '53', '54', '55', '55A']
        hangarData = pd.DataFrame(columns=hangarColumns, index=indices)
        hangarData = hangarData.fillna('')
        hangarData.to_pickle('HangarData.pkl')

#coords.to_csv('coords.csv')
