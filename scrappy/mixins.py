from django.urls import reverse
from django.shortcuts import redirect
from office.models import Rights


class UserAccessByRightMixin(object):
    access_page = ""

    def __init__(self):
        self.access_page = self.access_page.capitalize()

    @staticmethod
    def user_rights(user):
        rights = list(Rights.objects.filter(user=user).values_list("right", flat=True))
        return rights

    def get_redirect_url(self, user):
        redirect_page = ""
        rights = self.user_rights(user)
        right_for_access_page = self.access_page

        if right_for_access_page in rights:
            redirect_page = right_for_access_page
        else:
            possible_pages = ['Office', 'Payout', 'Arrival']
            for page in possible_pages:
                if page != self.access_page and page in rights:
                    redirect_page = page
                    break
        if redirect_page != "":
            redirect_url = reverse("{}_view".format(redirect_page.lower()))
        else:
            redirect_url = "/"
        return redirect_url

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin or self.access_page in self.user_rights(request.user):
            return super(UserAccessByRightMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(self.get_redirect_url(request.user))
