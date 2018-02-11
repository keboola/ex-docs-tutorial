
import csv
# Load the KBC library to process the config file
from keboola import docker
cfg = docker.Config('/data/')
params = cfg.get_parameters()

print("Hello world from python")

csvlt = '\n'
csvdel = ','
csvquo = '"'
with open('/data/in/tables/source.csv', mode='rt', encoding='utf-8') as in_file, \
        open('/data/out/tables/odd.csv', mode='wt', encoding='utf-8') as odd_file, \
        open('/data/out/tables/even.csv', mode='wt', encoding='utf-8') as even_file:
    lazy_lines = (line.replace('\0', '') for line in in_file)
    reader = csv.DictReader(lazy_lines, lineterminator=csvlt, delimiter=csvdel,
                            quotechar=csvquo)

    odd_writer = csv.DictWriter(odd_file, fieldnames=reader.fieldnames,
                                lineterminator=csvlt, delimiter=csvdel,
                                quotechar=csvquo)
    odd_writer.writeheader()

    even_writer = csv.DictWriter(even_file, fieldnames=reader.fieldnames,
                                 lineterminator=csvlt, delimiter=csvdel,
                                 quotechar=csvquo)
    even_writer.writeheader()
    i = 0
    for row in reader:
        if i % 2 == 0:
            even_writer.writerow(row)
        else:
            newRow = {}
            for key in reader.fieldnames:
                newRow[key] = row[key] + ''.join([params['sound']] * params['repeat'])
            odd_writer.writerow(newRow)
        i = i + 1
