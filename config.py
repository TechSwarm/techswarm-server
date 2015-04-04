# URL Format: dialect+driver://username:password@host:port/database
# SQLite:     sqlite://<nohostname>/<path>
# See: http://docs.sqlalchemy.org/en/latest/core/engines.html
DATABASE_URL = 'sqlite:///database.db'
DATABASE_SETTINGS = {
    'convert_unicode': True
}
