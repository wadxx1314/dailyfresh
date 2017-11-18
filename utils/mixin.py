from django.contrib.auth.decorators import login_required

#重写父类as_view的方法
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin,cls).as_view(**initkwargs)
        return login_required(view)

