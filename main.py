import csv
# Load the KBC library to process the config file
from keboola import docker


# produce some test output
print("Hello world from python")

# read configuration parameters
cfg = docker.Config('/data/')
params = cfg.get_parameters()

# set CSV format
csvlt = '\n'
csvdel = ','
csvquo = '"'

# open one input file and two output files
with open('/data/in/tables/source.csv', mode='rt', encoding='utf-8') as in_file, \
     open('/data/out/tables/odd.csv', mode='wt', encoding='utf-8') as odd_file, \
     open('/data/out/tables/even.csv', mode='wt', encoding='utf-8') as even_file:
    # fix possibly null characters in the input file
    # https://stackoverflow.com/questions/4166070/python-csv-error-line-contains-null-byte
    lazy_lines = (line.replace('\0', '') for line in in_file)

    # initialize CSV reader
    reader = csv.DictReader(lazy_lines, lineterminator=csvlt, delimiter=csvdel,
                            quotechar=csvquo)

    # initialize CSV writers
    odd_writer = csv.DictWriter(odd_file, fieldnames=reader.fieldnames,
                                lineterminator=csvlt, delimiter=csvdel,
                                quotechar=csvquo)
    odd_writer.writeheader()
    even_writer = csv.DictWriter(even_file, fieldnames=reader.fieldnames,
                                 lineterminator=csvlt, delimiter=csvdel,
                                 quotechar=csvquo)
    even_writer.writeheader()

    # loop over all rows of the input file
    i = 0
    for row in reader:
        if i % 2 == 0:
            # write even rows
            even_writer.writerow(row)
        else:
            # write odd rows
            newRow = {}

            # loop over all columns of the row
            for key in reader.fieldnames:
                # add the defined sounds a defined number of times
                newRow[key] = row[key] + ''.join([params['sound']] *
                                                 params['repeat'])
            odd_writer.writerow(newRow)
        i = i + 1
