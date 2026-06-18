class CookingAgent:
    
    def __init__(self):
        self.active = False
        self.recipe = None
        self.current_step = 0

    def start_recipe(self, recipe):
        self.active = True
        self.recipe = recipe
        self.current_step = 0

    def next_step(self):
        self.current_step += 1

cooking_agent = CookingAgent()