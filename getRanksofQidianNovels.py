import requests
from bs4 import BeautifulSoup
import re

def getHtmlText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getRankList(html, Num):
    RankList = []
    bsObj = BeautifulSoup(html, "html.parser")
    Rank = bsObj.find("div", {"class":"rank-wrap box-center mb20"})
    DayRank = Rank.find("div", {"data-l2":Num})
    DayRankList = DayRank.find("ul")
    TheFirst = DayRankList.find("h4").get_text()
    RankList.append(TheFirst)
    NextList = DayRankList.findAll("a", {"class":"name"})
    for l in NextList:
        RankList.append(l.get_text())
    return RankList

def printSpace(n):
    for i in range(n):
        print("")

def findRankList(Num, html):
    KindofRand = {"1":"-------原创风云榜·新书---------", "2":"---------24小时热销榜----------", "3":"-------新锐会员周点击榜--------", "4":"-----------周推荐榜-----------", "5":"---------签约作家新书榜--------"}
    Title = KindofRand[Num]
    printSpace(2)
    print (Title)
    RankList = getRankList(html, Num)
    i = 0
    for l in RankList:
        i += 1
        print (str(i) + " " + l)

def getMainInfo(RankNum, BookNum, html):
    ATags = []
    bsObj = BeautifulSoup(html, "html.parser")
    Rank = bsObj.find("div", {"class":"rank-wrap box-center mb20"})
    AimRank = Rank.find("div", {"data-l2":RankNum})
    AimRankList = AimRank.find("ul")
    TheFirst = AimRankList.find("h4").a
    BookHref = TheFirst["href"]
    pat = re.compile(r"\d{10}")
    BookCode = pat.search(BookHref).group(0)
    ATags.append(BookCode)
    NextList = AimRankList.findAll("a", {"class":"name"})
    for l in NextList:
        BookHref = l["href"]
        BookCode = pat.search(BookHref).group(0)
        ATags.append(BookCode)
    InfoHref = "https://book.qidian.com/info/" + ATags.pop(BookNum - 1)
    MainInfoHtml = getHtmlText(InfoHref)
    MainInfoSoup = BeautifulSoup(MainInfoHtml, "html.parser")
    BookName = MainInfoSoup.find("h1").get_text()
    MainIntro = MainInfoSoup.find("p", class_="intro").get_text()
    MainInfo = MainInfoSoup.find("div", {"class":"book-intro"}).find("p").get_text("\n", "<br>")
    BookIntro = BookName + "\n ===================== \n" + MainIntro + "\n\n" + MainInfo
    return BookIntro

def gettheRank(html):
    i = 1
    while (i <= 1):
        i += 1
        print ("请输入查询的排行类型：")
        print ("1、原创风云榜·新书")
        print ("2、24小时热销榜")
        print ("3、新锐会员周点击榜")
        print ("4、周推荐榜")
        print ("5、签约作家新书榜")
        print ("0、结束查询")
        NumofRank = input()
        if (NumofRank == "0"):
            print ("ByeBye!")
            continue
        else:
            i -= 1
        findRankList(NumofRank, html)
        n = 1
        while (n <= 1):
            n += 1
            printSpace(2)
            print ("输入小说序号获取作品信息，输入0返回")
            Numofbook = input()
            if (Numofbook == "0"):
                continue
            else:
                n -= 1
            InfoofBook = getMainInfo(NumofRank, int(Numofbook), html)
            printSpace(1)
            print (InfoofBook)
        printSpace(3)

def main():
    url = "https://www.qidian.com"
    html = getHtmlText(url)
    gettheRank(html)

if __name__ == "__main__":
    main()
