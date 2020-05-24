import ephem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

date = ephem.Date('')

class TimeToLatLon:
    url = "http://www.isstracker.com/historical"

    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--window-size=1280x720')
        
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(self.url)

    def convert(self, time):
        '''
        Converts time to the position of the iss, in lat and lon
        '''
        if time is None or time is "" or time is not str:
            raise ValueError('Time is required and must be a string')

        self.search(time)
        lat, lon = self.get_lat_lon()

        if lat is '' or lat is None:
            raise SyntaxError('Did not find latitudeValue, is the time correct?')

        if lon is '' or lon is None:
            raise SyntaxError('Did not find longitudeValue, is the time correct?')

        return lat, lon

    def search(self, time_text):
        '''
        Search for the time we are looking for 
        '''
        search_form = self.driver.find_element_by_id('historicalDateTime')
        search_form.clear()
        search_form.send_keys(time_text)
        self.driver.find_element_by_id('submitLookup').click()

    def get_lat_lon(self):
        '''
        Gets lat and lon from the html
        '''
        lat = self.driver.find_element_by_id('latitudeValue').text
        lon = self.driver.find_element_by_id('longitudeValue').text
        return lat, lon

    def quit(self):
        self.driver.quit()
