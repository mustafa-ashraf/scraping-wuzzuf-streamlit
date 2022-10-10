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

#/**************************************************************************************/
def cleaning(data):
        length = data["Experince"].count()
        for i in range(0,length):
            data["Experince"][i]= data["Experince"][i].strip()
            data["country"][i]= data["country"][i].strip()
            data["city"][i]= data["city"][i].strip()
            if(len(data["full_part"][i])<10):
                continue
            else:
                    data["full_part"][i]= data["full_part"][i].replace("Time","Time , ")
        return data
  
  
def draw_map(df):
        import sys, requests, urllib
        import pandas as pd
        from pathlib import Path
        from zipfile import ZipFile
        import plotly.express as px

        # fmt: off
        # download data set, world cities including GPS co-ordinates
        url = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.74.zip"

        f = Path.cwd().joinpath(f'{urllib.parse.urlparse(url).path.split("/")[-1]}.zip')
        if not f.exists():
            r = requests.get(url, stream=True, headers={"User-Agent": "XY"})
            with open(f, "wb") as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)

        zfile = ZipFile(f)
        dfs = {f.filename: pd.read_csv(zfile.open(f)) for f in zfile.infolist() if f.filename.split(".")[1]=="csv"}
        # fmt: on

        # just UK cities.. with GPS
        dfuk = dfs["worldcities.csv"].loc[lambda d: d["iso2"].eq("EG")]

        # dataframe referred to in question, cities listed multiple times
        n_cities = 20
        p = np.geomspace(0.1, 0.05, n_cities)
        p = p / p.sum()
        dflist = pd.DataFrame({"city": np.random.choice(dfuk.sample(n_cities)["city"],1000, p=p)})

        x = px.scatter_mapbox(
            df.groupby("city", as_index=False).size().merge(dfuk, on="city"),
            lat="lat",
            lon="lng",
            hover_name="city",
            size="size",
        ).update_layout(mapbox={"style": "open-street-map", "zoom": 6.9}, margin={"t":0,"b":0,"l":0,"r":0})
        return x
#/*************************************************************************************/

import streamlit as st
#st.image("Mostafa.jpg",width=200)
st.image("download.png",width=100)
header = '<p style="font-family:Courier; color:Blue; font-size: 45px;font-weight:bolder">scraping data from wuzzuf</p>'
st.markdown(header, unsafe_allow_html=True)

my_form=st.form(key='form-1')
title=my_form.text_input('Enter Job Title:')
way=my_form.radio('Way of collecting the data',('Fast : It collect some of job features not all','Slow : It collect all of job features'))
submitted=my_form.form_submit_button('Scrap Data to csv file')



try:
    if(title==""):
        if submitted:
           st.write("please enter the Job Title")
    else:
        if submitted:
            if(way=="Fast : It collect some of job features not all"):
                data = outer_scrap_function(title)
                data = cleaning(data)
                file_name = title + ".csv"
                data.to_csv(file_name)
            elif(way=="Slow : It collect all of job features"):
                data = all_scrap_function(title)
                data = cleaning(data)
                file_name = title + ".csv"
                data.to_csv(file_name)   
            st.write("CSV successfully created")
            st.write(data)
            import os
            dir_path = os.path.dirname(os.path.realpath(__file__)) +"\\"+file_name
            st.write("CSV file saved into this path :  "+dir_path)
            data = data[data["country"]=="Egypt"]
            header = '<p style="font-family:Courier; color:Blue; font-size: 45px;font-weight:bolder">Some statistics In Egypt</p>'
            st.markdown(header, unsafe_allow_html=True)
            st.write(draw_map(data))
            header = '<p style="font-family:Courier; color:White; font-size: 25px;font-weight:bolder">Top cities in this Job in Egypt</p>'
            st.markdown(header, unsafe_allow_html=True)
            x = data["city"].value_counts()[:6]
            st.bar_chart(x)
            header = '<p style="font-family:Courier; color:White; font-size: 25px;font-weight:bolder">Top companies in this Job in Egypt</p>'
            st.markdown(header, unsafe_allow_html=True)
            x = data["Company_name"].value_counts()[1:6]
            st.line_chart(x)
            
except:
     st.error("Please wait 2 minutes and try again because too many requests!!! ")
     st.stop()






