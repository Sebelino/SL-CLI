SL-CLI
======

Stockholms Lokaltrafik - Command Line Interface

# Installation
1. Döp om *sensitive.example.xml* till *sensitive.xml*.
2. Öppna *sensitive.xml* och byt ut de fejkade API-nycklarna mot riktiga nycklar. Har du inga
   nycklar kan du skaffa dem på *www.trafiklab.se*.

# API-moduler
Exempel på direkt använding av API-modulen *sl-platsuppslag*:
```bash
$ ./keyreader.py sl-platsuppslag | xargs ./sl-platsuppslag.py vårsta
Requesting URL: https://api.sl.se/api2/typeahead.json?stationsonly=True&searchstring=v%C3%A5rsta&maxresults=10&key=828a153284f5464f971e9362cbc36ba9
{u'ExecutionTime': 6, u'ResponseData': [{u'Y': u'59165264', u'Type': u'Station', u'SiteId': u'7305', u'Name': u'V\xc3\xa5rsta centrum (Botkyrka)', u'X': u'17797365'}, {u'Y': u'59626105', u'Type': u'Station', u'SiteId': u'5018', u'Name': u'M\xc3\xa4rsta v\xc3\xa5rdcentral (Sigtuna)', u'X': u'17858123'}, {u'Y': u'59273602', u'Type': u'Station', u'SiteId': u'9286', u'Name': u'V\xc3\xa5rberg (Stockholm)', u'X': u'17887931'}, {u'Y': u'59275867', u'Type': u'Station', u'SiteId': u'1796', u'Name': u'V\xc3\xa5rbergs centrum (Stockholm)', u'X': u'17886592'}, {u'Y': u'59263516', u'Type': u'Station', u'SiteId': u'9285', u'Name': u'V\xc3\xa5rby g\xc3\xa5rd (Huddinge)', u'X': u'17886520'}, {u'Y': u'59271328', u'Type': u'Station', u'SiteId': u'1689', u'Name': u'V\xc3\xa5rberg (p\xc3\xa5 Svanholmsv\xc3\xa4gen)  (Stockholm)', u'X': u'17889261'}, {u'Y': u'59219829', u'Type': u'Station', u'SiteId': u'7470', u'Name': u'V\xc3\xa5rbov\xc3\xa4gen (S\xc3\xb6dert\xc3\xa4lje)', u'X': u'17636197'}, {u'Y': u'59261521', u'Type': u'Station', u'SiteId': u'7139', u'Name': u'V\xc3\xa5rby brygga (Huddinge)', u'X': u'17878663'}, {u'Y': u'59256999', u'Type': u'Station', u'SiteId': u'7122', u'Name': u'V\xc3\xa5rby k\xc3\xa4lla (Huddinge)', u'X': u'17880883'}, {u'Y': u'59165264', u'Type': u'Station', u'SiteId': u'7305', u'Name': u'V\xc3\x85RC', u'X': u'17797365'}], u'Message': None, u'StatusCode': 0}
```
