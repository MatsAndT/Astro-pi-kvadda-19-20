import ephem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

date = ephem.Date('')

class TimeToPosition:
    url = "http://www.isstracker.com/historical"

    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--window-size=1280x720')
        
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(self.url)

    def convert(self, time):
        if time == None or time == "" or time != str:
            raise ValueError('Time is required and must be a string')

        self.search(time)
        lat, lon = self.get_lat_lon()

        if lat == '' or lat == None:
            raise SyntaxError('Did not find latitudeValue, is the time correct?') 
        else:
            if lon == '' or lon == None:
                raise SyntaxError('Did not find longitudeValue, is the time correct?')
            else:
                return lat, lon

    def search(self, time_text):
        search_form = self.driver.find_element_by_id('historicalDateTime')
        search_form.clear()
        search_form.send_keys(time_text)
        self.driver.find_element_by_id('submitLookup').click()

    def get_lat_lon(self):
        lat = self.driver.find_element_by_id('latitudeValue').text
        lon = self.driver.find_element_by_id('longitudeValue').text
        return lat, lon

    def quit(self):
        self.driver.quit()
