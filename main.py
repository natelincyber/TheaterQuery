# use selenium for webscraping
# ask for date
# print all movies 
# regex for the url
# access url and print available seats for available showtimes


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


driver = webdriver.Edge()
date = ""
selected_theater = ""

def list_available_theaters():
    driver.get('https://www.cinemark.com/theatres')
    driver.implicitly_wait(2)
    theater_parent = driver.find_element(By.ID, "theaterList")
    theaters = theater_parent.find_elements(By.CLASS_NAME, "theatreBlockLower")
    print("Listing Available Theaters")
    for idx, item in enumerate(theaters):
        span = item.find_element(By.TAG_NAME, "span")
        print(f"[{idx}] {span.text}")
    selection = int(input("Select theater by index: "))
    global selected_theater
    selected_theater = theaters[selection].find_element(By.TAG_NAME, "span").text
    return theaters[selection].find_element(By.CLASS_NAME, "theaterLink").get_attribute("href")

def list_movies(link):

    global date 
    date = input("Input watch date (YYYY-MM-DD):")
    link += f"?showDate={date}"
    driver.get(link)
    driver.implicitly_wait(4)

    movies_parent = driver.find_element(By.ID, "showtimesInner")
    movies = movies_parent.find_elements(By.CLASS_NAME, "showtimeMovieBlock")
    
    print(f"Movies for date {date}:")
    for idx, movie in enumerate(movies):
        name = movie.find_element(By.TAG_NAME, "h3")
        print(f"[{idx}] {name.text}")


    selection = int(input("Select movie by index: "))
    return movies[selection].find_element(By.CLASS_NAME, "movieLink").get_attribute("href")

def get_movie_details(link):
    link += f"?showDate={date}"
    driver.get(link)
    driver.implicitly_wait(4)

    theaters_parent = driver.find_element(By.ID, "theaterList")
    theatres = theaters_parent.find_elements(By.CLASS_NAME, "theatreBlock")
    
    print(f"Showtimes for {selected_theater} on {date}:")
    for item in theatres:
        span = item.find_element(By.TAG_NAME, "span")
        if span.text == selected_theater:
            times_parent = item.find_element(By.CLASS_NAME, "theatreBlockTimes")
            times = times_parent.find_elements(By.CLASS_NAME, "showtime-link")
            for time in times:
                print(time.text)



if __name__ == "__main__":
    theaterLink = list_available_theaters()
    movieLink = list_movies(theaterLink)
    get_movie_details(movieLink)
