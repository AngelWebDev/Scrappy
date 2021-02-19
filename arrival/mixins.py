from scrappy.mixins import UserAccessByRightMixin


class UserArrivalAccessMixin(UserAccessByRightMixin):
    access_page = 'arrival'
