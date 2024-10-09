class Student:
    def __init__(self, name, script, feedback=""):
        self.name = name
        self.script = script
        self.feedback = feedback

    def get_name(self):
        conjunctions = ["da", "de", "do", "das", "dos", "e"]

        name_parts = self.name.lower().split()

        formatted_name = [
            part.capitalize() if part not in conjunctions else part
            for part in name_parts
        ]
        
        return " ".join(formatted_name)
    
    def __str__(self):
        return f"Student(name={self.name}, script={self.script}, feedback={self.feedback})"