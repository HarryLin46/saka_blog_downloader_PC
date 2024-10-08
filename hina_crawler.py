import requests,bs4,os,json,time
from txt_to_html_hina import prepare_html_hina
import re

url = 'https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000'

def get_next_page(current_objSoup):
    global current_page,download_complete
    nextPages = current_objSoup.find_all('li', class_ = 'c-pager__item--count')
    
    for i in range(len(nextPages)):
        nextpage = nextPages[i].find('a')
        time.sleep(0.5)
        if  nextpage is not None and nextpage.text == str(current_page+1):
            current_page += 1
            link = nextpage['href']
            return url[:28] + link
        else:
            continue
    #it is end
    download_complete = True
    return ''

def download_pictures(blog_url):
    global current_new,download_complete,current_page
    #url = https://www.nogizaka46.com/s/n46/diary/detail/100577?ima=2936&cd=MEMBER
    html = requests.get(blog_url)
    time.sleep(1)
    objSoup = bs4.BeautifulSoup(html.text,'lxml')
    
    blog_tags = objSoup.find_all('div', class_ = "c-blog-article__text")
#     print(len(imgTag))

    author_members_raw = objSoup.find_all('div',class_ = 'c-blog-article__name')
    author_members = []
    for i in author_members_raw:
        author_members.append(i.text.strip())

    #record the concerned members first, avoid opening the file at each iteration
    with open('./member/hinata/concerned_member.txt', 'r', encoding='utf-8') as file:
        concerned_members = file.read().splitlines()
        concerned_members_no_space = [re.sub(r'\s+', '', member) for member in concerned_members]
        
    blog_title_raw = objSoup.find_all('div', class_ = "c-blog-article__title")
    blog_titles = []
    for i in blog_title_raw:
        bt = i.text
        if bt is None:
            bt = ''
        blog_titles.append(bt.strip())
        
    dateTime_raw = objSoup.find_all('div', class_ = "c-blog-article__date")
    dates = []
    for i in dateTime_raw:
        dateTime = i.text.strip() #get '2022.8.15 18:30'
        dateTime = dateTime.split('.')
        year,month,day = dateTime[0],dateTime[1].zfill(2),dateTime[2][:-6].zfill(2)

        dates.append(year+month+day)
    
    #run for 20 times in 1 page
    for k in range(len(blog_tags)):
        imgTag = blog_tags[k].find_all('img')
        author_member = author_members[k]
        #if the member is don't care, then skip
        author_member_no_space = re.sub(r'\s+', '', author_member)

        blog_title = blog_titles[k]
        date = dates[k]
        print("running:",author_member,blog_title)
    
        data = [dateTime_raw[k].text.strip(),author_member,blog_title]
        author_member_no_space = re.sub(r'\s+', '', author_member)
        current_new_member_no_space = re.sub(r'\s+', '', current_new[1])
        if data[0]==current_new[0] and author_member_no_space==current_new_member_no_space: #we can stop here
            download_complete = True
        else:
            #if the member is don't care, then skip
            if not author_member_no_space in concerned_members_no_space:
                continue
            #blog_title may not a good directory name
            blog_title = blog_title[:150]
            special_char = r'/\:*?"<>|'
            for i in special_char:
                blog_title = blog_title.replace(i,'')

            dir_path_member = 'blog_source/Hinatazaka46/' + author_member
            dir_path = 'blog_source/Hinatazaka46/' + author_member + '/' + date + ' ' + blog_title

            #the space at the end of blog_title should be remove
            dir_path = dir_path.rstrip(' .')
            os.makedirs(dir_path_member,exist_ok=True)

            # if os.path.exists(dir_path_member) == False:
            #     os.mkdir(dir_path_member)
            if os.path.exists(dir_path) == False:
                os.mkdir(dir_path)
                if len(imgTag) >= 0 : # > 0
                    for i in range(len(imgTag)):
                        imgUrl = imgTag[i].get('src')

                        try:
                            is_effective_url = (not imgUrl is None) and ((imgUrl[-4:] in ['.jpg','.tif','.png']) or (imgUrl[-5:] in ['.jpeg']))
                            if is_effective_url: #we may catch something we don't want(no 'src') 
                                
                                picture = requests.get(imgUrl)
                                time.sleep(0.5)
                                picture.raise_for_status()
                #                 print('%s 圖片下載成功' %finUrl)

                                pictFile = open(os.path.join(dir_path,str(i).zfill(2) + (imgUrl[-4:] if imgUrl[-4:] in ['.jpg','.tif','.png'] else imgUrl[-5:])),'wb')
                                for diskStorage in picture.iter_content(1024*1024):
                                    pictFile.write(diskStorage)
                                pictFile.close()
                        except requests.exceptions.HTTPError:
                            print(current_page,k+1,'找不到網頁! 照片可能被鎖了',author_member,blog_title)

                        except:
                            print(current_page,k+1,'新的未知錯誤出現! 可能是異常個案',author_member,blog_title)
                    prepare_html_hina(blog_tags[k],data,dates[k])
            else:
                print('看到重複的部落格了')

def update_current_new(current_new_url):
    html = requests.get(current_new_url)
    time.sleep(1)
    objSoup = bs4.BeautifulSoup(html.text,'lxml')
    
    blog_tags = objSoup.find_all('div', class_ = "c-blog-article__text")
    
    author_members_raw = objSoup.find_all('div',class_ = 'c-blog-article__name')
    author_member = author_members_raw[0].text.strip()
    
    blog_title_raw = objSoup.find_all('div', class_ = "c-blog-article__title")
    bt = blog_title_raw[0].text
    if bt is None:
        blog_title = ''
    else:
        blog_title = bt.strip()
    
    dateTime_raw = objSoup.find_all('div', class_ = "c-blog-article__date")
    dateTime = dateTime_raw[0].text.strip() #get '2022.8.15 18:30'
    
    current_new_data = [dateTime,author_member,blog_title]
    
    fn = 'blog_source/Hinatazaka46/current_new.json'
    with open(fn,'w',encoding='utf-8') as obj:
        json.dump(current_new_data,obj,ensure_ascii=False)

# def download_blogs(current_objSoup):
#     global current_new,current_page,download_complete
#     blogData = current_objSoup.find_all('a',class_='bl--card js-pos a--op hv--thumb')
    
#     for i in range(len(blogData)):
#         link = blogData[i]['href']
#         blog_url = url[:26] + link
        
#         if not download_complete:
#             download_pictures(blog_url,i)
        
#         if current_page == 1 and i == 0: #always update first
#             update_current_new(blog_url)

##Run!!
def hina_crawling():
    global current_new,current_page,download_complete
    current_page = 1
    current_url = url

    ##get current new
    fn = 'blog_source/Hinatazaka46/current_new.json'

    try:
        with open(fn,'r',encoding='utf-8') as fnobj:
            current_new = json.load(fnobj)

    except Exception: #the 1st run of this code
        current_new = ''

    download_complete = False
    while not download_complete:
        print(current_page)
        if current_page == 1:
            update_current_new(current_url)
            
        html = requests.get(current_url)
        current_objSoup = bs4.BeautifulSoup(html.text,'lxml')
        # download_pictures(current_url)
        try:
            download_pictures(current_url)
        except FileExistsError as e:
            print('檔案已存在! 載到重複的部落格')
            break
        except FileNotFoundError as e:
            print('檔案找不到! 可能部落格名稱太長或路徑有錯')
            break
        except NotADirectoryError as e:
            print('目錄名稱無效! 可能資料夾命名不合法')
            break
        except Exception as e:
            print( e,'可能為異常個案')
        current_url = get_next_page(current_objSoup)
    print("Download complete!")
