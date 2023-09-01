from base import models


user_interactions = models.UserInteraction.objects.all()

for interaction in user_interactions:
    user_id = interaction.user_id
    visited_url = interaction.visited_url
    timestamp = interaction.timestamp


    print(f"User ID: {user_id}, Visited URL: {visited_url}, Timestamp: {timestamp}")