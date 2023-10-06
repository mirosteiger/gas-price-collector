import requests
from bs4 import BeautifulSoup
import rumps
from datetime import datetime
import spreadsheet
import webbrowser

# rumps.debug_mode(True)

APP_NAME = "Gas Collector"
URL = "https://www.benzinpreis-aktuell.de/tanken-shell-tankstelle-koeln-50823-f40b.html"
SHEET_URL = "https://docs.google.com/spreadsheets/d/"+spreadsheet.SHEET_ID+"/edit"
REFRESH_INTERVALS = [10, 15, 30, 60, 90]


class TankApp(rumps.App):
    def __init__(self):
        super(TankApp, self).__init__(name=APP_NAME, icon="images/icon.svg")

        self.data = self.get_url_data()

        self.tankstelle = self.get_location_name()
        # self.data.find("div", class_="ksname").text.strip()
        self.price = ""
        self.last_update = ""
        self.interval = REFRESH_INTERVALS[0]
        self.set_up_menu()
        self.refresh_status()

    def get_url_data(self):
        try:
            page = requests.get(URL)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
                results = soup.find_all("div", class_="kachel")[0]
                return results
            else:
                rumps.alert("something went wrong! Error status code")
        except:
            rumps.alert("something went wrong!")

    def get_location_name(self):
        company = self.data.find("h1", class_="kh").text.strip()
        address = self.data.find("p", class_="sap").getText(separator=", ")
        return str(company + " – " + address)

    def get_price(self, url_data):
        if url_data:
            """Format price as currency"""
            price = round(
                float(
                    url_data.find("div", class_="kspreis")
                    .text.strip()
                    .replace(",", ".")
                ),
                2,
            )
            return price
        else:
            return "error"
    
    def get_update_time(self):
        return datetime.now().strftime("%H:%M")

    @rumps.timer(60*30)
    def refresh_status(self, *args, **kwargs):
        data = self.get_url_data()

        self.last_update = self.get_update_time()
        self.menu["updated"].title = "last Update: " + self.last_update + " Uhr"

        self.price = self.get_price(data)
        self.menu["price"].title = "Price: " + str(self.price) + "€"

        """ set price as part of the menu icon """
        self.title = str(self.price) + "€"

        spreadsheet.add(datetime.now().strftime("%d.%m.%Y"), self.last_update, self.price)



    
    @rumps.clicked("Open source in browser")
    def open_source(self, *args, **kwargs):
        webbrowser.open(URL, 2)

    @rumps.clicked("Open data sheet")
    def open_source(self, *args, **kwargs):
        webbrowser.open(SHEET_URL, 2)
        
    def set_up_menu(self):
        self.title = str(self.price) + "€"
        self.menu.add(rumps.MenuItem("Refresh", self.refresh_status))
        self.menu.add("Select Refresh-Interval:")
        self.menu = REFRESH_INTERVALS
        self.menu.add(rumps.separator)
        self.menu.add("updated")
        self.menu.add(rumps.separator)
        # self.menu.add(self.tankstelle)
        self.menu.add("price")
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Open source in browser"))
        self.menu.add(rumps.MenuItem("Open data sheet"))
        self.menu.add(rumps.separator)



if __name__ == "__main__":
    TankApp().run()
