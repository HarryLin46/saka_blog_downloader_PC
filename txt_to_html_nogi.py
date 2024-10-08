from PIL import Image
import io,os
import re
import sys
import tempfile
import requests,bs4
import time

def resize_pictures_nogi(original_html): 
    # find all imgs
    img_tags = re.findall(r'<img src=[\'"](.*?)[\'"]', original_html)

    new_html = original_html
    for img_path in img_tags:
        # print("img_path:",img_path)
        # img_path = os.path.join(dir_path,img_path)
        with Image.open(img_path) as img:
            # resize the img
            target_width = 896
            max_size = (target_width, target_width * 10)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            file_type = img_path[-4:]
            # save the resized img as tempfile
            if file_type==".jpg":
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_img_file:
                    img.save(temp_img_file, format='JPEG')
                    temp_img_path = temp_img_file.name

                    # change image pathsnin html
                    new_html = new_html.replace(img_path, temp_img_path)
            elif file_type==".png":
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_img_file:
                    img.save(temp_img_file, format='PNG')
                    temp_img_path = temp_img_file.name

                    # change image pathsnin html
                    new_html = new_html.replace(img_path, temp_img_path)
            elif file_type==".tif":
                with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as temp_img_file:
                    img.save(temp_img_file, format='TIFF')
                    temp_img_path = temp_img_file.name

                    # change image pathsnin html
                    new_html = new_html.replace(img_path, temp_img_path)

    return new_html

def modify_html_with_responsive_images(html_content): #unused
    max_width = "896px"
    # max_height = "200px"

    # add <img> Tag
    modified_html = re.sub(r'<img(.*?)src=[\'"](.*?)[\'"](.*?)>',
                           r'<img\1src="\2"\3 style="max-width: {}; max-height: {};">'.format(max_width, max_height),
                           html_content)
    return modified_html

def txt_to_html_nogi(file_path):
    html_content = ""

    with open(file_path, 'r', encoding='utf-8') as file:
        # max_width = "896px"
        for line in file:
            if line.strip().endswith(".jpg"):
                image_path = "blog_source/"+line.strip()
                # html_content += f"<img src='{image_path}' style=\"max-width: {max_width};\"><br>"
                html_content += f"<img src='{image_path}' /><br>"
            else:
                html_content += f"<p>{line.strip()}</p>"

    new_html_content = resize_pictures(html_content)
    return new_html_content


def prepare_html_nogi(url): #we need to modify the link of the images
    # with open(html_path, 'r', encoding='utf-8') as file:
    #     raw_html = file.read()
    html = requests.get(url)
    time.sleep(1)
    objSoup = bs4.BeautifulSoup(html.text,'lxml')


    author_member = objSoup.find('p',class_ = 'bd--prof__name f--head').text
    #if the member is don't care, then skip
    with open('./member/nogi/concerned_member.txt', 'r', encoding='utf-8') as file:
        concerned_members = file.read().splitlines()
        concerned_members_no_space = [re.sub(r'\s+', '', member) for member in concerned_members]
        author_member_no_space = re.sub(r'\s+', '', author_member)
        if not author_member_no_space in concerned_members_no_space:
            return

    blog_title = objSoup.find('h1', class_ = 'bd--hd__ttl f--head a--tx js-tdi').text
    if blog_title is None:
        blog_title = ''

    dateTime = objSoup.find('p', class_ = "bd--hd__date a--tx js-tdi").text
    date = dateTime[:10]
    date = date.replace('.','')
    
    data = [dateTime,author_member,blog_title]

    # print(data)


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

    
    #the space at the end of blog_title should be remove
    dir_path = dir_path.rstrip(' .')
    # print(dir_path)

    article = objSoup.find('div', class_ ="bd--edit")
    
    img_idx=0
    img_types = ['.jpg','.png', '.tif']#file could be .jpg, .png, .tif
    for img_tag in article.find_all("img"):
        for img_type in img_types:
            img_path = os.path.join(dir_path,f"{str(img_idx).zfill(2)}{img_type}")
            if os.path.isfile(img_path):
                img_tag['src'] = f"{str(img_idx).zfill(2)}{img_type}"
                break
        img_idx+=1
        # print(img_tag)

    # print(article)
    
    # print(article)
    # new_article = resize_pictures(str(article),dir_path)
    # print(new_article)
    with open(os.path.join(dir_path,'blog_article.html'), 'w', encoding='utf-8') as file:
        file.write(str(article))

    # return new_html_content


if __name__ == '__main__':
    url = "https://www.nogizaka46.com/s/n46/diary/detail/102263?ima=2029"
    prepare_html(url)
    
    

