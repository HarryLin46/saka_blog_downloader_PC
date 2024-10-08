import requests
import bs4

def load_member_image(member_list):
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

def prepare_member_list(member_list):
    with open('member/hinata/member_list.txt', 'w', encoding='utf-8') as file:
        for member in member_list:
            names = member.find_all('div',class_ = "c-member__name")
            name = names[0].text.strip() #it has space at front and end, use "strip" to remove
            file.write(f"{name}\n")
        file.write("ポカ"+"\n") #hard code the blue bird

def update_hinata():
    url = "https://www.hinatazaka46.com/s/official/search/artist?ima=0000"

    html = requests.get(url)

    objSoup = bs4.BeautifulSoup(html.text,'lxml')

    members = objSoup.find_all('div', class_ = "sorted sort-syllabary")[0] #togeher as one obj in the list, use [0] to extract


    member_list = members.find_all('li', class_ = "p-member__item")
    
    load_member_image(member_list)
    prepare_member_list(member_list)


if __name__ == '__main__':
    update_hinata()
