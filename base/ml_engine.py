from datetime import datetime

import numpy as np
import pandas as pd
from lightfm import LightFM
from lightfm.cross_validation import random_train_test_split
from lightfm.data import Dataset
from .models import UserInteraction


def preprocess_data(df=None):
    df['visited_url'] = df['visited_url'].map(lambda url: int(url.split('/')[2]))
    df.drop(columns=['id'], inplace=True)
    df['timestamp'] = df['timestamp'].apply(lambda t: int(datetime.timestamp(t)))

    df['timestamp'] = (df['timestamp'] - df['timestamp'].min()) / (
            df['timestamp'].max() - df['timestamp'].min())



    return df


def get_dataset():
    interactions = list(UserInteraction.objects.values_list())
    df = pd.DataFrame(interactions, columns= ['id', 'user_id','visited_url', 'timestamp'])

    df = preprocess_data(df)

    data = [tuple(i) for i in df.values]

    # Extract unique users and posts
    users = set(row[0] for row in data)
    posts = set(row[1] for row in data)

    # Create a Dataset object
    dataset = Dataset()
    dataset.fit(users=users, items=posts)

    return df, dataset


def build_model(df=None, new_dataset=None):
    dataset = new_dataset
    data = [tuple(i) for i in df.values]

    # Build interactions matrix
    (interactions, weights) = dataset.build_interactions((row[0], row[1]) for row in data)

    # Split data into train and test sets
    train, test = random_train_test_split(interactions)

    # Define and train the LightFM model
    model = LightFM(loss='warp')  # 'warp' stands for Weighted Approximate-Rank Pairwise loss
    model.fit(train, epochs=30, num_threads=2)

    return model


def get_recommendations(user_id, num_recomendations=5):
    df, dataset = get_dataset()
    model = build_model(df, dataset)

    data = [tuple(i) for i in df.values]
    posts = set(row[1] for row in data)

    # Recommend items for a specific user
    if user_id not in dataset.mapping()[0].keys():
        post_visits_counts = df.groupby('visited_url').size().reset_index(name='visit_count')
        sorted_posts = post_visits_counts.sort_values(by='visit_count', ascending=False)
        return sorted_posts['visited_url'][:num_recomendations].values

    user_idx = dataset.mapping()[0][user_id]
    n_items = len(posts)
    item_indices = np.arange(n_items)  # Create a NumPy array of item indices
    scores = model.predict(user_ids=user_idx, item_ids=item_indices)

    # Get top recommendations
    top_recommendations = sorted(zip(posts, scores), key=lambda x: -x[1])[:num_recomendations]

    top_recommendations = [i for i,_ in top_recommendations]

    return top_recommendations