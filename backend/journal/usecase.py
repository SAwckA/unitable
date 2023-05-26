from users.schema import User, UserRoleEnum
from journal.schema import Journal


class JournalAccessPolicies:

    @staticmethod
    def owner_only(user: User, journal: Journal) -> bool:
        if journal.owner_id == user.id or user.role == UserRoleEnum.admin:
            return True
        return False
