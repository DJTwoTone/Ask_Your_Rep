from models import db, User, District, UserDistrict, UserRepresentative, Representative, RepresentativeDistrict, Office, Interaction
from app import app

db.drop_all()
db.create_all()

Office.query.delete()
District.query.delete() 
Representative.query.delete()
User.query.delete()
Interaction.query.delete()
UserDistrict.query.delete()
UserRepresentative.query.delete()
RepresentativeDistrict.query.delete()

test_office = Office(phone='123-555-1234', address='123 Test St.', location='district')
test_district = District(state='ny', district_num=123, house='lower')

db.session.add(test_office)
db.session.add(test_district)
db.session.commit()

office = Office.query.get(1)
district = District.query.get(1)

test_rep = Representative(first_name='Testy', last_name='McTestface', full_name='Testy McTestface', photo_url='https://mn315.net/wp-content/uploads/2018/06/cropped-Ugandan-Knuckles.jpg', email='test@test.test', serving=True)
test_user = User.register(username='Someuser', password='1234567890', first_name='Some', last_name='User', email='some@user.com', address='123 Any St., Anytown NY 12345')

db.session.add(test_rep)
db.session.add(test_user)
db.session.commit()

user = User.query.get(1)
rep = Representative.query.get(1)

user.representatives.append(rep)
user.home_districts.append(district)
rep.offices.append(office)
rep.district.append(district)

db.session.commit()

# import pdb
# pdb.set_trace()

test_interaction = Interaction(user_id=user.id, representative_id=rep.id, interaction_date='2020-07-15 10:00:00', medium='email', topic='stuff and junk', content='all the things')
db.session.add(test_interaction)

db.session.commit()

print('If you made it this far, it seems to be working')

