import pandas as pd
import numpy as np
from bs4 import BeautifulSoup 
from urllib.request import urlopen
import os 
import requests
import random
import time
def scrape_post(soup):
    #for post in soup.find_all('div', {'class': 'info'}):
    for post in soup.find_all('div', {'class': 'article seo'}):
        for post_info in post.find_all('a', {'class':'like'}):
            #post_url.append(post_id)
            #post_like.append(post_info.text)
            post_like = post_info.text 
        for post_info in post.find_all('a', {'class':'comment'}):
            #post_comment.append(post_info.text)
            post_comment = post_info.text
        for post_info in post.find_all('p', {'id':'contentArea'}):
            #post_text.append(post_info.text)
            post_text = post_info.text 
        for post_info in post.find_all('h1', {'class':'word-break'}):
            #post_title.append(post_info.text)
            post_title = post_info.text
        for post_info in post.find_all('div', {'class': 'tit_info'}):
            #post_timestamp.append(post_info.span['title'])
            post_timestamp = post_info.span['title']
        for post_info in post.find_all('strong', {'class': 'user'}):
            #post_user.append(post_info.text)
            post_user = post_info.text
        for post_info in post.find_all('p', {'class': 'writer'}): 
            spans = post_info.find_all('span')
            try: 
                #post_firm.append(spans[0].a['href'])
                post_firm = spans[0].a['href']
            except:
                print('NO firm PARSE')
                #print('NO firm info PARSE:'+post_id)
                #post_firm.append(np.NaN)
                post_firm = np.NaN
            try:
                #post_position.append(spans[2].text)
                post_position = spans[2].text
            except:
                #print('NO position PARSE:'+post_id)
                #print('NO position PARSE')
                #post_position.append(np.NaN)
                post_position = np.NaN
    original_post = pd.DataFrame(np.column_stack([post_title, post_user, post_firm, post_position, post_text, post_like, post_comment, post_timestamp]), columns = ['post_title', 'post_user', 'post_firm', 'post_position', 'post_text', 'post_like', 'post_comment', 'post_timestamp']) 
    return original_post
    #return post_title, post_user, post_firm, post_position, post_text, post_like, post_comment, post_timestamp
# needs changes 
def scrape_comments(soup):
    #follow_post = pd.DataFrame()
    #column_names = ['comment_date', 'comment_text', 'comment_like', 'comment_user', 'comment_firm', 'comment_position']
    #follow_post = pd.DataFrame(columns = column_names)
    comment_date = []
    comment_like = []
    comment_text = []
    comment_user = []
    comment_position = []
    comment_firm = []
    for comments in soup.find_all('div', {'class': 'content'}):
        for subcomments in comments.find_all('div', {'class': 'writer'}):
            for subcomment in subcomments.find_all('div', {'class': 'pop_profile'}):
                for comment_info in subcomment.find_all('strong', {'class': 'user'}):
                    comment_user.append(comment_info.text)
                    #comment_user = comment_info.text
                    #comment_url.append(post_id)
                    spans = subcomment.find_all('span')
                    try:
                        comment_position.append(spans[2].text)
                        #comment_position = spans[2].text
                    except:
                        #print('No position PARSE')
                        #follow_post['comment_position'].append(np.NaN)
                        comment_position.append(np.NaN)
            for comment_info in subcomment.find_all('span', {'class': 'name'}):
                try:
                    #follow_post['comment_firm'].append(comment_info.a['href'])
                    comment_firm.append(comment_info.a['href'])
                except:
                    #print('No firm PARSE')
                    #follow_post['comment_firm'].append(np.NaN)
                    comment_firm.append(np.NaN)
            for subcomments in comments.find_all('div', {'class':'detail'}):
                for subcomment in subcomments.find_all('span'):
                    comment_text.append(subcomment.text)
                    #comment_text = subcomment.text
            for subcomments in comments.find_all('div', {'class': 'info'}):
                for subcomment in subcomments.find_all('span', {'class': 'date'}):
                    comment_date.append(subcomment.text)
                    #comment_date = subcomment.text
                for subcomment in subcomments.find_all('a', {'class': 'like'}):
                    comment_like.append(subcomment.text)
                    #comment_like = subcomment.text

                    #follow_post['comment_like'].append(subcomment.text)
        #for subcomment in subcomments.find_all('a', {'class': 'comment'}):
        #    comment_comment.append(subcomment.text)    
        follow_post = pd.DataFrame(np.column_stack([comment_date, comment_text, comment_like, comment_user, comment_firm, comment_position]), columns = ['comment_date', 'comment_text', 'comment_like', 'comment_user', 'comment_firm', 'comment_position'])
        #comment = pd.DataFrame([comment_date, comment_text, comment_like, comment_user, comment_firm, comment_position])
        #follow_post.append(comment)
    return follow_post
    

#def read_company():
#    with open('company_list.txt', 'r') as f:
#        company_list = [line.rstrip() for line in f]
#    return company_list 

def extract_post(company_name):
    #Pick a random user agent
    #user_agent = random.choice(user_agent_list)
    #Set the headers 
    #headers = {'User-Agent': user_agent}
    #headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    # resp = requests.get(url,headers = headers)
    # use header to avoid blocked 
    url = 'https://www.teamblind.com/company/' + company_name + '/posts?page='
    post_by_firm = []
    post_by_firm_hottopic = []
    final_post = []
    i = 1
    num_invalid = 0
    while num_invalid <=2: #greey all historical posts
    #while i < 10: # define how many pages of posts to scrape
        #with urlopen(url + str(i)) as response:
        try: 
            user_agent = random.choice(user_agent_list)
            headers = {'User-Agent': user_agent}
            delays = [7, 4, 3, 2, 1, 0.5]
            delay = np.random.choice(delays)
            time.sleep(delay)
    #        #time.sleep(5) 
            response = requests.get(url+str(i), headers = headers) #as response:  
            print('processing:' + url+str(i)+'.')
            soup = BeautifulSoup(response.text, 'html.parser') # use text if requests
            for post in soup.find_all('a', href = True):
                if post['href'].startswith('/company/' + company_name + '/posts'):
                    post_by_firm_hottopic.append(post['href']) # hot topics for each firm
                if post['href'].startswith('/post'):
                    post_by_firm.append(post['href']) # posts by firms
                    final_post = set(post_by_firm)
        except Exception: 
            continue 
        i +=1
        if len(soup.find_all('div', {'class': 'none'}))==1:
            num_invalid +=1
            print('no contents to show for \n' + url + str(i))
            continue 
            #break # end the loop if no more posts to show
    #post_by_firm_list = list(dict.fromkeys(post_by_firm)) # remove duplicate posts 
    return final_post

def scrape_firm_post(company_name):
    column_names = ['post_title', 'post_user', 'post_firm', 'post_position', 'post_text', 'post_like', 'post_comment', 'post_timestamp']
    df = pd.DataFrame(columns = column_names)
    domurl = 'https://www.teamblind.com'
    exception_post = []
    for post_id in extract_post(company_name):
        url = u''.join((domurl,post_id))
        print('scraping ...' + url)
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        time.sleep(2)
        try:
            #delays = [7, 4, 6, 1, 10, 9]
            #delay = np.random.choice(delays)
            #time.sleep(delay)
            #req = requests.get(url, headers = headers) #as response:  
            #with urlopen(url, headers = headers) as response:
            response = requests.get(url, headers = headers) #as response:  
            bs = BeautifulSoup(response.text, 'html.parser')
            post = scrape_post(bs)
            post = post.assign(post_url = post_id)
            df = df.append(post)
            df['company'] = company_name # easier merge
            #with urlopen(url) as response:
            #    bs = BeautifulSoup(response, 'html.parser')
            #    #df['post_url'].append(post_id) # url 
            #    #df = df.assign(post_url = post_id)
            #    post = scrape_post(bs)
            #    post = post.assign(post_url = post_id)
            #    df = df.append(post)
            #    df['company'] = company_name # easier merge
        except:
            exception_post.append(url)
    #return df
    store_path = '/Users/fangfeishu/Dropbox/Blind/company_post'
    df.to_csv(os.path.join(store_path, str(company_name)+'.csv'))

#f write_firm_post(company_name):
#   store_path = '/Users/fangfeishu/Dropbox/Backup/company_post'
#   scrape_firm_post(company_name).to_csv(os.path.join(store_path, str(company_name)+'.csv'))



def scrape_firm_comments(company_name):
    #comment_date = []
    #comment_like = []
    #comment_text = []
    #comment_user = []
    #comment_position = []
    #comment_firm = []
    #comment_url = []
    #exception_url = []
    #column_names = ['comment_url, comment_date, comment_text, comment_like, comment_user, comment_firm, comment_position']
    #df = pd.DataFrame(columns = column_names)
    df = pd.DataFrame()
    #for post_id in post_by_firm_list:
    domurl = 'https://www.teamblind.com'
    exception_url = []
    for post_id in extract_post(company_name): 
        url =  u''.join((domurl,post_id))
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        time.sleep(2)
        #print('scraping ...' + url)
        try:
            response = requests.get(url, headers = headers) #as response:  
            bs = BeautifulSoup(response.text, 'html.parser')
            comment = scrape_comments(bs)
            comment = comment.assign(comment_url = post_id)
            df = df.append(comment)
            df['company'] = company_name
            #delays = [7, 4, 6, 2, 1, 9]
            #delay = np.random.choice(delays)
            #with urlopen(url) as response:
            #    bs = BeautifulSoup(response, 'html.parser')
            #    comment = scrape_comments(bs)
            #    comment = comment.assign(comment_url = post_id)
            #    df = df.append(comment)
            #    df['company'] = company_name
        except:
            exception_url.append(url) # store exceptions 
    store_path = '/Users/fangfeishu/Dropbox/Blind/company_comment'
    df.to_csv(os.path.join(store_path, str(company_name)+'.csv'))

    # post id + comments 
    # follow_post = pd.DataFrame(np.column_stack([comment_url, comment_date, comment_text, comment_like, comment_user, comment_firm, comment_position]), columns = ['comment_url','comment_date', 'comment_text', 'comment_like', 'comment_user', 'comment_firm', 'comment_position'])
#    return follow_post


if __name__ == '__main__':
    user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    with open('full_list.txt', 'r') as f: # pilot: company_list.txt
        company_list = [line.rstrip() for line in f]
    for firm in company_list:
        scrape_firm_post(firm)
        print('---Finish scraping original posts for: ' + firm)
        scrape_firm_comments(firm)
        print('---Finish scraping comments for: ' + firm)