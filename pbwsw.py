import requests
import json
import datetime


class pbwsw:
    def __init__(self):
        self.applicationKey = 'NyxJn076zjp2Kvmh'
        self.sessionToken = []
        self.loginToBetfair()
        self.standardHeader = {'X-Application': self.applicationKey, 'X-Authentication': self.sessionToken,
                               'content-type': 'application/json'}
        self.betFairEndpoint =  "https://api.betfair.com/exchange/betting/rest/v1.0/"
        self.JSONRPC_url =      "https://api.betfair.com/exchange/betting/json-rpc/v1"

    def loginToBetfair(self):
        payload = 'username=pedmunds&password=cortinathingi5B'
        headers = {'X-Application': self.applicationKey, 'Content-Type': 'application/x-www-form-urlencoded'}

        resp = requests.post('https://identitysso.betfair.com/api/certlogin', data=payload, cert=(
            '/Users/edmunds/Documents/authcertforbetfair/client-2048.crt',
            '/Users/edmunds/Documents/authcertforbetfair/client-2048.key'), headers=headers)

        if resp.status_code == 200:
            resp_json = resp.json()
            # print resp_json['loginStatus']
            # print resp_json['sessionToken']
            self.sessionToken = resp_json['sessionToken']
            return True
        else:
            print "Login failed:"
            print json.dumps(json.loads(resp.text))

            return False

    def getEventsList(self, inPlay):
        url = self.betFairEndpoint + "listEvents/"

        if inPlay:
            inPlayFilter = '"inPlayOnly": true '
        else:
            inPlayFilter = ''

        json_req = '{"filter":{' + inPlayFilter + '}}'
        # json_req = '{"filter":{}}'
        resp = requests.post(url, data=json_req, headers=self.standardHeader)
        # print json.dumps(json.loads(resp.text), indent=3)
        resp_json = resp.json()

        evtList = []

        for listItem in resp_json:
            evt = listItem['event']

            try:
                timezone = evt['timezone']
            except KeyError:
                timezone = ''

            try:
                openDate = evt['openDate']
            except KeyError:
                openDate = ''

            try:
                id = evt['id']
            except KeyError:
                id = 0

            try:
                countryCode = evt['countryCode']
            except KeyError:
                countryCode = '  '

            try:
                name = evt['name']
            except KeyError:
                name = ''

            ev = event(id, timezone, openDate, countryCode, name)
            # ev.printSelf()

            evtList.append(ev)

        return evtList

    def getMarketCatalogueList(self, compID):
        url = self.betFairEndpoint + "listMarketCatalogue/"

        eventIDsFilter = '"competitionID": ' + '["' + str(compID) + '"]'

        json_req = '{"filter":{' + eventIDsFilter + '}}'
        # json_req = '{"filter":{}}'
        resp = requests.post(url, data=json_req, headers=self.standardHeader)
        # print json.dumps(json.loads(resp.text), indent=3)
        resp_json = resp.json()
        print json.dumps(json.loads(resp.text), indent=3)

    def getCompetitions(self):
        url = self.betFairEndpoint + "listCompetitions/"

        json_req = '{"filter":{}}'
        resp = requests.post(url, data=json_req, headers=self.standardHeader)
        # print json.dumps(json.loads(resp.text), indent=3)
        resp_json = resp.json()
        print json.dumps(json.loads(resp.text), indent=3)

    def getMarkets(self, eventTypeID):
        url = self.betFairEndpoint + "listMarketCatalogue/"
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        # json_req = '{"filter":{"eventTypeIds":["' + eventTypeID + '"],"inPlayOnly": true,"sort":"FIRST_TO_START","maxResults":"10","marketProjection":["COMPETITION", "EVENT", "EVENT_TYPE", "RUNNER_DESCRIPTION", "RUNNER_METADATA", "MARKET_START_TIME"]}'
        # "marketStartTime":{"from":"' + now + '"}},
        json_req = '{"filter":{"eventTypeIds":["' + eventTypeID + '"],"marketCountries":["GB"], "marketStartTime":{"from":"' + now + '"}}, "inPlayOnly": true, "marketTypeCodes":"DRAW", "sort":"FIRST_TO_START","maxResults":"200","marketProjection":["COMPETITION", "EVENT", "EVENT_TYPE", "RUNNER_DESCRIPTION", "RUNNER_METADATA"]}'
        # json_req = '{"params": {"filter":{"eventTypeIds":["' + eventTypeID + '"],"marketCountries":["GB"],"marketTypeCodes":["WIN"],"marketStartTime":{"from":"' + now + '"}},"sort":"FIRST_TO_START","maxResults":"1","marketProjection":["RUNNER_METADATA"]}, "id": 1}'
        resp = requests.post(url, data=json_req, headers=self.standardHeader)
        resp_json = resp.json()
        print json.dumps(json.loads(resp.text), indent=3)

# , "1.107702438"
#, "priceProjection" : ["EX_BEST_OFFERS"] },
# , "id": 1

    def getPrices(self):
        jsonrpc_req='{"jsonrpc": "2.0", ' \
            '"method": "SportsAPING/v1.0/listMarketBook", ' \
            '"params": {"marketIds" : ["1.119306828"], "priceProjection":{"priceData":["EX_BEST_OFFERS"]}}, ' \
            '"id": 1}'

        response = requests.post(self.JSONRPC_url, data=jsonrpc_req, headers=self.standardHeader)

        print json.dumps(json.loads(response.text), indent=3)

class event:
    def __init__(self, id, timezone, openDate, countryCode, name):
        self.id = id
        self.timezone = timezone
        self.openDate = openDate
        self.countryCode = countryCode
        self.name = name

    def dbSave(self):
        self.printSelf()

    def __repr__(self):
        return ('id:' + str(self.id) + ' date: ' + str(
            self.openDate) + ' country:' + self.countryCode + ' name:' + self.name + ' Time Zone: ' + str(
            self.timezone) + '\n')
