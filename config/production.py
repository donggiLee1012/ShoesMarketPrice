from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'mkpf.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xd5\x13\xdb\x8d\x81\xf6\xb8\xfa\x97\x8e\xcbYtHDs'