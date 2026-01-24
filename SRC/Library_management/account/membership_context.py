# Librarian/membership_context.py
from .membership_states import BasicState, StandardState, PremiumState

class MembershipContext:
    def __init__(self, level):
        if level == "basic":
            self.state = BasicState()
        elif level == "standard":
            self.state = StandardState()
        elif level == "premium":
            self.state = PremiumState()
        else:
            self.state = BasicState() 

    def get_info(self):
        return {
            "max_books": self.state.max_books,
            "max_days": self.state.max_days,
            "free_extend": self.state.free_extend,
            "priority": self.state.has_priority(),
        }
