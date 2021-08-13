import argparse
from bs4 import BeautifulSoup
import requests
import io

parser = argparse.ArgumentParser(description='Links to scrap mcq\'s')
parser.add_argument('--link', dest='firstLink', type=str)

linkList = []
links = parser.parse_args()

filename = ''


def linksGatherrer(link):
    response = requests.get(link)

    if (response.status_code == 200):
        rawHtml = response.content
        soupObtained = BeautifulSoup(rawHtml, features='html.parser')

        for title in soupObtained.findAll('h1', class_='entry-title'):
            global filename

            filename = title.text

        specificSoup = soupObtained.find('div', class_='inside-article')

        allAnchors = specificSoup.find_all('a', href=True)

        for anchor in allAnchors:
            if anchor['href'][0] != '#':
                linkList.append(anchor['href'])


def mcqGatherrer(link):
    response = requests.get(link)

    if (response.status_code == 200):
        rawHtml = response.content
        soupObtained = BeautifulSoup(rawHtml, features='html.parser')

        soupObtained.encode("utf-8")

        specificSoup = soupObtained.find('div', class_='entry-content')

        title = ''
        for title in soupObtained.findAll('h1', class_='entry-title'):
            title = title.text

        specificParagraph = specificSoup.find_all("p")

        for spanTag in specificParagraph[1].findAll('span', class_='collapseomatic'):
            spanTag.decompose()

        for mobileAdsTag in specificParagraph[1].findAll('div', class_='sf-mobile-ads'):
            mobileAdsTag.decompose()

        for desktopAdsTag in specificParagraph[1].findAll('div', class_='sf-desktop-ads'):
            desktopAdsTag.decompose()

        for mobileContentPara in specificParagraph[1].findAll('div', class_='mobile-content'):
            mobileContentPara.decompose()

        for desktopContentPara in specificParagraph[1].findAll('div', class_='desktop-content'):
            desktopContentPara.decompose()

        for socialMedia in specificParagraph[1].findAll('div', class_='sf-nav-bottom'):
            socialMedia.decompose()

        with io.open(filename + ".txt", "a", encoding="utf-8", errors='ignore') as txtFile:
            txtFile.writelines(
                title + '\n\n-----------------------------------------------------------------------------------------------------------------\n\n')
            txtFile.writelines(specificParagraph[1].text)

        with io.open(filename + ".txt", "r", encoding="utf-8", errors='ignore') as f1:
            lines = f1.readlines()

        with io.open(filename + ".txt", "w", encoding="utf-8", errors='ignore') as f2:
            f2.writelines(lines[:-7])
            f2.writelines(
                '\n\n\n-----------------------------------------------------------------------------------------------------------------\n\n\n')


def masterGatherrer(linkList):
    for i in range(len(linkList)):
        mcqGatherrer(linkList[i])


if __name__ == '__main__':
    linksGatherrer(links.firstLink)
    masterGatherrer(linkList)