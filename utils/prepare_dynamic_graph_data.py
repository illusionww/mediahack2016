import csv

with open('raw_dynamic.tsv','r') as tsvin, open('dynamic.tsv', 'w') as csvout:
    tsvin = csv.reader(tsvin, delimiter='\t')
    csvout = csv.writer(csvout)

    items = []
    for row in tsvin:
        items.append([row[0], row[1], row[2], "", ""])
        items.append([row[3], "", "", row[4], row[5]])

    for item in items:
        csvout.writerows([item])
