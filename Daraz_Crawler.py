#importing the relevent libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from dataformatter import price_convert,rating_convert,rating_retriever
import os
import tkinter as tk
import time
products=[]
prices=[]
ratings=[]
#intializing the driver
driver=webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
#opening the website and starting to crawl it..:)
keyword=input('Enter the  keyword that you want data of:')
i=int(input('Enter the number of pages that you want to crawl(max 10 at a time to avoid errors):'))
for j in range(1,i+1):
    try:
        driver.get(f'https://www.daraz.pk/catalog/?_keyori=ss&from=input&page={j}&q={keyword}&spm=a2a0e.home.search.go.35e34937Z50KTf')
    except:
        pass
    #getting the html code of the page
    content=driver.page_source
    soup=BeautifulSoup(content)
    for a in soup.findAll(attrs={'class':"gridItem--Yd0sa"}):
        name=a.find('div',attrs={'class':"title--wFj93"})
        price=a.find('span',attrs={'class':'currency--GVKjl'})
        rating=a.find('span',attrs={'class':'rating__review--ygkUy'})
        products.append(name.text)
        prices.append(price.text)
        ratings.append(rating)
#Insuring that no duplicates are present in the list
products=list(set(products))
ratings=rating_retriever(ratings)
ratings=list(map(rating_convert,ratings))
prices=list(map(price_convert,prices))
#Creating a check so that no errors occur while creating the dataframe
if len(products)==len(prices)==len(ratings):
    df=pd.DataFrame({'Product':products,'Price':prices,'Rating':ratings})
    print(df.head())
else:
    k=min(len(products),len(prices),len(ratings))
    df=pd.DataFrame({'Product':products[:k],'Price':prices[:k],'Rating':ratings[:k]})
    print(df.head())
#Saving the dataframe to a csv file
name_csv=input('Enter the name of the csv file:')
directory=os.getcwd()
print('Your current working directory is ',directory)
bol=input('Do you want to save the file in the current working directory?(y/n)')
if bol=='y':
    df.to_csv(f'{name_csv}.csv')
else:
    directory=tk.filedialog.askdirectory()
    df.to_csv(f'{directory}/{name_csv}.csv')
    print('Your file has been saved in ',directory)
#Closing the driver
driver.close()
driver.quit()
print('The program has finished running')
time.sleep(5)
#End of the program.



