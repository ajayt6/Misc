import requests
from bs4 import BeautifulSoup


class google_search_scrape:

    def __init__(self):
        self.USER_AGENT = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


    def fetch_results(self,search_term, number_results, language_code='en'):
        assert isinstance(search_term, str), 'Search term must be a string'
        assert isinstance(number_results, int), 'Number of results must be an integer'
        escaped_search_term = search_term.replace(' ', '+')

        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results,
                                                                              language_code)
        response = requests.get(google_url, headers=self.USER_AGENT)
        response.raise_for_status()

        return search_term, response.text

    def get_first_result_url(self,search_term, language_code ='en'):
        keyword, html_string = self.fetch_results(search_term, 1, language_code)

        soup = BeautifulSoup(html_string, 'lxml')  # Parse the HTML as a string
        first_result = soup.find("h3")
        first_url = first_result.find("a")['href']
        return first_url

if __name__ == '__main__':
    gss = google_search_scrape()
    print( gss.get_first_result_url('mohanlal imdb') )