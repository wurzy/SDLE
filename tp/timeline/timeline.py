class Timeline: 
    def __init__(self):
        self.timeline = []
    
    def add(self,post):
        self.timeline.append(post)
        
    def print():
        print("TIMELINE ----------------------")
        for post in self.timeline:
            print(f"Node {post.user}: {post.text}")