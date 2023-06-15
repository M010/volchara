import json
from pathlib import Path


COUNT_LINES_FOR_TARGET = 5

# gcovr --json coverage.json
# gcovr --json-summary coverage_sum.json
class CoverageParser:
    def __init__(self, root_dir: str, coverage_targets: str, coverage_files: str):
        self.root_dir = root_dir
        self.coverage_targets = str(Path(root_dir, coverage_targets).absolute())
        self.coverage_files = str(Path(root_dir, coverage_files).absolute())
        
        # our api coverage
        self.data = {"targets":[], "files":[]}

    def createTarget(self, line_number_begin: int, line_number_end: int, file_name: str):
        target = {}
        target["file"] = file_name
        target["target"] = {"count":0, "line_number_begin":0, "line_number_end":0}
        target["target"]["count"] = 0
        target["target"]["line_number_begin"] = line_number_begin
        target["target"]["line_number_end"] = line_number_end
        target["coef"] = {}
        self.data["targets"].append(target)
        
    def process_files(self):
        # get info about targets from coverage.json
        coverage_targets = open(self.coverage_targets)
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
                    self.createTarget(begin, vector_line[i - 1], coverage["file"])
                    begin = val
                    count = 1
                    continue

                if i == len(vector_line) - 1 and count > COUNT_LINES_FOR_TARGET:
                    self.createTarget(begin, val, coverage["file"])


        self.data["targets"] = [target for target in self.data["targets"] 
                                if target["target"]["line_number_end"] - target["target"]["line_number_begin"]
                                > COUNT_LINES_FOR_TARGET]
        for target in self.data["targets"]:
            target["coef"]["score"] = target["target"]["line_number_end"] - target["target"]["line_number_begin"]

        # get info about files from coverage_sum.json
        coverage_files = open(self.coverage_files)
        coverage_json = json.load(coverage_files)

        for coverage in coverage_json["files"]:
            file = {}
            file["name"] = coverage["filename"]
            file["score"] = coverage["line_percent"]
            self.data["files"].append(file)

        return self.data