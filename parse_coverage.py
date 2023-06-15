import json

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
    target = {}
    target["file"] = coverage["file"]
    target["target"] = {"count":0, "line_number_begin":0, "line_number_end":0}

    flag = 0
    current_line = 0
    prev_line = 0

    for line in coverage["lines"]:
        current_line = line["line_number"]
        if line["count"] == 0:
            flag += 1
        elif flag > COUNT_LINES_FOR_TARGET and line["count"] != 0:
            target["target"]["count"] = 0
            target["target"]["line_number_begin"] = current_line - flag
            target["target"]["line_number_end"] = current_line
            flag = 0
        else:
            prev_line = 
            flag = 0

    if flag > 0:
        target["target"]["count"] = 0
        target["target"]["line_number_begin"] = current_line - flag
        target["target"]["line_number_end"] = current_line

    
    target["coef"] = []
    data["targets"].append(target)


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