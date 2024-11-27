from PIL import Image
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from auth import signup_user, login_user, reset_password  # Import reset_password function
from Preprocessor import preprocess
from Helper import fetch_stats
import Helper

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
           text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.7);  /* Stronger black shadow */
           letter-spacing: 1px;  /* Adds a bit of spacing between letters */
}


    </style>
    """,
    unsafe_allow_html=True,
)



# Create Navigation Sidebar
st.sidebar.title("Latent Emotion Detection")
page = st.sidebar.radio("Navigation", ["User Guide", "Login", "Signup", "Forgot Password", "File Upload", "Analysis"])

# Sidebar icon (optional)
st.sidebar.image("analy.png", use_container_width=True)

# User Guide Page
if page == "User Guide":
    st.title("📘 User Guide")

    # Add the Emotion-Detection.png image only on the User Guide page
    st.image("emoji.jpg", use_container_width=True)

    st.markdown(
        """
        <h2 style="color:#3E64FF;">Welcome to Latent Emotion Detection!</h2>
        <p>
        This app allows you to analyze your WhatsApp chats and generate insights about emotions, activity trends, and more.
        </p>
        """,
        unsafe_allow_html=True,
    )
    # Steps to Use the App
    st.markdown(
        """
        <h3 style="color:#3498db;">How to Use:</h3>
        <ul style="color:#2c3e50; line-height: 1.8;">
            <li><b style="color:#e74c3c;">Signup:</b><span style="color:#ffffff;"> Create your account to access features.</span></li>
            <li><b style="color:#8e44ad;">Login:</b><span style="color:#ffffff;"> Securely log in with your credentials.</span></li>
            <li><b style="color:#16a085;">Upload:</b><span style="color:#ffffff;"> Upload your WhatsApp text file for processing.</span></li>
            <li><b style="color:#f39c12;">Analyze:</b><span style="color:#ffffff;"> Gain insights into your chat data.</span></li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    # Additional Details and Features
    st.subheader("Features")
    st.write("""- **User-based Analysis**: Analyze data for individual users or the overall chat.
                - **Statistics**: View total messages, words, media shared, and links shared.
                - **Monthly Timeline**: See the message activity trend over time.""")

    # Instructions for Exporting Data
    st.subheader("How to Export Data")
    st.write("""After analyzing your chat data, you can export the results to a file for further use.""")

    # Additional Guidelines
    st.subheader("Guidelines")
    st.write("""- Ensure the WhatsApp chat file is in **text format** and not corrupted.
                - The app works best with **clean data**. It's recommended to clean your chat export.""")

# Login Page
elif page == "Login":
    st.title("Login Page")

    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
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

    if st.button("Reset Password"):
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

        # Open and resize the GIF using PIL
        img = Image.open('thankyou.gif')
        img = img.resize((800, 300))  # Resize to desired dimensions

        # Display the resized GIF
        st.image(img)

# Analysis Page
elif page == "Analysis":
        if 'logged_in' in st.session_state and st.session_state['logged_in']:
            if 'uploaded_file' in st.session_state:
                uploaded_file = st.session_state.uploaded_file
                st.title("Data Analysis")
                try:
                    # Decode the uploaded file
                    bytes_data = uploaded_file.getvalue()
                    data = bytes_data.decode("utf-8")

                    # Preprocess the data
                    df = preprocess(data)

                    if 'user' in df.columns:
                        # Add your analysis logic here...
                        st.success("Analysis Complete! View the results below.")

                        # Show dataframe only if it exists
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
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

            # Word Cloud
            st.title('Wordcloud')
            df_wc = Helper.create_wordcloud(Selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # most common words
            most_common_df = Helper.most_common_words(Selected_user, df)

            fig, ax = plt.subplots()

            ax.barh(most_common_df[0], most_common_df[1])

            plt.xticks(rotation='vertical')

            st.title('Most commmon words')
            st.pyplot(fig)

            # Emoji analysis

            # helper.emoji_helper returns a list of emojis and their counts
            emoji_df = Helper.emoji_helper(Selected_user, df)

            st.title("Emoji Analysis")
            st.image('91636.jpg', width=700)

            # Define specific colors for the top 5 emojis
            color_mapping = {
                0: 'red',  # Color for the 1st top emoji
                1: 'blue',  # Color for the 2nd top emoji
                2: 'green',  # Color for the 3rd top emoji
                3: 'orange',  # Color for the 4th top emoji
                4: 'violet',  # Color for the 5th top emoji
            }
            # Create two columns for the display
            col1, col2 = st.columns(2)

            with col1:
                # Create a DataFrame for the top 5 emojis and their colors
                if not emoji_df.empty:
                    # Get top 5 emojis by count
                    top_emojis = emoji_df.nlargest(5, 'Count')

                    # Assign colors from the color mapping
                    top_emojis['Color'] = [color_mapping[i] for i in range(len(top_emojis))]

                    # Display the emoji dataframe in the first column
                    st.dataframe(top_emojis[['Emoji', 'Count', 'Color']])

            with col2:
                # Create a pie chart in the second column
                if not emoji_df.empty:
                    fig, ax = plt.subplots()

                    # Extract colors for the top 5 emojis
                    colors = top_emojis['Color'].tolist()

                    # Plotting the top 5 emojis by count
                    ax.pie(top_emojis['Count'], autopct='%1.1f%%', colors=colors)
                    st.pyplot(fig)
                else:
                    st.write("No emojis found for the Selected User.")

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
            csv_analysis = analysis_df.to_csv(index=False)  # Convert analysis results to CSV
            st.sidebar.download_button(
                label="Download Analysis Results CSV",
                data=csv_analysis,
                file_name="chat_analysis_results.csv",
                mime="text/csv"
            )

        # Add download button for the original file data CSV
        st.sidebar.subheader("Download Results")
        csv = df.to_csv(index=False)  # Convert DataFrame to CSV
        st.sidebar.download_button(
            label="Download Full Data CSV",
            data=csv,
            file_name="chat_analysis_full_data.csv",
            mime="text/csv"
        )
