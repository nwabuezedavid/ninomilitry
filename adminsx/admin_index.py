
from django.contrib.admin.sites import AdminSite
from django.utils.translation import gettext_lazy as _

class MilitaryBlogAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = _('Military Blog Admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = _('Military Blog Administration')

    # Text to put at the top of the admin index page.
    index_title = _('Military Blog Management')

    # URL for the "View site" link at the top of each admin page.
    site_url = '/'

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_list = super().get_app_list(request)
        
        # Reorder the apps
        app_dict = {app['app_label']: app for app in app_list}
        
        # Define the order you want
        ordered_apps = ['blog', 'auth', 'sites']
        ordered_app_list = []
        
        # Add the apps in the order you defined
        for app_label in ordered_apps:
            if app_label in app_dict:
                ordered_app_list.append(app_dict[app_label])
                app_dict.pop(app_label)
        
        # Add any remaining apps
        for app in app_dict.values():
            ordered_app_list.append(app)
        
        return ordered_app_list

# Create an instance of the custom admin site
military_blog_admin_site = MilitaryBlogAdminSite(name='military_blog_admin')