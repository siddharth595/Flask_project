from restro.models import Table, User, Reservation
from restro import db
import datetime

DEFAULT_RESERVATION_LENGTH = 1 # 1 hour

def create_reservation(form_data):
    guest = User.query.filter_by(phone_number=form_data.guest_phone.data).first()
    
    #now check table availability
    capacity = int(form_data.num_guests.data)
    tables = Table.query.filter(Table.capacity >= capacity).order_by(Table.capacity.desc()).all()
    t_ids = [t.id for t in tables]
    if not t_ids:
        # no tables with that size
        return False

    # check reservations
    begin_range = form_data.reservation_datetime.data - datetime.timedelta(hours=DEFAULT_RESERVATION_LENGTH)
    end_range = form_data.reservation_datetime.data + datetime.timedelta(hours=DEFAULT_RESERVATION_LENGTH)
    # reservations = Reservation.query.filter(Reservation.table.in_(
    #     t_ids), Reservation.reservation_time >= begin_range, Reservation.reservation_time <= end_range).all()
    reservations = Reservation.query.join(Reservation.table).filter(Table.id.in_(t_ids),
                    Reservation.reservation_time >= begin_range, Reservation.reservation_time <= end_range).order_by(Table.capacity.desc()).all()
    if reservations:
        if len(t_ids) == len(reservations):
            return False
        else:
            # get available table
            table_id = (set(t_ids) - set([r.table.id for r in reservations])).pop()
            reservation = Reservation(guest=guest, table=Table.query.get(int(table_id)),
                                      num_guests=capacity, reservation_time=form_data.reservation_datetime.data)
    else:
        # we are totally open
        reservation = Reservation(guest=guest, table=Table.query.get(int(t_ids[0])), num_guests = capacity, reservation_time=form_data.reservation_datetime.data)

    db.session.add(reservation)
    db.session.commit()
    return reservation