from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,role,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(f"{input}\nResume:{pdf_content}\nRole: {role}\n'Job description':{prompt}")
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file) 
        data = ""
        for i in range(len(reader.pages)):
            data = data + " " + reader.pages[i].extract_text() 
        return data
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert 🔍")
st.header("📃 Advance ATS Tracking System 🔍")
input_text_role=st.text_input("Job Role: ",key="input_role")
input_text_desc=st.text_area("Job Description: ",key="input_ds")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


col1, col2, col3 = st.columns(3)

with col1:
    submit1 = st.button("Tell Me About the Resume")

with col2:
    submit2 = st.button("Percentage match")

with col3:
    submit3 = st.button("Suggest courses")


input_prompt1 = """
 You are an experienced Human Resource Manager with experties in hiring candidates from either Data Science,
 Full stack development, Data Analytics, Data Engineering or Big Data engineering.
 Your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2= """
 You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of either Data Science,
 Full stack development, Data Analytics, Data Engineering or Big Data engineering.
 You are an expert in all the ATS functionalities, 
 your task is to evaluate the resume against the provided job description. give me the percentage of match (ranging from 0 to 100) if the resume matches
 the job description. Give higher weightage for the job role given matches the experiance. First the output should come as percentage and then top 10 keywords missing and last final thoughts in bullet points.
"""

input_prompt3= """
 You have the knowledge of all the courses listed in top edtech platforms like coursera, udemy etc.
 Provide a list of recommended courses based on the weaknesses of the applicant in relation to the specified job requirements, presented in bullet points.
 These courses will enhance the candidate's abilities and significantly improve their chances of success in the role.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text_role,input_text_desc)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text_role,input_text_desc)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
        
elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text_role,input_text_desc)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")



   



