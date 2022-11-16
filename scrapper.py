from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from pytube import extract
import json, io
import argparse


def get_page(web):

    s=Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=s, chrome_options=options)

    # Creating the driver 
    driver.get(web)

    #tps pour charger la page : attendre les données
    time.sleep(2)
    # create bs object to parse HTML  
    soup = BeautifulSoup(driver.page_source, "html.parser")

    return(soup, driver)

def getTitle(soup):
    return(soup.find("meta", itemprop="name")["content"])

def getName(soup):
    return(soup.find("span", itemprop="author").next.next["content"])

def getLikes(soup):
    raw_like = soup.find("button", {"class": "yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start"})
    like = raw_like['aria-label']
    if like[0] == 'C':
        nb_like = like.split("Cliquez sur \"J'aime\" pour cette vidéo comme ")[1].split("autres internautes.")[0]
    else:
        nb_like = like.split("like this video along with ")[1].split("other people")[0]
    
    return(nb_like)

def getDescription(soup, driver):
    element = driver.find_element(By.XPATH, "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
    element.click()
    element = driver.find_element(By.XPATH, "//html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[3]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]")
    element.click()
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return(soup.find("yt-formatted-string", {"class": "style-scope ytd-text-inline-expander"}))


def getLinks(description):
    listLien = []
    liens = description.find_all("a")
    for lien in liens :
        if lien['href'][0] == "/":
            listLien.append("https://www.youtube.com"+lien['href'])
        else:
            listLien.append(lien['href'])
    return(listLien)

def getId(web):
    return(extract.video_id(web))

def getComments(soup, driver):
    N = 5
    commentaires = []
    element = driver.find_element(By.XPATH, "//*[@id=\"comments\"]")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = N)
    while commentsList == []:
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = N)
    for comment in commentsList:
        commentaires.append(comment.find("yt-formatted-string", {"id": "content-text"}).text)

    return(commentaires)

def getData(soup, driver, web):

    
    #titre 
    title= getTitle(soup)
    
    #auteur
    name = getName(soup)
    #print("Auteur de la vidéo :", auteur)

    #likes
    nb_like = getLikes(soup)

    #description
    description = getDescription(soup, driver)

    #liste des liens
    listLien = getLinks(description)   

    #id video
    id=getId(web)

    #commentaires
    commentaires = getComments(soup,driver)

    youtube_video_page = []
    youtube_video_page.append({
            "titre": title,
            "nom ": name,
            "likes": nb_like,
            "description": description.text,
            "liens " : listLien,
            "id ": id,
            "commentaires ": commentaires,
        })

    return(youtube_video_page)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input', action="store")
    parser.add_argument('--output', action="store")

    args = parser.parse_args()
    inp = args.input
    out = args.output


    url_tab = []
    f = open(inp)
    data = json.load(f)
    for i in data["videos_id"]:
        url_tab.append('https://www.youtube.com/watch?v='+i)
    f.close()

    data= []
    for url in url_tab:
        result1, result2 = get_page(url)

        youtube_video_page = getData(result1, result2, url)

        data.append(youtube_video_page)

    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    main()