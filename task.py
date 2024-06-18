import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the data
df = pd.read_csv("C:\\Users\\shubh\\OneDrive\\Desktop\\USvideos.csv")
print(df.head())

# Drop duplicates
df = df.drop_duplicates()

# Display basic statistics
print(df.describe())

# Display information about the dataframe
print(df.info())

# Remove unnecessary columns
columns_to_remove = ['thumbnail_link', 'description']
df = df.drop(columns=columns_to_remove)
print(df.info())

# Correct imports and parsing dates
df["trending_date"] = df['trending_date'].apply(lambda x: datetime.strptime(x, '%y.%d.%m'))
print(df.head(3))

df['publish_time'] = pd.to_datetime(df['publish_time'])
print(df.head(2))

# Extract date components
df['publish_month'] = df['publish_time'].dt.month
df['publish_day'] = df['publish_time'].dt.day
df['publish_hour'] = df['publish_time'].dt.hour
print(df.head(2))

# Map category IDs to names
category_map = {
    1: 'Film and Animation',
    2: 'Autos and Vehicles',
    10: 'Music',
    15: 'Pet and Animal',
    17: 'Sports',
    19: 'Travel and Events',
    20: 'Gaming',
    22: 'People and Blogs',
    23: 'Comedy',
    24: 'Entertainment',
    25: 'News and Politics',
    26: 'How to and Style',
    27: 'Education',
    28: 'Science and Technology',
    29: 'Non Profits and Activism',
    30: 'Movies',
    43: 'Shows'
}
df['category_name'] = df['category_id'].map(category_map)

print(df.head())

# Extract year from publish_time
df['year'] = df['publish_time'].dt.year

# Plot total publish count per year
yearly_count = df.groupby('year')['video_id'].count()
yearly_count.plot(kind='bar', xlabel='Year', ylabel='Total Publish Count', title='Total Publish Video Per Year')
plt.show()

# Plot total views per year
yearly_views = df.groupby('year')['views'].sum()
yearly_views.plot(kind='bar', xlabel='Year', ylabel='Total Views', title='Total Views per Year')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Top categories by views
category_views = df.groupby('category_name')['views'].sum().reset_index()
top_categories = category_views.sort_values(by='views', ascending=False).head(5)
plt.bar(top_categories['category_name'], top_categories['views'])
plt.xlabel('Category Name', fontsize=12)
plt.ylabel('Total Views', fontsize=12)
plt.title('Top 5 Categories by Views', fontsize=15)
plt.tight_layout()
plt.show()

# Video count by category
plt.figure(figsize=(12, 6))
sns.countplot(x='category_name', data=df, order=df['category_name'].value_counts().index)
plt.xticks(rotation=90)
plt.title('Video Count by Category')
plt.show()

# Number of videos published per hour
video_per_hour = df['publish_hour'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
sns.barplot(x=video_per_hour.index, y=video_per_hour.values, palette='rocket')
plt.title('Number of Videos Published per Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Videos')
plt.xticks(rotation=45)
plt.show()

# Video publish over time
df['publish_date'] = df['publish_time'].dt.date
video_count_by_date = df.groupby('publish_date').size()
plt.figure(figsize=(12, 6))
sns.lineplot(data=video_count_by_date)
plt.title("Video Publish Over Time")
plt.xlabel('Publish Date')
plt.ylabel('Number of Videos')
plt.xticks(rotation=45)
plt.show()

# Scatter plot for Views vs Likes
sns.scatterplot(data=df, x='views', y='likes')
plt.title('Views vs Likes')
plt.xlabel('Views')
plt.ylabel('Likes')
plt.show()

# Plots for comments, ratings, and video errors
plt.figure(figsize=(14, 8))
plt.subplots_adjust(wspace=0.2, hspace=0.4, top=0.9)
plt.subplot(2, 2, 1)
g = sns.countplot(x='comments_disabled', data=df)
g.set_title("Comments Disabled", fontsize=16)
plt.subplot(2, 2, 2)
g1 = sns.countplot(x='ratings_disabled', data=df)
g1.set_title("Rating Disabled", fontsize=16)
plt.subplot(2, 2, 3)
g2 = sns.countplot(x='video_error_or_removed', data=df)
g2.set_title("Video Error or Removed", fontsize=16)
plt.show()

# Correlation between views and likes
corr_matrix = df['views'].corr(df['likes'])
print(f'Correlation between views and likes: {corr_matrix}')
