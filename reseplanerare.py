#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from api import API,cli

api = API(r'https://api.trafiklab.se/sl/reseplanerare.json',{
    'key' : {'required':True,'description':"Din API-nyckel."},
    's' : {'required':True,'description':"Namn eller ID för startpunkten."},
    'z' : {'required':True,'domain':bool,'description':"Namn eller ID för destinationen."},
    'time' : {'required':True,'domain':str,'description':"Tidpunkt."},
    'timesel' : {'required':False,'domain':set(["arrive","depart"]),'default':"depart",'description':"Betecknar tidpunkten ankomst eller avgång?"},
    'lang' : {'required':False,'domain':set(["sv","en"]),'default':"sv",'description':"Språket som resultaten presenteras i."},
})

if __name__ == '__main__':
    cli(api)

