from scrappy.mixins import UserAccessByRightMixin


class UserOfficeAccessMixin(UserAccessByRightMixin):
    access_page = 'office'