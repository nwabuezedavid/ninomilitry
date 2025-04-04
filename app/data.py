import os
import django
import datetime
import random
# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from .models import Rank, Country, Award, Personnel, Achievement
def random_awards():
    """Fetch 2 or 3 random awards from the database."""
    all_awards = list(Award.objects.all())
    return random.sample(all_awards, k=min(len(all_awards), random.randint(2, 3))) if all_awards else []

def random_ranks():
    """Fetch one random rank from the database."""
    all_ranks = list(Rank.objects.all())
    return random.choice(all_ranks) if all_ranks else None  # Returns None if no ranks exist
def random_country():
    """Fetch one random rank from the database."""
    all_ranks = list(Country.objects.all())
    return random.choice(all_ranks) if all_ranks else None  # Returns None if no ranks exist

def create_initial_data():
    # Create ranks 
    ranks = [
        {'name': 'General', 'abbreviation': 'GEN'},
        {'name': 'Lieutenant General', 'abbreviation': 'LTG'},
        {'name': 'Major General', 'abbreviation': 'MG'},
        {'name': 'Brigadier General', 'abbreviation': 'BG'},
        {'name': 'Colonel', 'abbreviation': 'COL'},
        {'name': 'Lieutenant Colonel', 'abbreviation': 'LTC'},
        {'name': 'Major', 'abbreviation': 'MAJ'},
        {'name': 'Captain', 'abbreviation': 'CPT'},
        {'name': 'Lieutenant', 'abbreviation': 'LT'},
    ]
    
    for rank in ranks:
        duplicates ,ee = Rank.objects.get_or_create(name=rank['name'], abbreviation=rank['abbreviation'])
        if Rank.objects.filter(name=rank['name'], abbreviation=rank['abbreviation']).count() > 1:
            # Keep the first entry and delete the rest
            first_entry = duplicates.first()
            duplicates.exclude(id=first_entry.id).delete()
    # Create countries
    countries = [
    ('United States', 'US'),
    ('United Kingdom', 'UK'),
    ('France', 'FR'),
    ('Germany', 'DE'),
    ('Italy', 'IT'),
    ('Canada', 'CA'),
    ('Spain', 'ES'),
    ('Netherlands', 'NL'),
    ('Belgium', 'BE'),
    ('Denmark', 'DK'),
        ]
    for country_name, short_code in countries:
        Country.objects.get_or_create(name=country_name, names=short_code)

    # Create awards
    awards = [
    {"name": "Medal of Honor", "description": "Highest military decoration awarded for valor in combat" ,"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjquBoCEz1qdBBsm-kNSDtZl7Us5j1l7nLEQ&s"},
    {"name": "Distinguished Service Cross", "description": "Second highest military decoration for extraordinary heroism" ,"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRObtZtd959jFAafgTIMDjwpRTYvZKCr7ILHw&s"},
    {"name": "Silver Star", "description": "Third-highest military combat decoration for gallantry in action" ,"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQrjvsPAEHxtDGxH11qmG5-tvA3H6mx0EYyA&s"},
    {"name": "Legion of Merit", "description": "Military award for exceptionally meritorious conduct" ,"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5IylFpCDeJV8Qdwfg1jM_njd_zIaQTqvXVA&s"},
    {"name": "Bronze Star", "description": "Awarded for heroic or meritorious achievement in a combat zone" , "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9oMz5nn0gcoMWqRXZOJwwnRep8zg9gnQcxw&s"},
    {"name": "Purple Heart", "description": "Awarded to those wounded or killed while serving" ,"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgh84TCwxD_XES9qOWcFNriEYqpwjFFqnhgw&s"},
    {"name": "Air Force Cross", "description": "Awarded for extraordinary heroism in combat operations","url": "https://s.turbifycdn.com/aah/yhst-89988323165017/philippine-independence-medal-29.jpg"},
    {"name": "Navy Cross", "description": "Second highest decoration for valor in the U.S. Navy and Marine Corps" ,"url": "https://s.turbifycdn.com/aah/yhst-89988323165017/u-s-army-miniature-medals-lapel-pins-10.jpg "},
    {"name": "Coast Guard Cross", "description": "Second highest decoration for heroism in the U.S. Coast Guard" ,"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiSCzFZCgRZHxRHb-pm397J8knC-Vw0TePEU1HcfOW_HUxwesnCyQoQbcr5UP6YbDMiOc&usqp=CAU"},
    {"name": "Distinguished Flying Cross", "description": "Awarded for heroism or extraordinary achievement in aerial flight" ,'url':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgAFe4Ilz1OU1azozesIXO6Bl3LxnKJZwelQ&s'},
    {"name": "Army Distinguished Service Medal", "description": "Awarded for exceptionally meritorious service in a duty of great responsibility" ,'url':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEv-Ku7HwtMPJjaKm7soQ6cXlpPyA6pNQHqg&s'},
    {"name": "Navy Distinguished Service Medal", "description": "Awarded for distinguished service in a significant position of responsibility" ,'url':'https://s.turbifycdn.com/aah/yhst-89988323165017/u-s-coast-guard-miniature-medals-lapel-pins-9.jpg'},
    {"name": "Air Force Distinguished Service Medal", "description": "Given for exceptional meritorious service in a duty of great responsibility",'url':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREignLIXagwPacNWbCuFTQfyXgxlEs1BHQ-A&s'},
    {"name": "Coast Guard Distinguished Service Medal", "description": "Awarded for exceptionally meritorious service to the government" ,'url':'https://s.turbifycdn.com/aah/yhst-89988323165017/u-s-coast-guard-medals-and-ribbons-13.jpg'},
    {"name": "Defense Superior Service Medal", "description": "Recognizes superior meritorious service in a position of significant responsibility" ,'url':'https://s.turbifycdn.com/aah/yhst-89988323165017/commemorative-medals-13.jpg'},
    {"name": "Defense Meritorious Service Medal", "description": "Awarded for non-combat meritorious achievement or service" ,'url':'https://cdn.shopify.com/s/files/1/1185/0798/files/ServiceCrossMedals.jpg'},
    {"name": "Meritorious Service Medal", "description": "Recognizes outstanding meritorious achievement or service" ,'url':'https://s.turbifycdn.com/aah/yhst-89988323165017/commemorative-medals-13.jpg'},
    {"name": "Air Medal", "description": "Awarded for heroic actions or meritorious service in aerial flight" ,'url':'https://s.turbifycdn.com/aah/yhst-89988323165017/medal-display-cases-u-s-flag-cases-16.jpg'},
    {"name": "Combat Action Ribbon", "description": "Awarded for active participation in ground or surface combat" ,'url':'https://s.turbifycdn.com/aah/yhst-89988323165017/u-s-marine-corps-miniature-medals-lapel-pins-9.jpg'}
]



    
    for award_data in awards:
        Award.objects.get_or_create(name=award_data['name'], description=award_data['description'], url= award_data['url'])
    
    # Get objects for relationships
    
    image_urls  = [
           "https://static.euronews.com/articles/stories/04/33/27/42/1200x675_cmsv2_627a7552-2e5e-5819-8da6-a65951b9ce86-4332742.jpg",
    "https://static.euronews.com/articles/stories/04/33/27/42/1200x675_cmsv2_627a7552-2e5e-5819-8da6-a65951b9ce86-4332742.jpg",
    
    "https://img.eurointegration.com.ua/images/doc/c/6/c60d328-thumbs-b-c-cac5fb4b54d6ebaff846c577e291721d.jpg",
    "https://newsukraine.rbc.ua/static/img/_/g/_gettyimages_1238300344__1__3d3af444c592a3004a3f222e226d5f23_1300x820_186e026b2e2c329c5d87e6ecd4cb67ad_1200x675.jpg",
    "https://www.pbs.org/newshour/app/uploads/2017/02/RTSYT9T-1024x667.jpg",
    "https://images.firstpost.com/uploads/2025/03/Ulf-Kristersson-Feb-26-2025-Reuters-2025-03-47d798eaa81cada07ed5a3b8524c12ad.jpg?im=FitAndFill=(596,336)",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAf5jYLSjWBwVyRSwkX91v4ig_d0BKBgQX5FeU1aO_lN4yxvrjH0FN30mwDG8G49hcRns&usqp=CAU",
    "https://www.nato.int/nato_static_fl2014/assets/pictures/images_mfu/2025/1/stock_cv/zhelyazkov-rosen_rdax_375x503p.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuqtGnuI2O9TtjSz41wYtCD8Mnhv54eZD1ip12Fim_2sHXpJah1SLNOahhq2RPgc24Y3U&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKdzdXXWNZfJUki7jq4f4VFfRHVGcEwQc46w&s",
    "https://shape.nato.int/resources/internal/file_views_listing/19567/14_germany_final_.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDysK6wWDpdmMxli9zuKj1P1-7Eljm19ahCw&s",
    "https://shape.nato.int/resources/internal/file_views_listing/19577/6_20250304 - 4476DS - HUN NMR_.jpg",
    "https://cdn4.focus.bg/fakti/photos/big/aa1/slug-for-change-1.webp",
    "https://i.insider.com/63d8ed630a08ae0018a62106?width=700",
    "https://foreignpolicy.com/wp-content/uploads/2023/12/turkey-nato-summit-erdogan-madrid-GettyImages-1241626498.jpg?w=800?quality=90",
    "https://bsmedia.business-standard.com/_media/bs/img/article/2023-11/21/full/1700531634-0663.jpg?im=FitAndFill=(826,465)",
    "https://shape.nato.int/resources/internal/file_views_listing/19548/3_luxembourg_.jpg",
    "https://static.independent.co.uk/2025/02/19/16/5bac5ec42732080e684eb6c27946692fY29udGVudHNlYXJjaGFwaSwxNzQwMDY1MzY1-2.78640601.jpg?quality=75&width=640&crop=3%3A2%2Csmart&auto=webp",
    "https://p.potaufeu.asahi.com/566b-p/picture/28587896/c9f13fe08e40cd173deede35166e2968.jpg",
    "https://c.arvakur.is/frimg/1/50/37/1503750.jpg"
    ]
    # Create personnel
    personnel_data = [
        {
            'first_name': 'James', 
            'last_name': 'Miller',
            'rank': random_ranks(),
            'country': random_country(),
            'date_of_birth': datetime.date(1965, 5, 15),
            'biography': 'General James Miller has served with distinction for over 35 years. He has commanded forces in multiple theaters and led several key NATO operations. His strategic vision has been instrumental in shaping modern military doctrine.',
            'years_of_service': 35,
            'service_start_date': datetime.date(1988, 6, 1),
            'is_active': True,
          'awards': random_awards(),
            'url': image_urls[1],
        },
        {
            'first_name': 'Elizabeth', 
            'last_name': 'Parker',
            'rank': random_ranks(),
             'country': random_country(),
            'date_of_birth': datetime.date(1970, 8, 22),
            'biography': 'Lieutenant General Elizabeth Parker has been a trailblazer throughout her career. She was one of the first women to command a combat brigade and has served in various leadership positions across NATO. Her expertise in logistics has transformed how NATO conducts operations.',
            'years_of_service': 30,
            'service_start_date': datetime.date(1993, 9, 10),
            'is_active': True,
            'url': image_urls[2],
            'awards':random_awards(),
        },
        {
            'first_name': 'Jean', 
            'last_name': 'Dupont',
         'rank': random_ranks(),
             'country': random_country(),
            'date_of_birth': datetime.date(1975, 3, 12),
            'biography': 'Colonel Jean Dupont is a decorated officer with extensive experience in special operations. He has led numerous high-risk missions and contributed significantly to counter-terrorism strategies within NATO. His tactical innovations have been adopted by multiple member nations.',
            'years_of_service': 25,
            'service_start_date': datetime.date(1998, 7, 15),
            'is_active': True,
            'url': image_urls[3],
            'awards': random_awards()
        },
        {
        'first_name': 'James',
        'last_name': 'Miller',
        'rank': random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1965, 5, 15),
        'biography': 'General James Miller has served with distinction for over 35 years. He has commanded forces in multiple theaters and led several key NATO operations. His strategic vision has been instrumental in shaping modern military doctrine.',
        'years_of_service': 35,
        'service_start_date': datetime.date(1988, 6, 1),
        'is_active': True,
        'awards': random_awards(),
        'url': image_urls[4]

    },
    {
        'first_name': 'Robert',
        'last_name': 'Anderson',
        'rank': random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1968, 3, 22),
        'biography': 'Admiral Robert Anderson is a decorated naval officer who has commanded carrier strike groups and played a key role in maritime security operations.',
        'years_of_service': 32,
        'service_start_date': datetime.date(1991, 9, 10),
        'is_active': True,
        'awards': random_awards(),
            'url': image_urls[5]

    },
    {
        'first_name': 'Sarah',
        'last_name': 'Thompson',
        'rank': random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1972, 7, 19),
        'biography': 'Colonel Sarah Thompson has been a pioneering leader in special operations and has received multiple commendations for valor in combat.',
        'years_of_service': 28,
        'service_start_date': datetime.date(1995, 4, 5),
        'is_active': True,
        'awards': random_awards(),
            'url': image_urls[5],

    },
    {
        'first_name': 'Daniel',
        'last_name': 'Carter',
        'rank': random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1963, 11, 2),
        'biography': 'Major General Daniel Carter has played a vital role in modernizing the armed forces and has led multiple international peacekeeping missions.',
        'years_of_service': 38,
        'service_start_date': datetime.date(1985, 8, 14),
        'is_active': False,
        'awards': random_awards(),
            'url': image_urls[6]

    },
    {
        'first_name': 'William',
        'last_name': 'Foster',
        'rank': random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1970, 2, 28),
        'biography': 'Brigadier General William Foster has been instrumental in leading counterterrorism operations and has received numerous commendations for gallantry.',
        'years_of_service': 30,
        'service_start_date': datetime.date(1993, 6, 15),
        'is_active': True,
        'awards': random_awards(),
            'url': image_urls[7],

    },
    {
        'first_name': 'Michael',
        'last_name': 'Turner',
        'rank': random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1966, 12, 5),
        'biography': 'Rear Admiral Michael Turner has commanded multiple naval battle groups and has played a key role in maritime security strategies.',
        'years_of_service': 36,
        'service_start_date': datetime.date(1987, 5, 20),
        'is_active': False,
        'awards': random_awards(),
            'url': image_urls[8],

    },
    {
        'first_name': 'Emma',
        'last_name': 'Wilson',
        'rank': random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1964, 6, 11),
        'biography': 'Lieutenant General Emma Wilson has overseen numerous strategic military initiatives and helped shape future defense policies.',
        'years_of_service': 40,
        'service_start_date': datetime.date(1983, 2, 9),
        'is_active': False,
        'awards': random_awards(),
            'url': image_urls[9],

    },
    {
        'first_name': 'Christopher',
        'last_name': 'Bennett',
        'rank': random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1960, 9, 29),
        'biography': 'General Christopher Bennett is a decorated military leader who has played a crucial role in modernizing battlefield tactics.',
        'years_of_service': 42,
        'service_start_date': datetime.date(1981, 1, 17),
        'is_active': False,
        'awards': random_awards(),
            'url': image_urls[10],

    },
    {
        'first_name': 'Olivia',
        'last_name': 'Evans',
        'rank':random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1981, 4, 25),
        'biography': 'Major Olivia Evans has been recognized for her leadership in combat operations and has played a significant role in military intelligence.',
        'years_of_service': 20,
        'service_start_date': datetime.date(2004, 9, 3),
        'is_active': True,
        'awards': random_awards(),
            'url': image_urls[11],

    },
    {
        'first_name': 'Benjamin',
        'last_name': 'Hughes',
        'rank': random_ranks(),
        'country': random_country(),
        'date_of_birth': datetime.date(1985, 8, 14),
        'biography': 'Captain Benjamin Hughes has led numerous special operations missions and has been highly commended for his bravery.',
        'years_of_service': 16,
        'service_start_date': datetime.date(2009, 3, 21),
        'is_active': True,
        'awards': random_awards(),
        'url': image_urls[12],

    }
    ]
    
    # Create personnel and their achievements
    for person_data in personnel_data:
        awards = person_data.pop('awards')
        if not  Personnel.objects.filter(url=person_data['url']).exists():
            person = Personnel.objects.create(**person_data)
            person.awards.set(awards)
        
        # Add achievements for each person
            if person.first_name == 'James':
                Achievement.objects.create(
                    personnel=person,
                    title='Led Operation Mountain Shield',
                    description='Successfully commanded a multinational force of 15,000 troops in a complex peacekeeping operation.',
                    date=datetime.date(2015, 6, 10)
                )
                Achievement.objects.create(
                    personnel=person,
                    title='NATO Strategic Command Appointment',
                    description='Appointed to lead NATO\'s Strategic Command for Operations, overseeing all NATO military operations globally.',
                    date=datetime.date(2018, 3, 15)
                )
            elif person.first_name == 'Elizabeth':
                Achievement.objects.create(
                    personnel=person,
                    title='Humanitarian Mission Success',
                    description='Coordinated the largest humanitarian aid delivery in NATO history, providing critical supplies to over 2 million civilians.',
                    date=datetime.date(2017, 11, 5)
                )
                Achievement.objects.create(
                    personnel=person,
                    title='NATO Logistics Transformation Initiative',
                    description='Led the comprehensive overhaul of NATO\'s logistics systems, increasing efficiency by 40% and reducing costs by €300 million annually.',
                    date=datetime.date(2020, 2, 28)
                )
            elif person.first_name == 'Jean':
                Achievement.objects.create(
                    personnel=person,
                    title='Counter-Terrorism Task Force',
                    description='Established and led a multinational counter-terrorism task force that successfully prevented multiple high-profile threats.',
                    date=datetime.date(2016, 8, 12)
                )
                Achievement.objects.create(
                    personnel=person,
                    title='Special Operations Training Program',
                    description='Developed an advanced training program for special operations forces that has been adopted by 12 NATO member countries.',
                    date=datetime.date(2019, 5, 20)
                )
    
    print("Initial data created successfully!")

 
    