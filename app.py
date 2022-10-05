####################################################### S T A R T  ####################################################
# Most important
import pandas as pd
import numpy as np
import pandas as pd 
# other
import os
import requests
import warnings
warnings.filterwarnings("ignore")
#!pip install bs4
from bs4 import BeautifulSoup
import time
import math
import re
# selenium 
import time
from PIL import Image
from selenium import webdriver
import selenium.webdriver.common.keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
##########################################################################################################
#############################################################################################################################
# enter job and get the url
def get_url(job):
    url= "https://wuzzuf.net/search/jobs/?q="+str(job)
    return url
#############################################################################################################################
# get the number of pages 
def get_pages_no(url):
    request = requests.get(url)
    data = request.text
    soup = BeautifulSoup(data)
    n = soup.find("li", {"class":"css-8neukt"}).text
    n = n.split(" ")
    number_of_pages = int(n[-1])/int(n[3])
    number_of_pages = math.ceil(number_of_pages)
    return number_of_pages
#############################################################################################################################
def all_scrap_function(job_name):
        titles = []
        Requirments = []
        Experince = []
        links = []
        Company_name = []
        country = []
        city = []
        address = []
        job_since = []
        company_link = []
        full_part = []

        base_url = get_url(job_name)
        pages = get_pages_no(base_url)
        for i in range(0,pages+1):
                url = base_url+"&start="+str(i)
                request = requests.get(url)
                data = request.text
                soup = BeautifulSoup(data)
                
                x = soup.findAll("h2",{"class":"css-m604qf"})
                for i in x:
                        titles.append(i.text.split("-")[0].strip())

                x = soup.findAll("div",{"class":"css-y4udm8"})
                for i in x:
                    Requirments.append(",".join(i.text.split("·")[2:]))
                
                x = soup.findAll("div",{"class":"css-y4udm8"})
                for i in x:
                    Experince.append(i.text.split("·")[1])

                x = soup.findAll("h2",{"class":"css-m604qf"})
                for i in x:
                    links.append(("https://wuzzuf.net"+i.find("a")["href"]))

                x = soup.findAll("div",{"class":"css-d7j1kk"})
                for i in x:
                    Company_name.append(i.find("a").text.replace("-","").strip())

                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    country.append(i.text.split(",")[-1])


                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    city.append(i.text.split(",")[-2])


                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    address.append(i.text.split(",")[0])


                x = soup.findAll("div",{"class":"css-4c4ojb"})
                x=x+soup.findAll("div",{"class":"css-do6t5g"})
                for i in x:            
                    job_since.append(i.text.split(",")[0])
                    
                x = soup.findAll("div",{"class":"css-d7j1kk"})
                for i in x:
                    if(i.find("a").text =="Confidential -" ):
                        company_link.append("Confidential")
                    else:
                        company_link.append(i.find("a")["href"])
                  
                
                x = soup.findAll("div",{"class":"css-1lh32fc"})
                for i in x:
                    full_part.append(i.text)
                    
                    
        
        JOB_DESCRIPTION = []
        JOB_REQUIRMENT = []
        jobs_skills =[]
        # Connection
        DRIVER_PATH = "chromedriver.exe"
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        # collecting data
        for i in links:
                jobaya_skils = []
                url = i
                driver.get(url)
                job_description_and_job_requirement = driver.find_elements(By.CLASS_NAME,"css-ghicub")
                if(len(job_description_and_job_requirement)>1):
                        JOB_DESCRIPTION.append(job_description_and_job_requirement[0].text)
                        JOB_REQUIRMENT.append(job_description_and_job_requirement[1].text)
                elif (len(job_description_and_job_requirement)==1):
                        JOB_DESCRIPTION.append(job_description_and_job_requirement[0].text)
                        JOB_REQUIRMENT.append("No")
                job_skills = driver.find_elements(By.CLASS_NAME,"css-158icaa")
        
                jobaya_skils = []
                for i in job_skills:

                    jobaya_skils.append(i.text)
                jobs_skills.append(jobaya_skils)
        
        length = len(company_link)
        company_logo = []
        for i in range(0,length):
            if(Company_name[i]=="Confidential"):
                company_logo.append("Confidential")
            else:
                url = company_link[i]
                request = requests.get(url)
                data = request.text
                soup = BeautifulSoup(data)
                company_logo.append(soup.find("img")["src"])
        
        # converting lists to a data frame 
        df = pd.DataFrame(titles,columns=["titles"])
        df["Requirments"] = Requirments
        df["Experince"] = Experince
        df["links"] = links
        df["Company_name"] = Company_name
        df["country"] = country
        df["city"] = city
        df["address"] = address
        df["job_since"] = job_since
        df["company_link"] = company_link
        df["full_part"] = full_part
        df["job_description"] = JOB_DESCRIPTION
        df["job_requirement"] = JOB_REQUIRMENT
        df["jobs_skills"] = jobs_skills
        df["company_logo"] = company_logo
        return df
#############################################################################################################################
def outer_scrap_function(job_name):
        titles = []
        Requirments = []
        Experince = []
        links = []
        Company_name = []
        country = []
        city = []
        address = []
        job_since = []
        company_link = []
        full_part = []

        base_url = get_url(job_name)
        pages = get_pages_no(base_url)
        for i in range(0,pages+1):
                url = base_url+"&start="+str(i)
                request = requests.get(url)
                data = request.text
                soup = BeautifulSoup(data)
                
                x = soup.findAll("h2",{"class":"css-m604qf"})
                for i in x:
                        titles.append(i.text.split("-")[0].strip())

                x = soup.findAll("div",{"class":"css-y4udm8"})
                for i in x:
                    Requirments.append(",".join(i.text.split("·")[2:]))
                
                x = soup.findAll("div",{"class":"css-y4udm8"})
                for i in x:
                    Experince.append(i.text.split("·")[1])

                x = soup.findAll("h2",{"class":"css-m604qf"})
                for i in x:
                    links.append(("https://wuzzuf.net"+i.find("a")["href"]))

                x = soup.findAll("div",{"class":"css-d7j1kk"})
                for i in x:
                    Company_name.append(i.find("a").text.replace("-","").strip())

                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    country.append(i.text.split(",")[-1])


                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    city.append(i.text.split(",")[-2])


                x = soup.findAll("span",{"class":"css-5wys0k"})
                for i in x:
                    address.append(i.text.split(",")[0])


                x = soup.findAll("div",{"class":"css-4c4ojb"})
                x=x+soup.findAll("div",{"class":"css-do6t5g"})
                for i in x:            
                    job_since.append(i.text.split(",")[0])
                    
                x = soup.findAll("div",{"class":"css-d7j1kk"})
                for i in x:
                    if(i.find("a").text =="Confidential -" ):
                        company_link.append("Confidential")
                    else:
                        company_link.append(i.find("a")["href"])
                  
                
                x = soup.findAll("div",{"class":"css-1lh32fc"})
                for i in x:
                    full_part.append(i.text)
                    
        df = pd.DataFrame(titles,columns=["titles"])
        df["Requirments"] = Requirments
        df["Experince"] = Experince
        df["links"] = links
        df["Company_name"] = Company_name
        df["country"] = country
        df["city"] = city
        df["address"] = address
        df["job_since"] = job_since
        df["company_link"] = company_link
        df["full_part"] = full_part
        return df


import streamlit as st
#st.image("Mostafa.jpg",width=200)
st.image("download.png",width=100)
header = '<p style="font-family:Courier; color:Blue; font-size: 45px;font-weight:bolder">scraping data from wuzzuf</p>'
st.markdown(header, unsafe_allow_html=True)

my_form=st.form(key='form-1')
title=my_form.text_input('Enter Job Title:')
way=my_form.radio('select a Way to scraping',('Fast','Slow'))
submitted=my_form.form_submit_button('Scrap Data to csv file')



try:
     if(title==""):
        if submitted:
           st.write("please enter the Job Title")
     else:
        if submitted:
            if(way=="Fast"):
                data = outer_scrap_function(title)
                file_name = title + ".csv"
                data.to_csv(file_name)
            elif(way=="Slow"):
                data = all_scrap_function(title)
                file_name = title + ".csv"
                data.to_csv(file_name)
            st.write("Csv successfully downloaded")    
except ValueError:
     print("Please wait 5 minutes and try again because too many requests!!! ")







