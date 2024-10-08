import requests,bs4,os,json,time
import re
from txt_to_html_saku import prepare_html_saku

url = "https://sakurazaka46.com/s/s46/diary/blog/list?ima=0000&page=0&cd=blog"

def get_next_page(current_objSoup):
    global current_page,download_complete
    
    box = current_objSoup.find('div', class_ = "com-pager wid1200")
    nextpage = box.find_all('li')
    for i in range(len(nextpage)):
        if nextpage[i].text == str(current_page+1):
            current_page += 1
            targetpage = nextpage[i]
            link = targetpage.find('a')['href']
            return url[:24] + link
    #it is end
    download_complete = True
    return ''

def download_pictures(blog_url,blog_index):
    global current_new,download_complete
    #url = https://www.nogizaka46.com/s/n46/diary/detail/100577?ima=2936&cd=MEMBER
    html = requests.get(blog_url)
    time.sleep(1)
    objSoup = bs4.BeautifulSoup(html.text,'lxml')
    
    box = objSoup.find('div',class_ = "box-article")
    imgTag = box.find_all('img')
    
    author_member = objSoup.find('p', class_ = "name").text

    #record the concerned members first, avoid opening the file at each iteration
    with open('./member/sakura/concerned_member.txt', 'r', encoding='utf-8') as file:
        concerned_members = file.read().splitlines()
        concerned_members_no_space = [re.sub(r'\s+', '', member) for member in concerned_members]
    
    blog_title = objSoup.find('h1', class_ = "title").text
    if blog_title is None:
        blog_title = ''
    
    dateTime_raw = objSoup.find_all('p', class_ = "date wf-a")
    # print("dateTime_raw:",dateTime_raw)
    # dateTime = dateTime_raw[1].text.split('/')
    dateTime = dateTime_raw[1].text.replace('/','.')
    # date = dateTime[0] + dateTime[1] + dateTime[2][:2]
    date =  dateTime[:4] + dateTime[5:7] + dateTime[8:10]
    # print("dateTime:",dateTime)
    # print("dateTime_V:",dateTime_V)
    # print("date:",date)
    
    print("running:",author_member,blog_title)
    data = [dateTime,author_member,blog_title]
    author_member_no_space = re.sub(r'\s+', '', author_member)
    current_new_member_no_space = re.sub(r'\s+', '', current_new[1])
    if data[0]==current_new[0] and author_member_no_space==current_new_member_no_space: #we can stop here
        download_complete = True
    else:
        #if the member is don't care, then skip
        if not author_member_no_space in concerned_members_no_space:
            return
        #blog_title may not a good directory name
        blog_title = blog_title[:150]
        special_char = r'/\:*?"<>|'
        for i in special_char:
            blog_title = blog_title.replace(i,'')

        dir_path_member = 'blog_source/Sakurazaka46/' + author_member
        dir_path = 'blog_source/Sakurazaka46/' + author_member + '/' + date + ' ' + blog_title
        
        #the space at the end of blog_title should be remove
        dir_path = dir_path.rstrip(' .')
        os.makedirs(dir_path_member,exist_ok=True)
        
        # if os.path.exists(dir_path_member) == False:
        #     os.mkdir(dir_path_member)
        if os.path.exists(dir_path) == False:
            os.mkdir(dir_path)
            if len(imgTag) >= 0 :
                for i in range(len(imgTag)):
                    imgUrl = imgTag[i].get('src')

                    try:
                        is_effective_url = (not imgUrl is None) and ((imgUrl[-4:] in ['.jpg','.tif','.png']) or (imgUrl[-5:] in ['.jpeg']))
                        if is_effective_url: #we may catch something we don't want(no 'src') 
                            finUrl = url[:24] + imgUrl
                            
                            picture = requests.get(finUrl)
                            time.sleep(0.5)
                            picture.raise_for_status()
            #                 print('%s 圖片下載成功' %finUrl)

                            pictFile = open(os.path.join(dir_path,str(i).zfill(2) + (imgUrl[-4:] if imgUrl[-4:] in ['.jpg','.tif','.png'] else imgUrl[-5:])),'wb')
                            for diskStorage in picture.iter_content(1024*1024):
                                pictFile.write(diskStorage)
                            pictFile.close()
                    except requests.exceptions.HTTPError:
                        print(current_page,blog_index+1,'找不到網頁! 照片可能被鎖了',author_member,blog_title)
                        
                    except:
                        print(current_page,blog_index+1,'新的未知錯誤出現! 可能是異常個案',author_member,blog_title)
        else:
            print('看到重複的部落格了')

def update_current_new(current_new_url):
    html = requests.get(current_new_url)
    time.sleep(1)
    objSoup = bs4.BeautifulSoup(html.text,'lxml')
    
    blog_tags = objSoup.find_all('div', class_ = "c-blog-article__text")
    
    author_member = objSoup.find('p', class_ = "name").text
    
    blog_title = objSoup.find('h1', class_ = "title").text
    
    dateTime_raw = objSoup.find_all('p', class_ = "date wf-a")
    # dateTime = dateTime_raw[1].text.split('/')
    dateTime = dateTime_raw[1].text.replace('/','.')
    # date = dateTime[0] + dateTime[1] + dateTime[2][:2]
    date =  dateTime[:4] + dateTime[5:7] + dateTime[8:10]
    
    current_new_data = [dateTime,author_member,blog_title]
    
    fn = 'blog_source/Sakurazaka46/current_new.json'
    with open(fn,'w',encoding='utf-8') as obj:
        json.dump(current_new_data,obj,ensure_ascii=False)

def download_blogs(current_objSoup):
    global current_new,current_page,download_complete
    boxes_raw = current_objSoup.find_all('li',class_ = 'box')
    boxes = []
    for i in boxes_raw:
        if i.find('div',class_ =  'wrap-bg') is not None:
            boxes.append(i)
    
    # print(boxes)
    for i in range(len(boxes)):
        link = boxes[i].find('a')['href']
        blog_url = url[:24] + link
        
        if not download_complete:
            download_pictures(blog_url,i)
            if not download_complete: #it may be True after running download_pictures()
                prepare_html_saku(blog_url)
        
        if current_page == 1 and i == 0: #always update first
            update_current_new(blog_url)


def saku_crawling():
    global current_new,current_page,download_complete
    current_page = 1
    current_url = url
    # fn = current_new_title

    ##get current new
    fn = 'blog_source/Sakurazaka46/current_new.json'

    try:
        with open(fn,'r',encoding='utf-8') as fnobj:
            current_new = json.load(fnobj)

    except Exception: #the 1st run of this code
        current_new = ''

    download_complete = False
    while not download_complete:
        print(current_page)
        # if current_page == 1:
        #     update_current_new(current_url)

        html = requests.get(current_url)
        current_objSoup = bs4.BeautifulSoup(html.text,'lxml')
        try:
            download_blogs(current_objSoup)
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
        
    
if __name__=="__main__":
    saku_crawling()
    # url = "https://sakurazaka46.com/s/s46/diary/blog/list?ima=0000&page=0&cd=blog"

    # fn = 'blog_source/Sakurazaka46/current_new.json'
    # with open(fn,'r',encoding='utf-8') as fnobj:
    #     current_new = json.load(fnobj)
    # # download_pictures(url,0)

    # current_page = 1
    # download_complete = False  
    # html = requests.get(url)
    # current_objSoup = bs4.BeautifulSoup(html.text,'lxml')
    # download_blogs(current_objSoup)
