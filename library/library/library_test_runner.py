from django.conf import settings
from mongoengine import connect, disconnect
from django.test.runner import DiscoverRunner


class LibraryMixinRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        disconnect()
        connect('test', host='mongomock://localhost')
        return super().setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        disconnect()
        connect(settings.DB_NAME, host=settings.MONGO_DATABASE_HOST)
        super().teardown_databases(old_config, **kwargs)
