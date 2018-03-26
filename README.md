# Geocoding Network Service
In this project, a network service with RESTful HTTP interface has been implemented to resolve the longitude and latitude coordinates for a given address using third party geo-coding services.

Google maps is the primary geo-coding service, while here maps is the secondary service. The code falls back to secondary service when primary service fails to return a result or there is a network error.

## Running the code
Run geocoding_service.py file in 'Geocoding_network_service' folder by typing the following command line arguments

```
=> python Geocoding_network_service/geocoding_service.py
```
Then, we will be prompted to enter the address of the location for which we need longitude and latitude coordinates. For example, if a valid location is entered as follows:

```
=> 503b lonelm ct
```
Ouput is:

```
{'lng': -80.543966, 'lat': 43.4907759}
```
If the entered address is invalid as follows:

```
=> kjegEHFLAHFJLHBEGRBEWH
```
And either of the geocoding services fail to find the longitude and latitude co-oordinates. Then the output returned will be:

```
Location coodinates could not be found, recheck the entered address 
```
