from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        db = connection.cursor().db_conn.client[settings.DATABASES['default']['NAME']]
        # Collections
        users = db.users
        teams = db.teams
        activities = db.activities
        leaderboard = db.leaderboard
        workouts = db.workouts

        # Clear collections
        users.delete_many({})
        teams.delete_many({})
        activities.delete_many({})
        leaderboard.delete_many({})
        workouts.delete_many({})

        # Create unique index on email
        users.create_index([('email', 1)], unique=True)

        # Sample teams
        marvel = {'name': 'Marvel', 'members': []}
        dc = {'name': 'DC', 'members': []}
        teams.insert_many([marvel, dc])

        # Sample users
        user_data = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
        ]
        users.insert_many(user_data)

        # Sample activities
        activities.insert_many([
            {'user': 'Iron Man', 'activity': 'Running', 'duration': 30},
            {'user': 'Wonder Woman', 'activity': 'Cycling', 'duration': 45},
        ])

        # Sample leaderboard
        leaderboard.insert_many([
            {'team': 'Marvel', 'points': 100},
            {'team': 'DC', 'points': 90},
        ])

        # Sample workouts
        workouts.insert_many([
            {'user': 'Iron Man', 'workout': 'Pushups', 'reps': 50},
            {'user': 'Batman', 'workout': 'Squats', 'reps': 40},
        ])

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
