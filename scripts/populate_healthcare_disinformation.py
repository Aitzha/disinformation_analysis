import os
import sys
import django
import csv
from collections import defaultdict

sys.path.append('D:/projects/Advanced Web Development/disinformation_analysis')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "disinformation_analysis.settings")
django.setup()

from researchdata.models import *

project_path = os.getenv('PROJECT_PATH')
heathcare_disinfo_data = project_path + "/Healthcare_Disinfo_Study_Data.csv"

users = defaultdict(list)
personalities = defaultdict(list)
responses = []

with open(heathcare_disinfo_data) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    next(csv_reader, None)

    # get all unique user ids from csv file
    unique_user_ids = set()
    for row in csv_reader:
        if not unique_user_ids.__contains__(row[1]):
            unique_user_ids.add(row[1])
            users[row[1]] = row[21:25]
            personalities[row[1]] = row[34:48] + row[49:65]

        responses.append(row[0:4] + row[9:10] + row[11:12])

User.objects.all().delete()
Personality.objects.all().delete()
Response.objects.all().delete()

user_objects = {}

for user_id, data in users.items():
    if not user_id.isnumeric():
        continue

    genderDict = {'1': 'male', '2': 'female', '3': 'non-binary', '4': 'prefer not to say'}
    birth_yearDict = {'1': 1990, '2': 1991, '3': 1992, '4': 1993, '5': 1994, '6': 1995, '7': 1996,
                      '8': 1997, '9': 1998, '10': 1999, '11': 2000, '12': 2001, '13': 2002, '14': 2003}
    ethnicityDict = {'1': 'white', '2': 'african american', '3': 'hispanic', '4': 'pacific islander',
                     '5': 'native american', '6': 'asian american', '7': 'multiracial', '8': 'other'}
    parentEduDict = {'1': 'less than high school', '2': 'high school/GED', '3': 'some college', '4': 'vocational/technica/community college degree',
                     '5': 'four-year college degree', '6': 'advanced degree', '7': 'dont know'}


    newUser = User.objects.create(user_id=int(user_id),
                                  gender=genderDict.get(data[0], 'prefer not to say'),
                                  birth_year=birth_yearDict.get(data[1], -1),
                                  ethnicity=ethnicityDict.get(data[2], 'other'),
                                  parent_edu=parentEduDict.get(data[3], 'dont know'))

    newUser.save()
    user_objects[user_id] = newUser


for user_id, data in personalities.items():
    if not user_id.isnumeric():
        continue

    if not user_objects.__contains__(user_id):
        continue

    newPersonality = Personality.objects.create(user_id=user_objects[user_id],
                                                mac1=int(data[0]),
                                                mac2=int(data[1]),
                                                mac3=int(data[2]),
                                                mac4=int(data[3]),
                                                mac5=int(data[4]),
                                                mac6=int(data[5]),
                                                mac7=int(data[6]),
                                                mac8=int(data[7]),
                                                mac9=int(data[8]),
                                                mac10=int(data[9]),
                                                mac11=int(data[10]),
                                                smds1=int(data[11]),
                                                smds2=int(data[12]),
                                                smds3=int(data[13]),
                                                smds4=int(data[14]),
                                                smds5=int(data[15]),
                                                smds6=int(data[16]),
                                                smds7=int(data[17]),
                                                smds8=int(data[18]),
                                                smds9=int(data[19]),
                                                smds10=int(data[20]),
                                                smds11=int(data[21]),
                                                smds12=int(data[22]),
                                                risk1=int(data[23]),
                                                risk2=int(data[24]),
                                                risk3=int(data[25]),
                                                risk4=int(data[26]),
                                                risk5=int(data[27]),
                                                risk6=int(data[28]),
                                                risk7=int(data[29]))

    newPersonality.save()