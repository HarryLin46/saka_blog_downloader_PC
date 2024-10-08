import requests,bs4,os,json,time
from txt_to_html_nogi import prepare_html_nogi
import re

##download HTML
url = 'https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=0107&ct=48006/s/n46/diary/detail/100509?ima=2301&cd=MEMBER'
# url = "https://www.nogizaka46.com/s/n46/diary/MEMBER?ima=1530"


## create member list
member_list = []
with open("member/nogi/member_list.txt",'r',encoding='utf-8') as file:
    for member in file:
        member_list.append(member.rstrip("\n"))

# print(member_list)


##find the blog link of current page
def get_next_page(current_objSoup):
    global current_page,download_complete
    
    nextPages = current_objSoup.find_all('ul',class_ = "pager")
    nextpage = nextPages[0].find_all('li',class_ = 'coun')
#     print(len(nextpage))
#     if current_page == 3:
#         download_complete = True
#         return ''
    for i in range(len(nextpage)):
        if nextpage[i].text == str(current_page+1):
            current_page += 1
            targetpage = nextpage[i]
            link = targetpage.find('a')['href']
            return url[:26] + link
    #it is end
    download_complete = True
    return ''

def download_pictures(blog_url,blog_index):
    global current_new,download_complete,current_page,member_list,author_member
    #url = https://www.nogizaka46.com/s/n46/diary/detail/100577?ima=2936&cd=MEMBER
    html = requests.get(blog_url)
    time.sleep(1)
    objSoup = bs4.BeautifulSoup(html.text,'lxml')
    
    imgTag = objSoup.select('img')
#     print(len(imgTag))

    author_member = objSoup.find('p',class_ = 'bd--prof__name f--head').text
    #if the member is don't care, then skip
    with open('./member/nogi/concerned_member.txt', 'r', encoding='utf-8') as file:
        concerned_members = file.read().splitlines()
        concerned_members_no_space = [re.sub(r'\s+', '', member) for member in concerned_members]
        author_member_no_space = re.sub(r'\s+', '', author_member)
    
    blog_title = objSoup.find('h1', class_ = 'bd--hd__ttl f--head a--tx js-tdi').text
    if blog_title is None:
        blog_title = ''
    print("running:",author_member,blog_title)

    dateTime = objSoup.find('p', class_ = "bd--hd__date a--tx js-tdi").text
    date = dateTime[:10]
    date = date.replace('.','')
    
    data = [dateTime,author_member,blog_title]
        
    # print("data: ",data)
    # print("current_new: ",current_new)
    # print(data[0]==current_new[0],data[1]==current_new[1],data[2]==current_new[2])
    author_member_no_space = re.sub(r'\s+', '', author_member)
    current_new_member_no_space = re.sub(r'\s+', '', current_new[1])
    if data[0]==current_new[0] and author_member_no_space==current_new_member_no_space: #we can stop here
        # print("download_complete become True")
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

        dir_path_member = 'blog_source/Nogizaka46/' + author_member
        
        if author_member[-5:] == '期生リレー':
            member = blog_title.split()[-1]
            if not member in member_list:
                member = ''.join(blog_title.split()[-2:])
                if not member in member_list:
                    print('成員名字找錯')
            dir_path = 'blog_source/Nogizaka46/' + author_member + '/' + member
            os.makedirs(dir_path,exist_ok=True)
                
            dir_path = 'blog_source/Nogizaka46/' + author_member + '/' + member + '/' + date + ' ' + blog_title
        else:
            dir_path = 'blog_source/Nogizaka46/' + author_member + '/' + date + ' ' + blog_title

        print(blog_title)
        #the space at the end of blog_title should be remove
        dir_path = dir_path.rstrip(' .')
        
        os.makedirs(dir_path_member,exist_ok=True)
        print(dir_path)
        if os.path.exists(dir_path) == False:
            os.makedirs(dir_path)
            if len(imgTag) >= 0 :
                for i in range(len(imgTag)):
                    imgUrl = imgTag[i].get('src')

                    try:
                        is_effective_url = (not imgUrl is None) and ((imgUrl[-4:] in ['.jpg','.tif','.png']) or (imgUrl[-5:] in ['.jpeg']))
                        if is_effective_url: #we may catch something we don't want(no 'src') 
                            finUrl = url[:26] + imgUrl
                            
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
    global current_new,download_complete,current_page
    html = requests.get(current_new_url)
    time.sleep(1)
    objSoup = bs4.BeautifulSoup(html.text,'lxml')
    
    author_member = objSoup.find('p',class_ = 'bd--prof__name f--head').text
    blog_title = objSoup.find('h1', class_ = 'bd--hd__ttl f--head a--tx js-tdi').text
    if blog_title is None:
        blog_title = ''
    dateTime = objSoup.find('p', class_ = "bd--hd__date a--tx js-tdi").text
    
    current_new_data = [dateTime,author_member,blog_title]
    
    fn = 'blog_source/Nogizaka46/current_new.json'
    with open(fn,'w',encoding='utf-8') as obj:
        json.dump(current_new_data,obj,ensure_ascii=False)

def download_blogs(current_objSoup):
    global current_new,current_page,download_complete
    blogData = current_objSoup.find_all('a',class_='bl--card js-pos a--op hv--thumb')
    
    for i in range(len(blogData)):
        link = blogData[i]['href']
        blog_url = url[:26] + link
        
        if not download_complete:
            download_pictures(blog_url,i)
            if not download_complete: #it may be True after running download_pictures()
                prepare_html_nogi(blog_url)
        else:
            break

        
        if current_page == 1 and i == 0: #always update first
            update_current_new(blog_url)

##Run!!
def nogi_crawling():
    global current_new,current_page,download_complete
    ##set some parameters
    current_page = 1
    current_url = 'https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=0107&ct=48006/s/n46/diary/detail/100509?ima=2301&cd=MEMBER'

    download_complete = False

    ##get current new
    fn = 'blog_source/Nogizaka46/current_new.json'

    try:
        with open(fn,'r',encoding='utf-8') as fnobj:
            current_new = json.load(fnobj)

    except Exception: #the 1st run of this code
        current_new = ''

    while not download_complete:
        print(current_page)
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
        # download_blogs(current_objSoup)
        if not download_complete:
            current_url = get_next_page(current_objSoup)
    print("Download complete!")

