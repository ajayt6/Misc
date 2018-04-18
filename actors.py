from bs4 import BeautifulSoup
import requests
import pickle
import operator
import re
import os
from google_results import google_search_scrape #this line works even though it shows up as an error


hindu_c = ['Nair','Menon','Iyer','Bhaskaran','Kurup','Murugan','Raghavan','Ramu','Sivan','Mahadev','Shivan','Varma','Verma','Pillai','Pilla','Parameswaran','Jagannathan','Balakrishnan','Balachandran','Shivaprasad']
christian_c = ['Alex','Zachariah','Sunny','John','Peter','George','Michael','James','Mathews','Mathew','Varghese','Albert','Charlie','Jimmy','Jacob','Thoma','Samuel','Freddy','Jacky','Cheriyan','Cherian','Richard']
muslim_c = ['Abdullah', 'Abdulla','Omar','Ahmed','Abdul','Ali','Rashid','Nazir','Ibrahim']

hindu_c = set(hindu_c)
christian_c = set(christian_c)
muslim_c = set(muslim_c)

def namestr(obj, namespace):
    l = ([name for name in namespace if namespace[name] is obj])
    return str(l[0])



def main():

    gss = google_search_scrape()

    global hindu_c
    global christian_c
    global muslim_c

    file = namestr(hindu_c,globals() ) + '.p'
    if os.path.exists(file):
        with open(file,'rb') as pfile:
            hindu_c = pickle.load(pfile)

    file = namestr(christian_c, globals()) + '.p'
    if os.path.exists(file):
        with open(file,'rb') as pfile:
            christian_c = pickle.load(pfile)

    file = namestr(muslim_c, globals()) + '.p'
    if os.path.exists(file):
        with open(file,'rb') as pfile:
            muslim_c = pickle.load(pfile)

    print(hindu_c)
    print(christian_c)
    print(muslim_c)

    professions = {  'Dr.' : 'Doctor' ,
                     'Prof.' : 'Professor' ,
                     'Fr.' : 'Father',
                     'Adv.' : 'Lawyer',
                     'Captain' : 'Army officer',
                     'Major' : 'Army officer' ,
                     'Inspector' : 'Police officer',
                     'Dysp' : 'Police officer' ,
                     'C.I.D.': 'Police officer',
                     'Police' : 'Police officer'
                     }


    actor_d = { 'Prem Nazir' : 'https://www.imdb.com/name/nm0623427/', #0
                'Mohanlal' :  'http://www.imdb.com/name/nm0482320/?ref_=fn_al_nm_1' , #1
                'Mammootty' : 'http://www.imdb.com/name/nm0007123/?ref_=nv_sr_1' , #2
                'Kamal Haasan' : 'http://www.imdb.com/name/nm0352032/' , #3
                'Rajinikanth' : 'http://www.imdb.com/name/nm0707425/' , #4
                'Shah Rukh Khan' : 'http://www.imdb.com/name/nm0451321/' , #5
                'Tom Cruise' : 'http://www.imdb.com/name/nm0000129/' , #6
                'Shobana' : 'http://www.imdb.com/name/nm0811794/', #7
                'Jyothika' : 'http://www.imdb.com/name/nm0433392/' , #8
                'Simran' : 'http://www.imdb.com/name/nm0801264/' ,#9
                'Manju Warrier' : 'http://www.imdb.com/name/nm0913097/' , #10
                'Jayalalitha' : 'http://www.imdb.com/name/nm0412883/' , #11
                }

    actor_l = []

    for actor in actor_d:
        actor_l.append(actor)


    actor = actor_l[2]

    #print("Actor name is: " + actor)

    actor = input("Enter actor name: ")
    url = gss.get_first_result_url(actor + ' imdb')

    #url = actor_d[actor]
    response = requests.get(url)
    html_string = response.text  # Access the HTML with the text property


    soup = BeautifulSoup(html_string, 'lxml')  # Parse the HTML as a string

    movies_divs = soup.find_all("div", class_="filmo-category-section")[0]


    movies_divs_odd = movies_divs.find_all("div", class_="filmo-row odd")
    movies_divs_even = movies_divs.find_all("div", class_="filmo-row even")

    all_movies_divs = []

    for div in movies_divs_even:
        all_movies_divs.append(div)

    for div in movies_divs_odd:
        all_movies_divs.append(div)

    names = []

    for movie_div in all_movies_divs:
        name = (movie_div.get_text().split('\n')[-2])

        if  len(name.strip()) > 0:
            names.append(name)

    name_d = {}

    hindu = []
    christian = []
    muslim = []
    uncategorized_religion = []
    religion_ds = [ (hindu_c,hindu) , (christian_c,christian ), (muslim_c,muslim)]

    train = input("Do you want to train name to religion mapping? (y/n)")


    for name in names:


        name = re.sub("[\(\[].*?[\)\]]", "", name)

        f=0
        for pair in religion_ds:
            for word in pair[0]:
                if word.lower() in name.lower():
                    pair[1].append(name)
                    f=1
                    break
            if f==1:
                break

        if f==0:
            uncategorized_religion.append(name)

        name_l = name.split()

        for part in name_l:

            if part in name_d:
                name_d[part].append(name)
            else:
                name_d[part] = [name]

            # analyze parts of the name for a possible categorization
            if f==0 and train == 'y':
                if part not in christian_c and part not in muslim_c and part not in hindu_c:
                    print(part)
                    r = input("enter character for religion (h for hindu, c for christian, m for muslim, nothing for not sure)")

                    if len(r) == 0:
                        pass
                    elif r == 'h':
                        hindu_c.add(part)
                    elif r == 'c':
                        christian_c.add(part)
                    elif r == 'm':
                        muslim_c.add(part)

    #save modified religion sets
    with open(namestr(hindu_c, globals()) + '.p','wb') as file:
        pickle.dump(hindu_c,file)

    with open(namestr(christian_c, globals()) + '.p','wb') as file:
        pickle.dump(christian_c,file)

    with open(namestr(muslim_c, globals()) + '.p','wb') as file:
        pickle.dump(muslim_c,file)


    #clean name_d
    remove_words = ['/','Appearance','(as', 'Appearance)']
    for word in remove_words:
        if word in name_d:
            del name_d[word]



    #construct a ranked list
    name_counts = [ ( name, len(name_d[name]) ) for name in name_d ]


    name_counts = sorted(name_counts, key = operator.itemgetter(1), reverse=True)

    print(name_counts)


    profession_d = {}

    for profession in professions:

        if profession in name_d:
            if professions[profession] in profession_d:
                profession_d[professions[profession]] += len(name_d[profession])
            else:
                profession_d[professions[profession]] = len(name_d[profession])

    for profession in profession_d:
        print("Number of movies as " + profession + " : " +str(profession_d[profession]))

    print(" ")

    print(hindu)
    print("hindu : " + str(len(hindu)))
    print(christian)
    print("christian : " + str(len(christian)))
    print(muslim)
    print("muslim : " + str(len(muslim)))
    print(uncategorized_religion)
    print("uncategorized religion : " + str(len(uncategorized_religion)))

main()