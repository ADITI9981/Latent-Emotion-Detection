import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import Helper
from PIL import Image
from auth import signup_user, login_user, reset_password
from Preprocessor import preprocess
from Helper import fetch_stats
from wordcloud import WordCloud
import labels
import numpy as np
import altair as alt
import sklearn
import joblib
import os

# Database Path
DB_PATH = "users.db"

# Apply CSS for custom styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(to bottom, #ffecd2, #fcb69f);
            color: #333;
            font-family: 'Roboto', sans-serif;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #3f2b96, #a8c0ff);
            color: white;
        }

        [data-testid="stSidebar"] .css-qbe2hs {
            font-weight: bold;
            color: white;
        }

        h1, h2, h3 {
            font-family: 'Roboto Slab', serif;
            color: #3E64FF;
        }

        h4, h5, h6 {
            color: #3E64FF;
            font-weight: 700;
        }

        .css-1d391kg {
            padding: 1.5rem;
        }

        .stDownloadButton button {
            background-color: #FF6F61;
            color: white;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
        }
        .stDownloadButton button:hover {
            background-color: #FF3F34;
        }

        table {
            margin: 0 auto;
            font-size: 16px;
        }
        .highlighted-title {
           font-size: 36px;
           font-weight: bold;
           color: black;  /* Black color */
           text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.7);  
           letter-spacing: 1px;  
}
    </style>
    """,
    unsafe_allow_html=True,
)

# Create Navigation Sidebar
st.sidebar.title("Latent Emotion Detection")
page = st.sidebar.radio("Navigation", ["User Guide", "Login", "Signup", "Forgot Password", "File Upload", "Analysis",
                                       "Text Emotion Detection"])

# Sidebar icon (optional)
st.sidebar.image("analy.png")

# User Guide Page
if page == "User Guide":
    st.title("📘 User Guide")
    st.image("emoji.jpg")
    st.markdown("<h2 style='color:#3E64FF;'>Welcome to Latent Emotion Detection!</h2>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style="color:#3498db;">How to Use:</h3>
        <ul style="color:#2c3e50; line-height: 1.8;">
            <li><b style="color:#e74c3c;">Signup:</b><span style="color:#ffffff;"> Create your account to access features.</span></li>
            <li><b style="color:#8e44ad;">Login:</b><span style="color:#ffffff;"> Securely log in with your credentials.</span></li>
            <li><b style="color:#16a085;">Upload:</b><span style="color:#ffffff;"> Upload your chat file for processing.</span></li>
            <li><b style="color:#f39c12;">Analyze:</b><span style="color:#ffffff;"> Gain insights into your chat data.</span></li>
        </ul>
    """, unsafe_allow_html=True)
    #Additional Details and features
    st.subheader("Features")
    st.write("""- **User-based Analysis**: Analyze data for individual users or the overall chat.
                - **Statistics**: View total messages, words, media shared, and links shared.
                - **Monthly Timeline**: See the message activity trend over time.""")
    # Instructions for Exporting Data
    st.subheader("How to Export Data")
    st.write("""After analyzing your chat data, you can export the results to a file for further use.""")

    # Additional Guidelines
    st.subheader("Guidelines")
    st.write("""- Ensure the chat file is in **text format** and not corrupted.
                - The app works best with **clean data**. It's recommended to clean your chat export.""")

# Login Page
elif page == "Login":
    st.title("Login Page")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    st.markdown("""<p><a href="#forgot-password">Forgot Password?</a></p>""", unsafe_allow_html=True)
    if st.button("Login"):
        if username and password:
            user_exists = login_user(username, password, DB_PATH)
            if user_exists:
                st.success(f"Welcome {username}! Proceed to the 'Analysis' page.")
                st.session_state['logged_in'] = True
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Please fill all fields.")

# Signup Page
elif page == "Signup":
    st.title("Signup Page")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    if st.button("Signup"):
        if username and password:
            signup_user(username, password, DB_PATH)
            st.success("Signup successful! Please go to the 'Login' page to log in.")
        else:
            st.error("Please fill all fields.")

# Forgot Password Page
elif page == "Forgot Password":
    st.title("Forgot Password")
    username = st.text_input("Enter your username")
    new_password = st.text_input("Enter your new password", type="password")
    confirm_password = st.text_input("Confirm your new password", type="password")
    if st.markdown('[Reset Password](#)', unsafe_allow_html=True):

        if username and new_password and confirm_password:
            if new_password == confirm_password:
                message = reset_password(username, new_password, DB_PATH)
                if "successfully" in message:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("Passwords do not match!")
        else:
            st.error("Please fill all fields.")

# File Upload Page
elif page == "File Upload":
    st.title("Upload Data File")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.success("File uploaded successfully! Proceed to the 'Analysis' page.")
        img = Image.open('thankyou.gif')
        img = img.resize((800, 300))  # Resize to desired dimensions
        st.image(img)

# Analysis Page
elif page == "Analysis":
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        if 'uploaded_file' in st.session_state:
            uploaded_file = st.session_state.uploaded_file
            st.title("Data Analysis")
            try:
                bytes_data = uploaded_file.getvalue()
                data = bytes_data.decode("utf-8")
                df = preprocess(data)

                if 'user' in df.columns:
                    st.success("Analysis Complete! View the results below.")
                    st.dataframe(df)
                else:
                    st.error("The uploaded file does not contain a 'user' column.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please upload a file first in the 'File Upload' section.")
    else:
        st.warning("Please log in to access the analysis page.")

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "overall")

        # User selection for analysis
        Selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

        # Show Analysis button
        if st.sidebar.button("Show Analysis"):
            num_messages, words, total_media, num_links = fetch_stats(Selected_user, df)

            # Display top statistics
            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(total_media)
            with col4:
                st.header("Links Shared")
                st.title(num_links)

            # Show Monthly Timeline Chart
            st.title("Monthly Timeline")
            timeline = Helper.monthly_timeline(Selected_user, df)
            if not timeline.empty:
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['message'], color='purple')
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.error("No data available for the Monthly Timeline.")

            # Daily timeline
            st.title("Daily Timeline")
            daily_timeline = Helper.daily_timeline(Selected_user, df)

            if not daily_timeline.empty:
                daily_timeline['datetime'] = pd.to_datetime(daily_timeline['datetime'], format='%Y-%m-%d')

                # Apply smoothing
                daily_timeline['smoothed'] = daily_timeline['message'].rolling(window=7, center=True).mean()

                fig, ax = plt.subplots(figsize=(12, 6))  # Increase graph size for readability
                ax.plot(daily_timeline['datetime'], daily_timeline['smoothed'], color='blue', label='')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
                plt.xticks(rotation=45)
                ax.set_xlabel('Date')
                ax.set_ylabel('Number of Messages')
                ax.set_title(f"Daily Timeline for {Selected_user}")
                plt.legend()
                st.pyplot(fig)
            else:
                st.write("No data to show for the selected user in Daily Timeline.")

            # weekly activity
            activity_map = '<br><br><u><p style="font-family:Roboto; color:#3E64FF; font-size: 40px; font-weight: bold">Activity Map</p></u>'
            st.markdown(activity_map, unsafe_allow_html=True)
            st.markdown(
                '<p style="font-family:Roboto fax; color:#ffa81a; font-size: 15px; font-weight: bold">This stats shows which day and month of your chats are busy</p>',
                unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                most_busy_day = '<p style="font-family:georgia; color:#3E64FF; font-size: 30px; font-weight: bold">Most Busy Day</p>'
                st.markdown(most_busy_day, unsafe_allow_html=True)
                busy_day = Helper.week_activity_map(Selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='pink')
                plt.xticks(rotation='vertical')
                plt.title("Most busy day in a week")
                plt.xlabel("Days")
                plt.ylabel("Number of chats")
                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(3)
                    ax.spines[axis].set_color("orange")
                    ax.spines[axis].set_zorder(5)
                st.pyplot(fig)

            with col2:
                most_busy_month = '<p style="font-family:Roboto; color:#3E64FF; font-size: 30px; font-weight: bold">Most Busy Month</p>'
                st.markdown(most_busy_month, unsafe_allow_html=True)
                busy_month = Helper.month_activity_map(Selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='purple')
                plt.xticks(rotation='vertical')
                plt.title("Most busy month")
                plt.xlabel("Months")
                plt.ylabel("Number of chats")
                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(3)
                    ax.spines[axis].set_color("orange")
                    ax.spines[axis].set_zorder(5)
                st.pyplot(fig)

            # Weekly hours' activity map
            weekly_hours_activity_map = '<br><br><u><p style="font-family:Roboto; color:#3E64FF; font-size: 40px; font-weight: bold">Weekly Hours Activity Map</p></u>'
            st.markdown(weekly_hours_activity_map, unsafe_allow_html=True)
            st.markdown(
                '<p style="font-family:Roboto fax; color:#ffa81a; font-size: 15px; font-weight: bold">This map shows the active hours of the  group across the week</p>',
                unsafe_allow_html=True)
            user_heatmap = Helper.activity_heatmap(Selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 4))
            if not user_heatmap.empty:
                ax = sns.heatmap(user_heatmap)
                st.pyplot(fig)
            else:
                st.write("No activity data available for the selected user.")

            plt.title("Weekly Hours Activity Map")
            plt.xlabel("Time")
            plt.ylabel("Number of chats")
            for axis in ['top', 'bottom', 'left', 'right']:
                ax.spines[axis].set_linewidth(3)
                ax.spines[axis].set_color("orange")
                ax.spines[axis].set_zorder(5)
            st.pyplot(fig)

             # finding the busiest users  in the group
            if Selected_user == 'overall':
                st.title('Most Busy User')
                x = Helper.most_busy_users(df)
                # Check if the data is empty
                if x.empty:
                    st.error("No data available to analyze most busy users.")
                else:
                   # Styling for the section using HTML & CSS
                   st.markdown("""
                    <style>
                            .busy-users-title {
                                font-size: 28px;
                                color: #FF6F61;
                                font-weight: bold;
                                text-align: center;
                                margin-bottom: 20px;
                            }
                            .chart-container {
                                padding: 15px;
                                background: linear-gradient(145deg, #f7f7f7, #e6e6e6);
                                border-radius: 15px;
                                box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1), -5px -5px 15px rgba(255, 255, 255, 0.5);
                                margin: 20px auto;
                            }
                    </style>
                    """, unsafe_allow_html=True)

                  # Create a layout with two columns
                col1, col2 = st.columns([3, 1])

                # Left column: Display bar chart
                with col1:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

                    # Plotting bar chart
                    fig, ax = plt.subplots(figsize=(10, 6))  # Adjusted size for clarity
                    bar_colors = plt.cm.coolwarm(x.values / max(x.values))  # Dynamic colors based on values
                    ax.bar(x.index, x.values, color=bar_colors, edgecolor='black', linewidth=0.7)

                        # Styling the chart
                    ax.set_title("Most Active Users", fontsize=16, fontweight='bold', color='#333')
                    ax.set_xlabel("Users", fontsize=12, labelpad=10)
                    ax.set_ylabel("Message Count", fontsize=12, labelpad=10)
                    ax.tick_params(axis='x', rotation=45, labelsize=10)
                    ax.tick_params(axis='y', labelsize=10)
                    plt.grid(axis='y', linestyle='--', alpha=0.7)

                    # Display the chart
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

                       # Right column: Additional insights
                with col2:
                    st.subheader("📈 Insights")
                    st.markdown(f"""
                        - **Most Active User:** {x.index[0]}
                        - **Messages Sent:** {x.values[0]}
                        - **Total Users Analyzed:** {len(x)}
                        """)
                    st.image("activity_icon.jpeg")




            # Word Cloud
            st.title("🎨 Word Cloud Analysis")

            # Generate Word Cloud using Helper function
            df_wc = Helper.create_wordcloud(Selected_user, df)

            # Styling for Word Cloud Section
            st.markdown("""
                    <style>
                    .wordcloud-title {
                        font-size: 28px;
                        color: #FF6F61;
                        font-weight: bold;
                        text-align: center;
                        margin-bottom: 20px;
                    }
                    .wordcloud-container {
                        padding: 15px;
                        background: linear-gradient(145deg, #f7f7f7, #e6e6e6);
                        border-radius: 15px;
                        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1), -5px -5px 15px rgba(255, 255, 255, 0.5);
                        margin: 20px auto;
                    }
                    </style>
                    <div class="wordcloud-title">Word Cloud Representation</div>
                 """, unsafe_allow_html=True)

                  # Set up a layout with two columns
            col1, col2 = st.columns([2, 1])

                # Display Word Cloud
            if df_wc:
                with col1:
                 st.markdown('<div class="wordcloud-container">', unsafe_allow_html=True)
                 fig, ax = plt.subplots(figsize=(10, 6))  # Adjust size for better visualization
                 ax.imshow(df_wc, interpolation='bilinear')
                 ax.axis("off")  # Hide axes for a cleaner look
                 st.pyplot(fig)
                 st.markdown('</div>', unsafe_allow_html=True)

                 # Optional: Display additional info or controls in the second column
                with col2:
                 st.markdown("""
                 **What is a Word Cloud?**
                   A word cloud visually represents frequently used words in your data.

                   **Usage Tips:**
                    - Highlight important terms at a glance.
                    - Understand key topics or sentiments quickly.
                    """)
            else:
                st.error("No data available to generate a Word Cloud.")



            # most common words
            most_common_df = Helper.most_common_words(Selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')
            st.title('Most common words')
            st.pyplot(fig)

            # Emoji analysis

            # helper.emoji_helper returns a list of emojis and their counts
            emoji_df = Helper.emoji_helper(Selected_user, df)
            st.title("Emoji Analysis")
            st.image('91636.jpg', width=700,caption="Emoji Insights")

            # Define specific colors for the top 5 emojis
            color_mapping = ['Red', 'Blue', 'Pink', 'Purple', 'Yellow']

            st.markdown("""
                <style>
                    .emoji-title {
                        color: #2E3A59;
                        font-size: 28px;
                        font-weight: bold;
                        text-align: center;
                    }
                    .emoji-card {
                        padding: 15px;
                        border-radius: 10px;
                        background: linear-gradient(145deg, #f7f7f7, #e6e6e6);
                        box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.1), -4px -4px 8px rgba(255, 255, 255, 0.5);
                        margin-top: 20px;
                    }
                    .emoji-chart-container {
                        padding: 15px;
                        border-radius: 10px;
                        border: 2px solid #FF6F61; /* Border around the pie chart */
                        background: #fff;
                        box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.1), -4px -4px 8px rgba(255, 255, 255, 0.3);
                    }
                    .dataframe-style {
                        margin-top: 20px;
                        border: 2px solid #FF6F61;
                        border-radius: 10px;
                        box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
                    }
                </style>
                """, unsafe_allow_html=True)



            # Create two columns for the display
            col1, col2 = st.columns(2)

            if not emoji_df.empty:
                # Get top 5 emojis by count
             top_emojis = emoji_df.nlargest(5, 'Count')

            # Assign colors from the color mapping
             top_emojis['Color'] = [color_mapping[i] for i in range(len(top_emojis))]


             with col1:
                st.markdown('<div class="emoji-card"><h3 style="color:#FF6F61;">Top 5 Emojis</h3></div>',
                                unsafe_allow_html=True)
                styled_df = top_emojis[['Emoji', 'Count', 'Color']]
                st.dataframe(styled_df.style.highlight_max(subset=['Count'], color='#FF6F61', axis=0))

             with col2:
                # Create a pie chart in the second column
                st.markdown('<div class="emoji-chart-container">', unsafe_allow_html=True)
                st.subheader("Emoji Usage Distribution")
                fig, ax = plt.subplots(figsize=(6, 6))

                # Plotting the pie chart for the top 5 emojis
                labels = [f"Emoji {i }" for i in range(len(top_emojis))]
                ax.pie(
                   top_emojis['Count'],
                   labels=labels,
                   autopct='%1.1f%%',
                   colors=top_emojis['Color'],
                   wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},  # Add border to the pie slices
                   textprops={'fontsize': 14, 'color': 'black'}
                )
                ax.set_title("Top Emojis", fontsize=18, color='#2E3A59')
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.write("No emojis found for the Selected User.")




               # Set up custom CSS for styling
                st.markdown("""
                    <style>
                    /* Body Styling */
                    body {
                        background-color: #f0f4f8;
                        font-family: 'Arial', sans-serif;
                    }
                    .title {
                        color: #FF6F61;
                        font-size: 36px;
                        font-weight: bold;
                        text-align: center;
                        padding-bottom: 20px;
                    }
                    .sentiment-title {
                        color: #2E3A59;
                        font-size: 26px;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }
                    .sentiment-description {
                        font-size: 18px;
                        color: #7F8C8D;
                        margin-bottom: 30px;
                    }
                    .sentiment-card {
                        padding: 15px;
                        border-radius: 10px;
                        background: linear-gradient(145deg, #f6f7f9, #e2e8f0);
                        box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.1), -3px -3px 6px rgba(255, 255, 255, 0.3);
                        margin-top: 20px;
                    }
                    .sentiment-card h3 {
                        font-size: 20px;
                        color: #FF6F61;
                    }
                    .sentiment-chart {
                        padding: 15px;
                        border-radius: 10px;
                        border: 2px solid #FF6F61;  /* Add border to the chart */
                        background-color: #fff;
                        box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.1);
                    }
                    .pie-chart {
                        border-radius: 10px;
                        border: 2px solid #FF6F61;  /* Add border to the pie chart */
                    }
                    .sentiment-bar {
                        color: #FF6F61;
                    }
                    .sentiment-label {
                        font-size: 14px;
                        color: #FF6F61;
                    }
                    .chart-container {
                        margin-top: 30px;
                    }
                   </style>
                   """, unsafe_allow_html=True)





            # Sentiment Analysis
            st.header("Sentiment Analysis")
            sentiment_df = Helper.sentiment_analysis(Selected_user, df)

            if not sentiment_df.empty:
                col1, col2 = st.columns(2)

                # Sentiment count and pie chart generation
                sentiment_counts = sentiment_df['sentiment'].value_counts()

                # Display overall sentiment counts
                with col2:
                    sentiment_html = """
                       '<br><br><p style="font-family:Roboto; color:#FF6F61; font-size: 20px; font-weight: bold">Sentiment Distribution </p>'

                        """
                # Display the sentiment distribution bar chart
                    st.markdown(sentiment_html, unsafe_allow_html=True)
                    st.markdown('<div class="sentiment-chart">', unsafe_allow_html=True)
                    st.bar_chart(sentiment_counts, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)


                # Display sentiment percentages
                with col1:
                    st.markdown('<div class="sentiment-chart pie-chart">', unsafe_allow_html=True)
                    st.subheader("Sentiment Percentage")
                    fig, ax = plt.subplots(figsize=(6, 6))
                    sentiment_counts.plot.pie(
                        autopct='%1.1f%%', labels=sentiment_counts.index, ax=ax,
                        colors=['#FF6F61', '#7F8C8A', '#8A2BE2']
                    )
                    ax.set_ylabel("")  # Hide y-axis label
                    ax.set_title("Sentiment Breakdown", fontsize=18, color='#2E3A67')
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("No sentiment data available for the selected user.")

            # Create a DataFrame for the analysis results to download
            analysis_results = {
                'Total Messages': [num_messages],
                'Total Words': [words],
                'Media Shared': [total_media],
                'Links Shared': [num_links],

            }
            analysis_df = pd.DataFrame(analysis_results)

            # Add download button for Show Analysis results (CSV)
            st.sidebar.subheader("Download Analysis Results")
            csv_analysis = analysis_df.to_csv(index=False)
            st.sidebar.download_button(
                label="Download Analysis Results CSV",
                data=csv_analysis,
                file_name="chat_analysis_results.csv",
                mime="text/csv"
            )

        # Add download button for the original file data CSV
        st.sidebar.subheader("Download Results")
        csv = df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download Full Data CSV",
            data=csv,
            file_name="chat_analysis_full_data.csv",
            mime="text/csv"
        )

# Text Emotion Detection Page
elif page == "Text Emotion Detection":
    # Load the pre-trained model
    pipe_lr = joblib.load(open("text_emotion.pkl", "rb"))

    emotions_emoji_dict = {
        "anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗", "joy": "😂",
        "neutral": "😐", "sad": "😔", "sadness": "😔", "shame": "😳", "surprise": "😮"
    }


    def predict_emotions(docx):
        results = pipe_lr.predict([docx])
        return results[0]


    def get_prediction_proba(docx):
        results = pipe_lr.predict_proba([docx])
        return results


    st.markdown("""
             <style>
             .center-header {
                 font-size: 50px;
                 color: #4CAF50;
                 font-weight: bold;
                 text-align: center;
             }
             </style>
             <p class="center-header">Text Emotion Detection</p>
         """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Text Emotion Detection</p>', unsafe_allow_html=True)
    st.subheader("Discover the emotion behind the text 📝")

    with st.form(key='my_form'):
        raw_text = st.text_area("Type your text here", height=200)
        submit_text = st.form_submit_button(label='Submit')

    if submit_text:
        col1, col2 = st.columns(2)
        prediction = predict_emotions(raw_text)
        probability = get_prediction_proba(raw_text)

        with col1:
            st.success("Original Text")
            st.write(raw_text)

            st.success("Emotion Prediction")
            emoji_icon = emotions_emoji_dict.get(prediction, "😐")
            st.markdown(f"""
                     <div style="font-size: 100px; text-align: center;">
                         {emoji_icon}
                     </div>
                     <h2 style="text-align: center;">{prediction.capitalize()}</h2>
                 """, unsafe_allow_html=True)

        with col2:
            st.success("Probability Score")
            prediction_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
            st.write(prediction_df)

            st.success("Emoji Analysis")
            emoji_frequency = dict(zip(pipe_lr.classes_, probability[0]))
            emoji_icons = [emotions_emoji_dict.get(emotion, "😐") for emotion in pipe_lr.classes_]
            st.bar_chart(emoji_frequency)

    st.markdown("---")
