csv.field_size_limit(sys.maxsize)

with open(main_file, "r") as fp:
    root = csv.reader(fp, delimiter='\t', quotechar='"')
    result = collections.defaultdict(list)
    next(root)
    for row in root:
        year = row[0].split("-")[0]
        result[year].append(row)

for i,j in result.items():
    row_count = sum(1 for row in j)
    print(row_count)
    file_path = "C:\Users\ArulSamy\Downloads\COVID-19.csv"%(src_path, i, row_count)
    with open(file_path, 'w') as fp:
            writer = csv.writer(fp, delimiter='\t', quotechar='"')
            writer.writerows(j)