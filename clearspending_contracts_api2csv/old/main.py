import csv

import requests

okdp_list = [
    # "92.20.11.110",
    # "92.20.11.111",
    # "92.20.11.112",
    # "92.20.11.120",
    # "92.20.11.121",
    # "92.20.11.122",
    # "92.20.11.130",
    # "92.20.11.131",
    # "92.20.11.132",
    # "92.20.11.140",
    # "92.20.11.141",
    # "92.20.11.142",
    # "92.20.11.190",
    # "92.20.11.191",
    # "92.20.11.192",
    # "92.20.12.110",
    # "92.20.12.111",
    # "92.20.12.112",
    # "92.20.12.120",
    # "92.20.12.121",
    # "92.20.12.122",
    # "92.20.12.130",
    # "92.20.12.131",
    # "92.20.12.132",
    # "92.20.12.140",
    # "92.20.12.141",
    # "92.20.12.142",
    # "92.20.12.190",
    # "92.20.12.191",
    "92.20.12.192",
    "22.12.11.110",
    "22.12.11.120",
    "22.12.11.190",
    "22.12.11.210",
    "22.12.12.110",
    "22.12.12.111",
    "22.12.12.112",
    "22.12.12.113",
    "22.12.12.114",
    "22.12.12.115",
    "22.12.12.116",
    "22.12.12.117",
    "22.12.12.119",
    "22.12.12.120",
    "22.12.12.190",
    "22.12.21.110",
    "22.12.21.120",
    "22.12.21.190",
    "22.12.22.110",
    "22.12.22.120",
    "22.12.22.190",
    "22.12.99.000",
    "22.13.11.110",
    "22.13.11.111",
    "22.13.11.112",
    "22.13.11.113",
    "22.13.11.114",
    "22.13.11.115",
    "22.13.11.116",
    "22.13.11.117",
    "22.13.11.118",
    "22.13.11.119",
    "22.13.11.120",
    "22.13.11.121",
    "22.13.11.122",
    "22.13.11.123",
    "22.13.11.124",
    "22.13.11.125",
    "22.13.11.126",
    "22.13.11.129",
    "22.13.11.190",
    "22.13.11.210",
    "22.13.12.110",
    "22.13.12.111",
    "22.13.12.112",
    "22.13.12.113",
    "22.13.12.114",
    "22.13.12.115",
    "22.13.12.116",
    "22.13.12.117",
    "22.13.12.118",
    "22.13.12.119",
    "22.13.12.120",
    "22.13.12.121",
    "22.13.12.122",
    "22.13.12.123",
    "22.13.12.124",
    "22.13.12.125",
    "22.13.12.126",
    "22.13.12.129",
    "22.13.12.190",
    "22.13.21.110",
    "22.13.21.120",
    "22.13.21.190",
    "22.13.22.110",
    "22.13.22.120",
    "22.13.22.190",
    "22.13.99.000"
]

def get_contracts_by_okdp(okdp):
    print "start okdp", okdp
    params = {
        "okdp_okpd": okdp,
        "daterange": "01.01.2014-31.12.2015"
    }
    raw_json = requests.get("http://openapi.clearspending.ru/restapi/v3/contracts/search/", params=params)
    if raw_json.text == "Invalid request.":
        print "okdp", okdp, "Invalid request."
        return []
    if raw_json.text == "Data not found.":
        print "okdp", okdp, "Data not found."
        return []
    json = raw_json.json()
    total = json["contracts"]["total"]
    print "total:", total
    if total < 500:
        return get_pages_ordinary(params)
    else:
        print "okdp", okdp, "has more than 500 contracts!"
        all = []
        params["pricerange"] = "0-200000"
        all.extend(get_pages_ordinary(params))
        params["pricerange"] = "200000-350000"
        all.extend(get_pages_ordinary(params))
        params["pricerange"] = "350000-500000"
        all.extend(get_pages_ordinary(params))
        params["pricerange"] = "500000-1000000"
        all.extend(get_pages_ordinary(params))
        params["pricerange"] = "1000000-3000000"
        all.extend(get_pages_ordinary(params))
        params["pricerange"] = "3000000-5000000"
        all.extend(get_pages_ordinary(params))
        params["pricerange"] = "5000000-10000000000"
        all.extend(get_pages_ordinary(params))
        return all


def get_pages_ordinary(params):
    params["page"] = 1
    total = requests.get("http://openapi.clearspending.ru/restapi/v3/contracts/search/", params=params).json()["contracts"]["total"]

    pages = []
    for page_num in range(1, total/50 + 2):
        print "\tpage", page_num, "/", total/50 + 1
        params["page"] = page_num
        raw_json = requests.get("http://openapi.clearspending.ru/restapi/v3/contracts/search/", params=params)
        if raw_json.text == "Invalid request.":
            print "okdp", okdp, "; page", page_num, "Invalid request."
            continue
        if raw_json.text == "Data not found.":
            print "okdp", okdp, "; page", page_num, "Data not found."
            continue
        json = raw_json.json()
        pages.append(json["contracts"]["data"])
    return pages

if __name__ == "__main__":
    for okdp in okdp_list:
        contracts = []
        pages = get_contracts_by_okdp(okdp)
        for raw_contracts in pages:
            for raw_contract in raw_contracts:
                contracts.append({
                    "okdp": okdp,
                    "regionCode": raw_contract["regionCode"],
                    "signDate": raw_contract["signDate"],
                    "executionDate": raw_contract["execution"]["year"] + "-" + raw_contract["execution"]["month"] + "-30T00:00:00" if "month" in raw_contract["execution"] else raw_contract["execution"]["endDate"],
                    "price": raw_contract["price"],
                    "supplier_regNum": raw_contract["regNum"],
                    "supplier_inn": raw_contract["suppliers"][0]["inn"] if "inn" in raw_contract["suppliers"][0] else None,
                    "supplier_name": raw_contract["suppliers"][0]["organizationName"].replace("\n", " ").replace("\r", " ") if "organizationName" in raw_contract["suppliers"][0] else None
                })

        with open("test.csv", "a") as outfile:
            f = csv.writer(outfile)
            for contract in contracts:
                f.writerow([
                    unicode(contract["okdp"]).encode("utf-8"),
                    unicode(contract["regionCode"]).encode("utf-8"),
                    unicode(contract["signDate"]).encode("utf-8"),
                    unicode(contract["executionDate"]).encode("utf-8"),
                    unicode(str(contract["price"])).encode("utf-8"),
                    unicode(contract["supplier_regNum"]).encode("utf-8"),
                    unicode(contract["supplier_inn"]).encode("utf-8"),
                    unicode(contract["supplier_name"]).encode("utf-8")
                ])
