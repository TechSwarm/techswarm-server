import sys
import tsserver

print("Creating database...", file=sys.stderr)
print("Database URL: %s" % tsserver.db.engine.url, file=sys.stderr)
tsserver.db.create_all()

print("Everything is done!", file=sys.stderr)
