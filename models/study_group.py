class StudyGroup:
    def __init__(self, name, interests):
        self.name = name
        self.interests = interests

# Sample study groups
study_groups = [
    StudyGroup("Group 1", ["AI", "Machine Learning"]),
    StudyGroup("Group 2", ["Mathematics", "Physics"]),
    StudyGroup("Group 3", ["Literature", "History"])
]

def find_groups_by_interest(interest):
    return [group for group in study_groups if interest.lower() in [i.lower() for i in group.interests]]