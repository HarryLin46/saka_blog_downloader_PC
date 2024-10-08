import requests
import bs4

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

def update_sakura():
    url = "https://sakurazaka46.com/s/s46/search/artist?ima=0000&display=syllabary"

    html = requests.get(url)

    objSoup = bs4.BeautifulSoup(html.text,'lxml')

    members = objSoup.find_all('ul', class_ = "elem fx")[0] #togeher as one obj in the list, use [0] to extract

    member_list = members.find_all('li') #<li class="box" data-member="69"> <img alt="山下 瞳月" />...</li>
    
    load_sakura_image(member_list)
    prepare_sakura_list(member_list)


if __name__ == '__main__':
    update_sakura()
