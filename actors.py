from bs4 import BeautifulSoup
import requests
import pickle
import operator
import re
import os
from google_results import google_search_scrape #this suresh gopiline works even though it shows up as an error

data_folder = 'data/'
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

    global data_folder


    file = data_folder + namestr(hindu_c,globals() ) + '.p'
    if os.path.exists(file):
        with open(file,'rb') as pfile:
            hindu_c = pickle.load(pfile)

    file = data_folder + namestr(christian_c, globals()) + '.p'
    if os.path.exists(file):
        with open(file,'rb') as pfile:
            christian_c = pickle.load(pfile)

    file = data_folder + namestr(muslim_c, globals()) + '.p'
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
                     'Police' : 'Police officer',
                     'IPS' : 'Police officer',
                     'I.P.S.' : 'Police officer'
                     }


    actor_data_d = {}
    actor_data_file = data_folder + 'actor_data.p'
    if os.path.exists(actor_data_file):
        with open(actor_data_file,'rb') as pfile:
            actor_data_d = pickle.load(pfile)

    actor = input("Enter actor name: ")
    pflag = False

    if actor.lower() in actor_data_d:
        url = actor_data_d[actor.lower()]
    else:
        url = gss.get_first_result_url(actor + ' imdb')
        actor_data_d[actor.lower()] = url
        pflag = True

    if url in actor_data_d:
        html_string = actor_data_d[url]
    else:
        response = requests.get(url)
        html_string = response.text  # Access the HTML with the text property
        actor_data_d[url] = html_string
        pflag = True

    if pflag:
        #pickle the data structure
        with open(actor_data_file,'wb') as pfile:
            pickle.dump(actor_data_d,pfile)




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

        name_l = name.split()

        f=0
        for pair in religion_ds:
            for part in name_l:
                if part.lower() in pair[0]:
                    pair[1].append(name)
                    f=1
                    break
            if f==1:
                break

        if f==0:
            uncategorized_religion.append(name)

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
                        hindu_c.add(part.lower())
                    elif r == 'c':
                        christian_c.add(part.lower())
                    elif r == 'm':
                        muslim_c.add(part.lower())

    #save modified religion sets
    with open(data_folder + namestr(hindu_c, globals()) + '.p','wb') as file:
        pickle.dump(hindu_c,file)

    with open(data_folder + namestr(christian_c, globals()) + '.p','wb') as file:
        pickle.dump(christian_c,file)

    with open(data_folder + namestr(muslim_c, globals()) + '.p','wb') as file:
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