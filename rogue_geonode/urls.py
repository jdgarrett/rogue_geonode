from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from geonode.sitemap import LayerSitemap, MapSitemap
import geonode.proxy.urls

# Setup Django Admin
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('geonode',)
}

sitemaps = {
    "layer": LayerSitemap,
    "map": MapSitemap
}

urlpatterns = patterns('',
                       url(r'^$', 'geonode.views.index', {'template': 'site_index.html'}, name='home'),
                       url(r'^help/$', TemplateView.as_view(template_name="help.html"), name='help'),
                       url(r'^developer/$', TemplateView.as_view(template_name="developer.html"), name='developer'),
                       url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),
                       (r'^layers/', include('geonode.layers.urls')),

                       # Map views
                       (r'^maps/', include('geonode.maps.urls')),

                       # MapLoom Urls
                       url(r'^maploom/maps/new', 'geonode.maps.views.new_map', {'template': 'maps/maploom.html'},
                           name='maploom-map-new'),

                       url(r'^maploom/maps/(?P<mapid>\d+)/view', 'geonode.maps.views.map_view',
                           {'template': 'maps/maploom.html'}, name='maploom-map-view'),

                       # Catalogue views
                       (r'^catalogue/', include('geonode.catalogue.urls')),

                       # Search views
                       (r'^search/', include('geonode.search.urls')),

                       # Upload views
                       (r'^upload/', include('geonode.upload.urls')),

                       # GeoServer Helper Views
                       (r'^gs/', include('geonode.geoserver.urls')),

                       # Social views
                       (r"^account/", include("account.urls")),
                       (r'^people/', include('geonode.people.urls')),
                       (r'^avatar/', include('avatar.urls')),
                       (r'^comments/', include('dialogos.urls')),
                       (r'^ratings/', include('agon_ratings.urls')),
                       (r'^activity/', include('actstream.urls')),
                       (r'^announcements/', include('announcements.urls')),
                       # (r'^notifications/', include('notification.urls')),
                       (r'^messages/', include('user_messages.urls')),
                       (r'^social/', include('geonode.social.urls')),

                       # Accounts
                       url(r'^account/ajax_login$', 'geonode.views.ajax_login', name='account_ajax_login'),
                       url(r'^account/ajax_lookup$', 'geonode.views.ajax_lookup', name='account_ajax_lookup'),
                       url(r'^security/permissions/(?P<type>[^/]*)/(?P<resource_id>\d+)$',
                           'geonode.security.views.resource_permissions', name='resource_permissions'),

                       # Meta
                       url(r'^lang\.js$', TemplateView.as_view(template_name="lang.js"), name='lang'),
                       url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, name='jscat'),
                       url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
                           {'sitemaps': sitemaps}, name='sitemap'),

                       (r'^i18n/', include('django.conf.urls.i18n')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^file-service/', include('rogue_geonode.file_service.urls')),
                       (r'^proxy/', 'rogue_geonode.views.proxy'),
                       (r'^groups/', include('geonode.contrib.groups.urls')),)

# Documents views
if 'geonode.documents' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', (r'^documents/', include('geonode.documents.urls')),)

urlpatterns += geonode.proxy.urls.urlpatterns

# Serve static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
