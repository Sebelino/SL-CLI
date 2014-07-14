SL-CLI
======

Stockholms Lokaltrafik - Command Line Interface.

# Installation
1. Skapa en kopia av **sensitive.example.xml** som du kallar **sensitive.xml**.
2. Öppna **sensitive.xml** och byt ut de fejkade API-nycklarna mot riktiga nycklar. Har du inga
   nycklar kan du skaffa dem på **trafiklab.se**.

## Dependencies
* xmltodict

# slcli
Med modulen **slcli.py** kan du få reseinformation direkt i terminalen. Se manualen:
```bash
$ ./slcli.py --help
usage: slcli.py [-h] from to at

positional arguments:
  from        Varifrån ska du resa?
  to          Vart ska du?
  at          När ska du bege dig?

optional arguments:
  -h, --help  show this help message and exit
```
Exempel på användning:
```bash
$ ./slcli.py vårsta "tekniska högskolan" 8:00                   
08:08 14.07.14 Vårsta centrum (Botkyrka) - Tekniska högskolan (Stockholm)
08:08....Vårsta centrum
08:09........Malmtorp           
08:10........Bergudden          
08:12........Kassmyra           
08:14........Skäcklinge         
08:15........Skäcklinge gårdsväg
08:17........Lövholmenvägen     
08:18........Toppvägen          
08:19........Hålvägen           
08:20........Passvägen          
08:23....Tumba station
08:33....Tumba
08:37........Tullinge           
08:40........Flemingsberg       
08:43........Huddinge           
08:46........Stuvsta            
08:49........Älvsjö             
08:52........Årstaberg          
08:55........Stockholms södra   
08:59....Stockholms central
09:11....T-Centralen
09:13........Östermalmstorg     
09:15........Stadion            
09:17....Tekniska högskolan
```

# API-moduler
Utöver det användarvänliga slcli.py finns två wrapper-moduler för API:erna SL Reseplanerare
respektive SL Platsuppslag. CLI-argumenten till dessa är samma som de faktiska query-parametrarna;
se **--help** för en beskrivning. Output är JSON.

Exempel på direkt använding av API-modulen **reseplanerare.py** i GNU/Linux:
```bash
$ ./keyreader.py reseplanerare | xargs -I % ./reseplanerare.py 9506 % '9:15' 9526       
{u'HafasResponse': {u'Trip': [{u'SubTrip': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'09:27', u'@type': u'EXACT'}, u'IntermediateStopsQuery': u'https://api.trafiklab.se/sl/reseplanerare/intermediate/le.01426453.1405147882/1/C0-0:0.json', u'ArrivalDate': u'12.07.14', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'10:05', u'@type': u'EXACT'}, u'RTUMessages': {u'RTUMessage': u'Kommande h\xe4ndelse: Pendelt\xe5gen stannar inte i Solna, Ulriksdal och Helenelund sena kv\xe4llar och n\xe4tter 25 juli - 3 augusti pga underh\xe5llsarbete. L\xe4s mer under Aktuellt p\xe5 sl.se'}, u'Transport': {u'Line': u'36', u'Towards': u'S\xf6dert\xe4lje C', u'Type': u'TRN', u'Name': u'pendelt\xe5g 36'}}, u'Summary': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'09:27', u'@type': u'EXACT'}, u'CO2': u'0,0', u'PriceInfo': {u'TariffZones': u'AB', u'TariffRemark': u'tid-biljett'}, u'ArrivalDate': u'12.07.14', u'MT6MessagesExist': u'0', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'RemarksExist': u'0', u'RTUMessagesExist': u'1', u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'10:05', u'@type': u'EXACT'}, u'Duration': u'0:38', u'SubTrips': u'1', u'Changes': u'0'}}, {u'SubTrip': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'09:57', u'@type': u'EXACT'}, u'IntermediateStopsQuery': u'https://api.trafiklab.se/sl/reseplanerare/intermediate/le.01426453.1405147882/1/C0-0:0C0-1:0.json', u'ArrivalDate': u'12.07.14', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'10:35', u'@type': u'EXACT'}, u'RTUMessages': {u'RTUMessage': u'Kommande h\xe4ndelse: Pendelt\xe5gen stannar inte i Solna, Ulriksdal och Helenelund sena kv\xe4llar och n\xe4tter 25 juli - 3 augusti pga underh\xe5llsarbete. L\xe4s mer under Aktuellt p\xe5 sl.se'}, u'Transport': {u'Line': u'36', u'Towards': u'S\xf6dert\xe4lje C', u'Type': u'TRN', u'Name': u'pendelt\xe5g 36'}}, u'Summary': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'09:57', u'@type': u'EXACT'}, u'CO2': u'0,0', u'PriceInfo': {u'TariffZones': u'AB', u'TariffRemark': u'tid-biljett'}, u'ArrivalDate': u'12.07.14', u'MT6MessagesExist': u'0', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'RemarksExist': u'0', u'RTUMessagesExist': u'1', u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'10:35', u'@type': u'EXACT'}, u'Duration': u'0:38', u'SubTrips': u'1', u'Changes': u'0'}}, {u'SubTrip': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'10:27', u'@type': u'EXACT'}, u'IntermediateStopsQuery': u'https://api.trafiklab.se/sl/reseplanerare/intermediate/le.01426453.1405147882/1/C0-0:0C0-1:0C0-2:0.json', u'ArrivalDate': u'12.07.14', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'11:05', u'@type': u'EXACT'}, u'RTUMessages': {u'RTUMessage': u'Kommande h\xe4ndelse: Pendelt\xe5gen stannar inte i Solna, Ulriksdal och Helenelund sena kv\xe4llar och n\xe4tter 25 juli - 3 augusti pga underh\xe5llsarbete. L\xe4s mer under Aktuellt p\xe5 sl.se'}, u'Transport': {u'Line': u'36', u'Towards': u'S\xf6dert\xe4lje C', u'Type': u'TRN', u'Name': u'pendelt\xe5g 36'}}, u'Summary': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'10:27', u'@type': u'EXACT'}, u'CO2': u'0,0', u'PriceInfo': {u'TariffZones': u'AB', u'TariffRemark': u'tid-biljett'}, u'ArrivalDate': u'12.07.14', u'MT6MessagesExist': u'0', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'RemarksExist': u'0', u'RTUMessagesExist': u'1', u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'11:05', u'@type': u'EXACT'}, u'Duration': u'0:38', u'SubTrips': u'1', u'Changes': u'0'}}, {u'SubTrip': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'10:57', u'@type': u'EXACT'}, u'IntermediateStopsQuery': u'https://api.trafiklab.se/sl/reseplanerare/intermediate/le.01426453.1405147882/1/C0-0:0C0-1:0C0-2:0C0-3:0.json', u'ArrivalDate': u'12.07.14', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'11:35', u'@type': u'EXACT'}, u'RTUMessages': {u'RTUMessage': u'Kommande h\xe4ndelse: Pendelt\xe5gen stannar inte i Solna, Ulriksdal och Helenelund sena kv\xe4llar och n\xe4tter 25 juli - 3 augusti pga underh\xe5llsarbete. L\xe4s mer under Aktuellt p\xe5 sl.se'}, u'Transport': {u'Line': u'36', u'Towards': u'S\xf6dert\xe4lje C', u'Type': u'TRN', u'Name': u'pendelt\xe5g 36'}}, u'Summary': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'10:57', u'@type': u'EXACT'}, u'CO2': u'0,0', u'PriceInfo': {u'TariffZones': u'AB', u'TariffRemark': u'tid-biljett'}, u'ArrivalDate': u'12.07.14', u'MT6MessagesExist': u'0', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'RemarksExist': u'0', u'RTUMessagesExist': u'1', u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'11:35', u'@type': u'EXACT'}, u'Duration': u'0:38', u'SubTrips': u'1', u'Changes': u'0'}}, {u'SubTrip': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'11:27', u'@type': u'EXACT'}, u'IntermediateStopsQuery': u'https://api.trafiklab.se/sl/reseplanerare/intermediate/le.01426453.1405147882/1/C0-0:0C0-1:0C0-2:0C0-3:0C0-4:0.json', u'ArrivalDate': u'12.07.14', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'12:05', u'@type': u'EXACT'}, u'RTUMessages': {u'RTUMessage': u'Kommande h\xe4ndelse: Pendelt\xe5gen stannar inte i Solna, Ulriksdal och Helenelund sena kv\xe4llar och n\xe4tter 25 juli - 3 augusti pga underh\xe5llsarbete. L\xe4s mer under Aktuellt p\xe5 sl.se'}, u'Transport': {u'Line': u'36', u'Towards': u'S\xf6dert\xe4lje C', u'Type': u'TRN', u'Name': u'pendelt\xe5g 36'}}, u'Summary': {u'Origin': {u'#text': u'Sollentuna', u'@x': u'17948833', u'@sa': u'200105061', u'@y': u'59428019'}, u'DepartureTime': {u'#text': u'11:27', u'@type': u'EXACT'}, u'CO2': u'0,0', u'PriceInfo': {u'TariffZones': u'AB', u'TariffRemark': u'tid-biljett'}, u'ArrivalDate': u'12.07.14', u'MT6MessagesExist': u'0', u'Destination': {u'#text': u'Flemingsberg', u'@x': u'17947206', u'@sa': u'200105171', u'@y': u'59219047'}, u'RemarksExist': u'0', u'RTUMessagesExist': u'1', u'DepartureDate': u'12.07.14', u'ArrivalTime': {u'#text': u'12:05', u'@type': u'EXACT'}, u'Duration': u'0:38', u'SubTrips': u'1', u'Changes': u'0'}}], u'Trips': u'5', u'Queries': {u'PrevQuery': u'https://api.trafiklab.se/sl/reseplanerare/prev/le.01426453.1405147882/1.json', u'NextQuery': u'https://api.trafiklab.se/sl/reseplanerare/next/le.01426453.1405147882/1.json', u'CurrentQuery': u'https://api.trafiklab.se/sl/reseplanerare/current/le.01426453.1405147882/1.json'}}}
```
där
* **9506** är ID:t för Sollentuna
* **%** är en placeholder för en API-nyckel som **keyreader.py** spottar ut
* **9:15** är tidpunkten för avgång
* **9526** är ID:t för Flemingsberg

