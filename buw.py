import requests
from bs4 import BeautifulSoup


def get_buw():
    """
    Scrape data about number of people in the library, date and opening hours.
    """
    url = "https://www.buw.uw.edu.pl/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # find number of people currently in the library
    number_of_people = soup.find("div", {"class": "text-center"})
    time = number_of_people.text.split(". ")[1].strip()
    number_of_people = number_of_people.find("span").text

    # find opening hours
    opening_hours = soup.find("div", {"id": "hours"}).text
    opening_hours_list = opening_hours.split(" - ")
    opening_hour = opening_hours_list[0]
    closing_hour = opening_hours_list[1]

    # find date
    date = soup.find("div", {"id": "open-hours"})
    date = date.find(string=True, recursive=False)

    return number_of_people, time, date, opening_hour, closing_hour
