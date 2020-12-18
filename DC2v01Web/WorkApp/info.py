from MainApp.models import Profile


def info(username):
    try:
        profile = Profile.objects.get(user__username=username)
        active_order = profile.active_order
        active_project = profile.active_project
        active_device = active_project.device
        print(profile)
        print(active_order)
        print(active_project)
        print(active_device)
    except Exception:
        return False
