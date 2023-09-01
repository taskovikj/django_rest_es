import numpy as np
import pandas as pd
from lightfm import LightFM
from lightfm.cross_validation import random_train_test_split
from lightfm.data import Dataset
from .models import UserInteraction
from datetime import  datetime

def preprocess_data(df):
    # You can use apply to process the 'visited_url' column
    df['visited_url'] = df['visited_url'].apply(lambda url: int(url.split('/')[2]))

    # Drop the 'id' column if you don't need it
    # df = df.drop(columns=['id'])

    # Factorize user_id to start from 1
    df['user_id'] = pd.factorize(df['user_id'])[0] + 1

    # Normalize timestamp
    df['timestamp'] = df['timestamp'].apply(lambda t: int(datetime.timestamp(t)))
    min_timestamp = df['timestamp'].min()
    max_timestamp = df['timestamp'].max()
    df['timestamp'] = (df['timestamp'] - min_timestamp) / (max_timestamp - min_timestamp)

    return df


def get_dataset():
    # Retrieve data from the UserInteraction model
    interactions = UserInteraction.objects.values_list('user_id', 'visited_url', 'timestamp')

    # Create a DataFrame from the interactions
    df = pd.DataFrame(interactions, columns=['user_id', 'visited_url', 'timestamp'])

    # Preprocess the data
    df = preprocess_data(df)

    # Extract unique users and posts
    users = set(df['user_id'])
    posts = set(df['visited_url'])

    # Create a Dataset object
    dataset = Dataset()
    dataset.fit(users=users, items=posts)

    return df, dataset


def build_model(df, new_dataset):
    dataset = new_dataset

    # Build interactions matrix
    (interactions, weights) = dataset.build_interactions(df.itertuples(index=False))

    # Split data into train and test sets
    train, test = random_train_test_split(interactions)

    # Define and train the LightFM model
    model = LightFM(loss='warp')  # 'warp' stands for Weighted Approximate-Rank Pairwise loss
    model.fit(train, epochs=30, num_threads=2)

    return model


def get_recommendations(user_id, num_recommendations=5):
    df, dataset = get_dataset()
    model = build_model(df, dataset)

    # Recommend items for a specific user
    user_idx = dataset.mapping()[0][user_id]
    n_items = len(dataset.items())

    scores = model.predict(user_ids=user_idx, item_ids=np.arange(n_items))

    # Get top recommendations
    top_recommendations = np.argsort(-scores)[:num_recommendations]

    return top_recommendations
