# Librarian/membership_states.py

class MembershipState:
    """Lớp cơ sở (interface) cho các trạng thái thành viên"""
    @property
    def name(self):
        return self.__class__.__name__.replace("State", "")

    @property
    def max_books(self):
        raise NotImplementedError

    @property
    def max_days(self):
        raise NotImplementedError

    @property
    def free_extend(self):
        raise NotImplementedError

    def has_priority(self):
        return False



class BasicState(MembershipState):
    @property
    def max_books(self):
        return 10

    @property
    def max_days(self):
        return 14

    @property
    def free_extend(self):
        return 0


class StandardState(MembershipState):
    @property
    def max_books(self):
        return 20

    @property
    def max_days(self):
        return 30

    @property
    def free_extend(self):
        return 2

    def has_priority(self):
        return True


class PremiumState(MembershipState):
    @property
    def max_books(self):
        return 50

    @property
    def max_days(self):
        return 60

    @property
    def free_extend(self):
        return 5

    def has_priority(self):
        return True
