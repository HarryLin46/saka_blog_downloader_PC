import json
import requests
import bs4
import shutil
import os

## Nogi part
##load member's image
def load_nogi_image(data_list):
    for member in data_list["data"]:
        print(member["name"],member["img"],"\n")
        if member["graduation"] == "YES":
            continue
        image_url = member["img"]

        # send HTTP GET request to image's URL
        response = requests.get(image_url)

        # check if request is success
        if response.status_code == 200:
            image_path = f"member/nogi/{member["name"]}.jpg"

            # write the data into the file
            with open(image_path, "wb") as file:
                file.write(response.content)


def prepare_nogi_list(data_list):
    filtered_data = [member["name"] for member in data_list["data"] if member["graduation"] == "NO" and member["name"] != "乃木坂46"]
    with open('member/nogi/member_list.txt', 'w', encoding='utf-8') as file:
        for member in filtered_data:
            file.write(member+"\n")
            os.makedirs(os.path.join("blog_source/Nogizaka46",member),exist_ok=True)#create member's file for convenience


def update_nogi():
    #update member source
    url = "https://www.nogizaka46.com/s/n46/api/list/member?so=AB"
    
    #send request
    response = requests.get(url)

    html_txt = response.text
    raw_data = html_txt[html_txt.find('{'):html_txt.rfind('}')+1]

    data_list = json.loads(raw_data)
    load_nogi_image(data_list)
    prepare_nogi_list(data_list)



## Hinata part
def load_hinata_image(member_list):
    for member in member_list:
        names = member.find_all('div',class_ = "c-member__name")
        name = names[0].text.strip() #it has space at front and end, use "strip" to remove
        print(name) 

        image_paths = member.find_all('div',class_ = "c-member__thumb") #ex. <div class="c-member__thumb"> <img src="https://cdn.hinatazaka46.com/images/14/b69/af4879fb1ef702360ec3f6cc89507/400_320_102400.jpg"/></div>
        image_path = image_paths[0].find("img").get("src")
        print(image_path) 

        # send HTTP GET request to image's URL
        response = requests.get(image_path)

        # check if request is success
        if response.status_code == 200:

            image_path = f"member/hinata/{name}.jpg"
            # write the data into the file
            with open(image_path, "wb") as file:
                file.write(response.content)

def prepare_hinata_list(member_list):
    with open('member/hinata/member_list.txt', 'w', encoding='utf-8') as file:
        for member in member_list:
            names = member.find_all('div',class_ = "c-member__name")
            name = names[0].text.strip() #it has space at front and end, use "strip" to remove
            file.write(f"{name}\n")
            os.makedirs(os.path.join("blog_source/Hinatazaka46",name),exist_ok=True)#create member's file for convenience
        file.write("ポカ"+"\n") #hard code the blue bird
        os.makedirs(os.path.join("blog_source/Hinatazaka46","ポカ"),exist_ok=True)#create member's file for convenience

def update_hinata():
    url = "https://www.hinatazaka46.com/s/official/search/artist?ima=0000"

    html = requests.get(url)

    objSoup = bs4.BeautifulSoup(html.text,'lxml')

    members = objSoup.find_all('div', class_ = "sorted sort-syllabary")[0] #togeher as one obj in the list, use [0] to extract


    member_list = members.find_all('li', class_ = "p-member__item")
    
    load_hinata_image(member_list)
    prepare_hinata_list(member_list)


##sakura part
def load_sakura_image(member_list):
    for member in member_list:
        names = member.find_all('p',class_ = "name")
        name = names[0].text
        print(name) 

        image_paths = member.find_all('img') #ex. <li class="box" data-member="69"> <img alt="山下 瞳月" src="/images/14/b28/8113a5e1360897f54e569b7774dc1/400_320_102400.jpg"/></li>
        image_path = "https://sakurazaka46.com/"+ image_paths[0].get("src")
        print(image_path) 

        # send HTTP GET request to image's URL
        response = requests.get(image_path)

        # check if request is success
        if response.status_code == 200:

            image_path = f"member/sakura/{name}.jpg"
            # write the data into the file
            with open(image_path, "wb") as file:
                file.write(response.content)

def prepare_sakura_list(member_list):
    with open('member/sakura/member_list.txt', 'w', encoding='utf-8') as file:
        for member in member_list:
            names = member.find_all('p',class_ = "name")
            name = names[0].text
            file.write(f"{name}\n")
            os.makedirs(os.path.join("blog_source/Sakurazaka46",name),exist_ok=True)#create member's file for convenience
            

def update_sakura():
    url = "https://sakurazaka46.com/s/s46/search/artist?ima=0000&display=syllabary"

    html = requests.get(url)

    objSoup = bs4.BeautifulSoup(html.text,'lxml')

    members = objSoup.find_all('ul', class_ = "elem fx")[0] #togeher as one obj in the list, use [0] to extract

    member_list = members.find_all('li') #<li class="box" data-member="69"> <img alt="山下 瞳月" />...</li>
    
    load_sakura_image(member_list)
    prepare_sakura_list(member_list)

# if __name__ == '__main__':
#     update_nogi()

    





