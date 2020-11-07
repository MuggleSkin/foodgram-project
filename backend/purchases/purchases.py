from django.conf import settings

class Purchases:
    def __init__(self, request):
        self.session = request.session
        purchases = self.session.get(settings.PURCHASES_SESSION_ID)
        if not purchases:
            purchases = {"ids" : [], "count" : 0,}
        self.purchases = purchases

    def get_ids(self):
        return self.purchases["ids"]
    
    def save(self):
        self.session[settings.PURCHASES_SESSION_ID] = self.purchases

    def add(self, recipe):
        if recipe.id not in self.purchases["ids"]:
            self.purchases["ids"].append(recipe.id)
            self.purchases["count"] += 1
            self.save()
            return True
        return False
    
    def remove(self, recipe):
        if recipe.id in self.purchases["ids"]:
            self.purchases["ids"].remove(recipe.id)
            self.purchases["count"] -= 1
            self.save()
            return True
        return False
    
    def clear(self):
        self.purchases = {"ids" : [], "count" : 0,}
        del self.session[settings.PURCHASES_SESSION_ID]
