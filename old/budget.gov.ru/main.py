import csv

import requests


def get_page_by_inn(inn):
    params = {
        'blocks': 'info,grbs,rcv,change,plan',
        'filterinn': inn,
        'sortField': 'startdate',
        'sortDir': 'asc',
        'pageNum': '1',
        'pageSize': '1000'
    }
    raw_page = requests.get("http://budget.gov.ru/epbs/registry/grants/data", params=params)
    json = raw_page.json()

    items = []
    for json_item in json["data"]:
        for json_plan in json_item["plans"]:
            items.append({
                "id": json_item["info"]["numAgreem"],
                "date_agree": json_item["info"]["dateAgreem"],
                "start_date": json_item['info']["startDate"],
                "end_date": json_item['info']["endDate"],
                "receiver_full_name": json_item['receiver'][0]['fullName'],
                "receiver_short_name": json_item['receiver'][0]['shortName'],
                "receiver_inn": inn,
                "total_sum": json_item["info"]["sum"],
                "plan_purpose": json_plan["purpose"],
                "plan_sum": json_plan["sumTotal"]
            })

        with open("budget.gov.ru.csv", "a") as outfile:
            f = csv.writer(outfile)
            for item in items:
                f.writerow([
                    unicode(item["id"]).encode("utf-8"),
                    unicode(item["date_agree"]).encode("utf-8"),
                    unicode(item["start_date"]).encode("utf-8"),
                    unicode(item["end_date"]).encode("utf-8"),
                    unicode(item["receiver_full_name"]).encode("utf-8"),
                    unicode(item["receiver_short_name"]).encode("utf-8"),
                    unicode(item["receiver_inn"]).encode("utf-8"),
                    unicode(item["total_sum"]).encode("utf-8"),
                    unicode(item["plan_purpose"]).encode("utf-8"),
                    unicode(item["plan_sum"]).encode("utf-8"),
                ])


if __name__ == "__main__":
    inn_list = [
        "7717039300",
        "7736207543",
        "7901533600",
        "7704676655",
        "7743001840",
        "7805093829",
        "7710703177",
        "7714037217",
        "7737008974",
        "7728547955",
        "7708183322",
        "7724914298",
        "7743002018",
        "7717535281",
        "7730115448",
        "7705056238",
        "9710002513",
        "7743645178",
        "7710045545",
        "7714024842",
        "7703082786",
        "7708093333",
        "7704853840",
        "7712108141",
        "7714072839"
    ]
    for inn in inn_list:
        print inn
        get_page_by_inn(inn)
