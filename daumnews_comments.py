Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 22:39:24) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> #라이브러리 import
>>> from selenium import webdriver
>>> from selenium.webdriver.common.by import By
>>> from selenium.webdriver.common.keys import Keys
>>> import requests
>>> from bs4 import BeautifulSoup as bs
>>> import pandas as pd
>>> import time
>>> import csv
>>> 
>>> #'중국'으로 검색한 뉴스 목록
>>> url = 'https://search.daum.net/search?w=news&q=%EC%A4%91%EA%B5%AD&DA=23A&spacing=0'
>>> 
>>> #뉴스 제목 밑의 다음뉴스를 클릭해야 댓글 수집 가능, url = https://news.v.daum.net/v/숫자 형식
>>> web = requests.get(url).content
>>> source = bs(web, 'html.parser')
>>> urls_list = []
>>> 
>>> for urls in source.find_all('a', {'class' : "f_link_b"}):
	#기존 다음뉴스 url에서 숫자만 따오기 위해
	new_url_content = urls["href"][-21:-4]
	new_url = "https://news.v.daum.net/v/" + new_url_content
	urls_list.append(new_url)

	
>>> #본인의 크롬드라이버 저장경로
>>> driver = webdriver.Chrome(executable_path = r'C:\Users\변정민\Desktop\chromedriver.exe')
>>> #크롤링할 댓글 리스트
>>> comments_list = []
>>> #총 10개의 뉴스 댓글 수집
>>> for i in range(10):
	driver.get(urls_list[i])
	print(driver.current_url)
	#오류 발생 방지용 시간차
	time.sleep(3)
	try:
		#댓글의 더보기 버튼이 나타나지 않을때까지 클릭
		while driver.find_element_by_xpath('//*[@id="alex-area"]/div/div/div/div[3]/div[2]/a').text !='':
			driver.find_element_by_xpath('//*[@id="alex-area"]/div/div/div/div[3]/div[2]/a').click()
			time.sleep(3)
	except:
		pass
	time.sleep(2)
	#최대 40개 댓글 크롤링
	for k in range(40):
		try:
			#크롬 개발자도구 이용해 full Xpath 복사
			comments = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div[1]/div[2]/div[4]/div[2]/div/div/div/div[3]/ul[2]/li[' + str(k) + ']/div/p').text
			comments = comments.replace("\n", " ")
			comments_list.append(comments)
		#try 내부 실행문에서 오류 발생시 pass
		except:
			pass
	time.sleep(3)
>>> #크롤링 결과 csv파일로 제작
>>> cmts = pd.DataFrame(comments_list)
>>> cmts.head()
>>> cmts.to_csv('cmts_UTF8.csv', encoding='UTF-8')
