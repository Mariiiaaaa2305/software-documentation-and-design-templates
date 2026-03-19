from models.apartment import Apartment, db

class ApartmentService:
    @staticmethod
    def get_all():
        return Apartment.query.all()

    @staticmethod
    def get_by_id(apt_id):
        return Apartment.query.get(apt_id)

    @staticmethod
    def add_apartment(data):
        new_apt = Apartment(
            title=data.get('title'),
            address=data.get('address'),
            price=data.get('price'),
            description=data.get('description')
        )
        db.session.add(new_apt)
        db.session.commit()

    @staticmethod
    def update_apartment(apt_id, data):
        apt = Apartment.query.get(apt_id)
        if apt:
            apt.title = data.get('title')
            apt.address = data.get('address')
            apt.price = data.get('price')
            apt.description = data.get('description')
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_apartment(apt_id):
        apt = Apartment.query.get(apt_id)
        if apt:
            db.session.delete(apt)
            db.session.commit()
            return True
        return False