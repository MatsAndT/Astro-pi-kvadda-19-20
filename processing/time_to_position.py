import ephem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

date = ephem.Date('')

class TimeToPosition:
    url = ""

    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--window-size=1280x720')
        
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(self.url)

    def convert(self, time):
        self.search(time)
        lat, lon = self.get_lat_lon()

        if lat == '' or lat == None:
            # TODO: add error for not lat
            return Error
        else:
            if lon == '' or lon == None:
                #TODO: add error for not lon
                return Error
            else:
                return lat, lon

    def search(self, time_text):
        search_form = self.driver.find_element_by_id('historicalDateTime')
        search_form.send_keys(time_text)
        search_form.submit()

    def get_lat_lon(self):
        lat = self.driver.find_element_by_id('latitudeValue').text
        lon = self.driver.find_element_by_id('longitudeValue').text
        return lat, lon

    def quit(self):
        self.driver.quit()
