import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

extract = URLExtract()
#Top Statistics
def fetch_stats(Selected_user,df):

    if Selected_user !='overall':
        df = df[df['user'] == Selected_user]
    #fetch number of messages
    num_messages = df.shape[0]

    #fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_images = df[df['message'].str.contains('image omitted', case=False, na=False)].shape[0]
    num_media_videos = df[df['message'].str.contains('video omitted', case=False, na=False)].shape[0]

    # Total media count
    total_media = num_media_images + num_media_videos

    # number of links
    Links = []
    for message in df['message']:
        Links.extend(extract.find_urls(message))


    return num_messages, len(words),total_media,len(Links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    return x

# word cloud
def create_wordcloud(Selected_user,df):

    f =open('stop_hinglish.txt','r')
    stop_words = f.read()

    if Selected_user != "overall":
        df = df[df['user'] == Selected_user]

    temp =df[df['user'] != "group_notification"]
    temp = temp[temp['message'] != "<Media omitted>\n"]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color="black")
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


#most common words
def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


# emoji
def emoji_helper(Selected_user,df):
    if Selected_user == "overall":
        filtered_df = df
    else:
        filtered_df = df[df['user'] == Selected_user]

    emojis = []
    for message in filtered_df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA.keys()])

    emojis_df = pd.DataFrame(Counter(emojis).most_common(),columns=["Emoji","Count"])

    return emojis_df

#monthly timeline
def monthly_timeline(Selected_user, df):
    # Filter data based on the selected user
    if Selected_user == "overall":
        filtered_df = df
    else:
        filtered_df = df[df['user'] == Selected_user]

    # Group data by year, month_num, and month
    timeline = filtered_df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Create a 'time' column for plotting
    timeline['time'] = timeline.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)

    return timeline
# daily timeline
def daily_timeline(Selected_user, df):
    # Filter data based on the selected user
    if Selected_user == "overall":
        filtered_df = df
    else:
        filtered_df = df[df['user'] == Selected_user]

    # Group data by the datetime field
    daily_timeline = filtered_df.groupby('datetime').count()['message'].reset_index()

    return daily_timeline
#week activity map
def week_activity_map(Selected_user, df):
    if Selected_user != 'overall':
     df = df[df['user'] == Selected_user]
    return df['day_name'].value_counts()


#month activity map
def month_activity_map(Selected_user, df):
    if Selected_user != 'overall':
        df = df[df['user'] == Selected_user]

    return df['month'].value_counts()


def activity_heatmap(Selected_user, df):
    if Selected_user != 'overall':
        df = df[df['user'] == Selected_user]


    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)


    return user_heatmap
