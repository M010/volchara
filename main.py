import json
from typing import List

max_score = 100

class File:
    def __init__(self, name: str, score: int):
        self.name = name
        self.score = score
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
        
    @staticmethod
    def from_json(json_data):
        return File(name=json_data["name"], score=json_data["score"])

class Files:
    def __init__(self, files: List[File]):
        self.files = files
        
    def get_file_with_name(self, name: str):
        for file in self.files:
            if file.name == name:
                return file        
        raise Exception(f"File with name {name} not found")
    
    def sort_by_score(self):
        self.files = sorted(self.files, key=lambda file: file.score, reverse=True) 
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
    
    @staticmethod
    def from_json(json_data):
        files = []
        for file in json_data["files"]:
            files.append(File.from_json(file))
        return Files(files=files)

def get_coverage_data():
    return {
        'files': [
            {
                "name":"main.cpp", 
                "score": 100
            },
            {
                "name":"main2.cpp", 
                "score": 50
            }
        ]
    }

def get_git_data():
    return {
        'files': [
            {
                "name":"main.cpp", 
                "score": 20
            },
            {
                "name":"main2.cpp", 
                "score": 10
            }
        ]
    }
    
def merge(git_files: Files, coverage_files: Files) -> Files:
    output = []
    for git_file in git_files.files:
        try:
            coverage_file = coverage_files.get_file_with_name(git_file.name)
        except Exception as e:
            print(f"Warn: file found in git but coverage missing. {e}")
            # If coverage not found assume no coverage at all
            # so, file should be surely checked
            coverage_file = File(name=git_file.name, score=max_score)
        output.append(File(name=git_file.name, score=git_file.score + coverage_file.score))
    return Files(files=output)

def main():
    coverage = Files.from_json(get_coverage_data())
    git = Files.from_json(get_git_data())
    
    total = merge(git, coverage)
    total.sort_by_score()
    print(total.toJson())
    

if __name__ == "__main__":
    main()