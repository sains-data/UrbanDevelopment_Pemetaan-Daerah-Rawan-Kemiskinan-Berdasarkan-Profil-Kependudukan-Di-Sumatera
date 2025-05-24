from airflow import settings
from airflow.models import User, Role
from sqlalchemy.orm.exc import NoResultFound

username = "naufal"
password = "naufalfakhri"
email = "naufal@example.com"
first_name = "naufal"
last_name = "fakhri"

session = settings.Session()

try:
    user = session.query(User).filter(User.username == username).one()
    print("User sudah ada.")
except NoResultFound:
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_active=True,
    )
    user.set_password(password)

    admin_role = session.query(Role).filter(Role.name == "Admin").one()
    user.roles = [admin_role]

    session.add(user)
    session.commit()
    print(f"User '{username}' berhasil dibuat.")
