
# coding: utf-8

# In[4]:


import json
import urllib.request
import urllib.parse
from IPython.core.debugger import Tracer


# In[5]:


class HttpInterface:
    # Connect to given geocoding service
    # Fetch data
    def get_url(self, host, path, parameters):
        URL = '{0}{1}?{2}'.format(host, path, self.encode_parameters(parameters))
        try:
            request_handler = self.execute_get(URL)
        # Raise exception in case of an error
        except urllib.request.URLError as e:
            return False
        else:
            return request_handler
    
    # Execute get request
    def execute_get(self, url):
        return urllib.request.urlopen(url)

    # Encode parameters to construct URL
    def encode_parameters(self, parameters):
        return urllib.parse.urlencode(parameters)
    
class GetLatLong:
    # Intialize current instance of the class
    def __init__(self, http_interface):        
        self.http_interface = http_interface

    # Perform primary geocoding using google service, if it fails code falls back to here service
    def getCoords(self, address):
        google_service = GoogleService( address, self.http_interface)
        here_service = HereService(address, self.http_interface)        
        Coords = google_service.getCoords()        
        if Coords == False:
            Coords = here_service.getCoords()
        return Coords
        
class HereService():
    # Host and path names of here service
    HOST = 'https://geocoder.cit.api.here.com'
    PATH = '/6.2/geocode.json'

    # Intialize current instance of the class
    def __init__(self, address, http_interface):
        self.address = address
        self.http_interface = http_interface

    # get longitude and latitude co-ordinates, return false if this network service fails or doesn't return output    
    def getCoords(self):
        output = self.execute_request()
        if output is False:
            return False
        coordinates = self.drawCoord(output)
        if coordinates is False:
            return False        
        return coordinates

    # Execute request
    def execute_request(self):
        output = self.http_interface.get_url(self.HOST, self.PATH, self.parameters())
        if output is False:
            return False
        elif output.getcode() is 200:
            return output
        else:
            return False
    
    # Parameters required for performing here request. app_id and app_code are left open to have a working code
    def parameters(self):
        return {
            "searchtext": self.address,
            "app_id": "QyTrpK1enRZhJ2uxT5Ew",
            "app_code": "noqvr4goz4IoBVUek111aQ"
        }

    # Draw out the co-odinates from the json output of here service request
    def drawCoord(self, output):
        data = json.loads(output.read().decode('utf-8'))
        if len(data['Response']['View']) is not 0:
            coordinates = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']        
            return {
                'latitude': coordinates['Latitude'],
                'longitude': coordinates['Longitude']
            }
        else:
            return False

class GoogleService():
    # Host and path names of here service
    HOST = 'https://maps.googleapis.com'
    PATH = '/maps/api/geocode/json'

    # Intialize current instance of the class
    def __init__(self, address, http_interface):
        self.address = address
        self.http_interface = http_interface

    # get longitude and latitude co-ordinates, return false if this network service fails or doesn't return output 
    def getCoords(self):
        output = self.execute_request()
        if output is False:
            return False
        coordinates = self.drawCoord(output)
        return coordinates

    # Execute request
    def execute_request(self):
        output = self.http_interface.get_url(self.HOST, self.PATH, self.parameters())
        if output is False:
            return False
        elif  output.getcode() is 200:
            return output
        else:
            return False
    
     # Parameters required for performing here request. app_id and app_code are left open to have a working code
    def parameters(self):
        return {
            "address": self.address
        }

    # Draw out the co-odinates from the json output of google service request
    def drawCoord(self, output):
        data = json.loads(output.read().decode('utf-8'))
        if len(data['results']) is not 0:
            return data['results'][0]['geometry']['location']
        else:
            return False
 


# In[6]:


http_interface = HttpInterface()                                    
latlong = GetLatLong(http_interface)
add = input("Provide address of the location to geocode: ")
coordinates = latlong.getCoords(add)
if coordinates is False:
    print("Location coodinates could not be found, recheck the address entered ")
else:
    print(coordinates)

