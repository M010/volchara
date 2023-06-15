import json

def createTarget(line_number_begin: int, line_number_end: int, file_name: str, data):
    target = {}
    target["file"] = file_name
    target["target"] = {"count":0, "line_number_begin":0, "line_number_end":0}
    target["target"]["count"] = 0
    target["target"]["line_number_begin"] = line_number_begin
    target["target"]["line_number_end"] = line_number_end
    target["coef"] = {}
    data["targets"].append(target)

# start 
# gcovr --json coverage.json
# gcovr --json-summary coverage_sum.json

COUNT_LINES_FOR_TARGET = 5

# our api coverage
data = {"targets":[], "files":[]}


# get info about targets from coverage.json
coverage_targets = open("coverage.json")
coverage_json = json.load(coverage_targets)

for coverage in coverage_json["files"]:
    vector_line = []
    for line in coverage["lines"]:
        if line["count"] == 0:
            vector_line.append(line["line_number"])

    for i, val in enumerate(vector_line):
        if i == 0:
            count = 1
            begin = val
            continue

        if val - count == begin:
            count += 1
        else:
            createTarget(begin, vector_line[i - 1], coverage["file"], data)
            begin = val
            count = 1
            continue

        if i == len(vector_line) - 1 and count > COUNT_LINES_FOR_TARGET:
            createTarget(begin, val, coverage["file"], data)


data["targets"] = [target for target in data["targets"] if target["target"]["line_number_end"] - target["target"]["line_number_begin"] > COUNT_LINES_FOR_TARGET]
for target in data["targets"]:
    target["coef"]["score"] = target["target"]["line_number_end"] - target["target"]["line_number_begin"]




# get info about files from coverage_sum.json
coverage_files = open("coverage_sum.json")
coverage_json = json.load(coverage_files)

for coverage in coverage_json["files"]:
    file = {}
    file["name"] = coverage["filename"]
    file["score"] = coverage["line_percent"]
    data["files"].append(file)


# For Nikita Grebnev
with open('volchar_test.json', 'w') as outfile:
    json.dump(data, outfile)