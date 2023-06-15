import json
from typing import List

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