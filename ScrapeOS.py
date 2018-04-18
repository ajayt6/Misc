from PyPDF2 import PdfFileMerger
from bs4 import BeautifulSoup
import requests

url = "http://pages.cs.wisc.edu/~remzi/OSTEP/"
response = requests.get(url)
html_string = response.text  # Access the HTML with the text property

soup = BeautifulSoup(html_string, 'lxml')  # Parse the HTML as a string
table = soup.find_all('table')[3]  # Grab the fourth table
header_row = table.find_all('tr')[0]
num_sections = len(header_row.find_all('td'))

sections_list = [[] for i in range(num_sections)]

print(len(sections_list))

for row in table.find_all('tr')[1:]:
    #print(row)
    columns = row.find_all('td')
    for i,column in enumerate(columns):
        links = column.find_all('a')
        for link in links:
            print(link)
            print(link['href'])
            print(link.get_text())
            name = link['href']
            full_link = url+ name
            print(full_link)
            if name.split('.')[-1] == 'pdf':
                sections_list[i].append(name)
                #urllib.request.urlretrieve(full_link,name)

print(sections_list)

#Now merge the pdf

merger = PdfFileMerger()

for pdfs in sections_list:
    for pdf in pdfs:
        merger.append(open(pdf, 'rb'))

with open('OS_TEP.pdf', 'wb') as fout:
    merger.write(fout)



