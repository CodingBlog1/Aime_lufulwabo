import re
from pdf2image import convert_from_path
import pandas as pd
from pytesseract import image_to_string
import time
from api import data_str
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


data_list = data_str.split("\n")
data_dict = {key: key for key in data_list}


def identify_icd10(text):
            icd10_codes = []
            for medical_term in data_dict:
                pattern = re.compile(medical_term)
                if pattern.search(text):
                    icd10_codes.append(data_dict[medical_term])

            return icd10_codes



pdf_file = 'alexia -ecw note scanned pdf.pdf'

new_df = pd.DataFrame([],columns=["ICD10","ICD10 Label","CC","HCC Label"])

df = pd.read_excel("Revised-V07-ICD-10-Crosswalk-for-HHS-HCC-Risk-Adjustment-Model.xlsx",header=[3],sheet_name="Table 3 ICD10 Crosswalk")
df_sheet2 = pd.read_excel("Revised-V07-ICD-10-Crosswalk-for-HHS-HCC-Risk-Adjustment-Model.xlsx",header=[2],sheet_name="Table 4 V07 Hierarchies")

images = convert_from_path(pdf_file,poppler_path=r'C:\\Users\\s\\Downloads\\poppler-22.12.0\\Library\\bin')
print(pdf_file)
final_text = ""
index_val=0


for pg, img in enumerate(images):
    st = time.time()
    final_text += image_to_string(img)
    final_text = final_text.replace(".",'')
    en = time.time()

    print(f"total time{pg}",en-st)
    with open("text_output.txt","a")as f:
        f.write(final_text)

    results = identify_icd10(final_text)
    print(results)
    
    for i in results:
        
            print(df["CC"][df["ICD10"]==i].values)
            new_df.loc[index_val]=[df['ICD10'][df["ICD10"]==i].values[0],df['ICD10 Label'][df["ICD10"]==i].values[0], df["CC"][df["ICD10"]==i].values[0],df_sheet2["HCC Label"][df["CC"][df["ICD10"]==i].values[0]==df_sheet2["V07 HCC"]].values[0]]
            index_val+=1
    final_text=""           

filename=pdf_file.split(".")[0]            
new_df.to_excel(f"output_{filename}.xlsx",index=False,header=True)
        

