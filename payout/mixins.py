from scrappy.mixins import UserAccessByRightMixin


class UserPayoutAccessMixin(UserAccessByRightMixin):
    access_page = 'payout'