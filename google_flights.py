from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import traceback
import datetime

weekday = [
    'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' 
]

month = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

xpath = {
    'trip_type': '//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[1]/div[1]/dropdown-menu/div/div[1]',
    'one_way': '//*[@id="flt-app"]/div[2]/main[4]/div[2]/div/div[1]/div[1]/div[1]/dropdown-menu/div/div[2]/menu-item[2]',
    'round_trip': '//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[1]/div[1]/dropdown-menu/div/div[2]/menu-item[1]',
    'passenger': '//*[@id="flt-pax-button"]/span',
    'adult_plus': '//*[@id="flt-modaldialog"]/div/div/div[1]/div/div[3]',
    'child_plus': '//*[@id="flt-modaldialog"]/div/div/div[2]/div/div[3]',
    'pass_done': '//*[@id="flt-modaldialog"]/div/div/div[5]/div[1]',
    'from_form': '//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[1]',
    'from_field': '//*[@id="sb_ifc50"]/input',
    'to_form': '//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[2]',
    'to_field': '//*[@id="sb_ifc50"]/input',
    'date': '//*[@id="flt-app"]/div[2]/main[4]/div[2]/div/div[1]/div[2]/div[4]/div[1]/div[2]',
    'date_from': '//*[@id="flt-modaldialog"]/div/div[4]/div[2]/div[1]/date-input/input',
    'date_to': '//*[@id="flt-modaldialog"]/div/div[4]/div[2]/div[3]/date-input/input',
    'date_done': '//*[@id="flt-modaldialog"]/div/div[5]/g-raised-button',
    'date_rst': '//*[@id="flt-modaldialog"]/div/div[4]/div[1]/text-button',
    'search': '//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[4]/floating-action-button',
    'cheapest': '//*[@id="flt-app"]/div[2]/main[4]/div[7]/div[1]/div[6]/div[3]/div[1]/div[1]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]/div[6]/div[1]',
    'sort': '//*[@id="flt-app"]/div[2]/main[4]/div[7]/div[1]/div[6]/div[1]/div/div',
    'sort_price': '//*[@id="flt-app"]/div[2]/main[4]/div[7]/div[1]/div[6]/div[1]/div/div/dropdown-menu/div/div[2]/menu-item[2]/span'
}

class GoogleFlights():
    """
    Class providing access to google flights
    """
    def __init__(self, orig, dest, trip_type='round_trip', adults=1, children=0):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.google.com/flights')
        self._set_trip_type(trip_type)
        self._set_origin(orig)
        self._set_destination(dest)
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['search']))).click() 
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['sort']))).click()
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['sort_price']))).click()
        #self._set_passenger_count(adults, children)

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass

    def _click(self, form):
        self.driver.execute_script("arguments[0].click();", form)

    def _set_trip_type(self, trip_type):
        """
        set the trip type [one_way, round_trip]
        """
        self._click(WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['trip_type']))))
        if trip_type == 'round_trip':
            self._click(WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['round_trip']))))
        elif trip_type == 'one_way':
            self._click(WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['one_way']))))
        else:
            raise Exception('invalid trip type ' + trip_type)

    def _set_passenger_count(self, adults, children):
        """
        setting passenger count (adults, children)
        """
        self._click(WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['passenger']))))
        # set adult count
        if adults:
            adult_plus = WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['adult_plus'])))
            for _ in range(adults - 1):
                self._click(adult_plus)
        else:
            raise Exception('adults count must be more than 0')
        # set children count
        if children:
            child_plus = WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['child_plus'])))
            for _ in range(children):
                self._click(child_plus)
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['pass_done']))).click()

    def _set_date(self, from_date, to_date):
        """
        setting the date range
        """
        if to_date >= from_date:
            self._click(WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['date']))))
            self._click(WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['date_rst']))))
            date_from = WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['date_from'])))
            date_from.click()
            start_date = weekday[from_date.weekday()] + ', ' + str(from_date.day) + ' ' + month[from_date.month - 1]
            date_from.send_keys(start_date)
            date_from.send_keys(Keys.RETURN)
            date_to = WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['date_to'])))
            date_to.click()
            end_date = weekday[to_date.weekday()] + ', ' + str(to_date.day) + ' ' + month[to_date.month - 1]
            date_to.send_keys(end_date)
            date_to.send_keys(Keys.RETURN)
            self._click(WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['date_done']))))
        else:
            raise Exception('invalid dates')
            print(from_date)
            print(to_date)

    def _set_origin(self, origin):
        if origin:
            WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['from_form']))).click()
            from_field = WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['from_field'])))
            from_field.clear()
            from_field.click()
            from_field.send_keys(origin)
            sleep(0.1)
            from_field.send_keys(Keys.RETURN)
        else:
            raise Exception('invalid origin')

    def _set_destination(self, dest):
        if dest:
            WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['to_form']))).click()
            to_field = WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.XPATH, xpath['to_field'])))
            to_field.clear()
            to_field.click()
            to_field.send_keys(dest)
            sleep(0.1)
            to_field.send_keys(Keys.RETURN)
        else:
            raise Exception('invalid destination')

    def get_cheapest_price(self, from_date, to_date):
        current_price = WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, xpath['cheapest']))).text
        self._set_date(from_date, to_date)
        while current_price == WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, xpath['cheapest']))).text:
            sleep(0.1)
        cheapest = WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, xpath['cheapest'])))
        if cheapest.text.startswith('$'):
            return int(cheapest.text[1:].replace(',', ''))
        else:
            raise Exception('no flights found')

