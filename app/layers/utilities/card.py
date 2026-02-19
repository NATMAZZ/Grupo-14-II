class Card:
    def __init__(self, name, gender, status, phrases, occupation, image, age=None, user=None, id=None):
        self.name = name
        self.gender = gender
        self.status = status
        self.phrases = phrases
        self.occupation = occupation
        self.image = image
        self.age = age
        self.user = user
        self.id = id

    def __str__(self):
        return 'name: ' + self.name + ', gender: ' + self.gender + ', status: ' + self.status

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        
        same_name = self.name == other.name
        same_gender = self.gender == other.gender
        same_status = self.status == other.status
        same_occupation = self.occupation == other.occupation
        
        return same_name and same_gender and same_status and same_occupation

    def __hash__(self):
        return hash((self.name, self.gender, self.status, self.occupation))