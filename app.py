import streamlit as st
import pandas as pd
import json
import numpy as np
import modal

@st.cache_data
def get_podcasts_data():
    Podcasts_Data = pd.read_csv("Podcasts_Data.csv")
    Podcasts_Data['Episode Duration'] = Podcasts_Data['Episode Duration'].astype(int)
    return Podcasts_Data

def extract_json_from_text(text):
    try:
        start_index = text.find('{')
        end_index = text.rfind('}') + 1

        if start_index == -1 or end_index == 0:
            print("Error in Extracting JSON from LLM Output: No {} Brackets Found")
            return None  # JSON not found in the string

        # Extract the JSON portion from the string
        json_string = text[start_index:end_index]
        extracted_json = json.loads(json_string)
        return extracted_json
    except Exception as e:
        print(f"Error in Extracting JSON from LLM Output: {e}")
        return None
    
podcast_data = get_podcasts_data()
if "duration_filter" not in st.session_state:
    st.session_state.duration_filter = (0, 45)
    st.session_state.start_timestamp = pd.Timestamp("2023-01-01")
    st.session_state.end_timestamp = pd.Timestamp.now()
    st.session_state.search_keyword = ""
    st.session_state.podcast_category = "History Hit"
    st.session_state.filtered_podcasts = pd.DataFrame()  # Initialize with an empty DataFrame

# Initialize liked podcasts using session state
if 'liked_podcasts' not in st.session_state:
    st.session_state.liked_podcasts = set()

if 'current_recommendations' not in st.session_state:
    st.session_state.current_recommendations = []

def get_podcast_from_titles(title_list):
    filtered_rows = podcast_data[podcast_data['Episode Title'].isin(title_list)]
    podcast_dict = filtered_rows.to_dict(orient='records')
    return podcast_dict

def sample_podcasts_with_exclusion(excluded_titles, sample_size):
    # Filter the DataFrame to exclude rows with specified titles
    filtered_dataframe = podcast_data[~podcast_data['Episode Title'].isin(excluded_titles)]
    
    # Sample rows from the filtered DataFrame
    sampled_rows = filtered_dataframe.sample(n=sample_size, random_state=42)  # You can change the random_state if needed
    
    # Convert the sampled rows to a list of dictionaries
    sampled_dict_list = sampled_rows.to_dict(orient='records')
    
    return sampled_dict_list

def data_for_recommendations(Like_Podcast_Data, Sample_Podcast_Data):
    liked_podcasts = """"""
    for podcast in Like_Podcast_Data:
        podcast_duration = f"{podcast['Episode Duration']} Minutes"
        liked_podcasts += f"'Liked Title': {podcast['Episode Title']}  'Liked Summary': {podcast['Episode Summary']} 'Liked Duration': {podcast_duration}"
        liked_podcasts += "\n\n"
        
    sample_podcasts = """"""
    for podcast in Sample_Podcast_Data:
        podcast_duration = f"{podcast['Episode Duration']} Minutes"
        sample_podcasts += f"'Title': {podcast['Episode Title']}  'Summary': {podcast['Episode Summary']} 'Duration': {podcast_duration}"
        sample_podcasts += "\n\n-----------------------------------------------------------------------------------------\n\n"
    
    return liked_podcasts, sample_podcasts

def apply_filters():
    print(st.session_state)
    filtered_podcasts = podcast_data[
        (podcast_data['Episode Duration'] >= st.session_state.duration_filter[0]) &
        (podcast_data['Episode Duration'] <= st.session_state.duration_filter[1]) &
        (pd.to_datetime(podcast_data['Episode Date'], format='%d/%m/%Y') >= np.datetime64(st.session_state.start_timestamp)) &
        (pd.to_datetime(podcast_data['Episode Date'], format='%d/%m/%Y') <= np.datetime64(st.session_state.end_timestamp)) &
        (podcast_data['Podcast Name'] == st.session_state.podcast_category) & # Filter by Podcast Category
        (podcast_data['Episode Title'].str.contains(st.session_state.search_keyword, case=False))
    ]
    st.session_state.filtered_podcasts = filtered_podcasts


# Filter and display podcasts based on user's selections
def display_sidebar():
    st.sidebar.subheader("Change or Interact with Filters to see Podcasts!!")
    # Filter by Duration
    st.sidebar.subheader("Filter by Duration (minutes)")
    duration_filter = st.sidebar.slider("", 0, 45, key="duration_filter")
    
    # Filter by Published Date
    st.sidebar.subheader("Filter by Published Date")
    start_date = st.sidebar.date_input("Start Date", key="start_timestamp")
    end_date = st.sidebar.date_input("End Date", key="end_timestamp")

    # Convert start and end date to pandas Timestamp objects
    start_timestamp = pd.Timestamp(start_date)
    end_timestamp = pd.Timestamp(end_date)

    # Filter by Podcast Category
    st.sidebar.subheader("Filter by Podcast Name")
    podcast_categories = podcast_data['Podcast Name'].unique()
    selected_category = st.sidebar.selectbox("Select Podcast", podcast_categories, key="podcast_category")

    # Filter by Keyword
    st.sidebar.subheader("Filter by Keyword")
    search_keyword = st.sidebar.text_input("Enter keyword", key="search_keyword")

    st.sidebar.subheader("Click here to Check & Listen your Liked Podcasts!")
    like_button = st.sidebar.button("Liked Podcasts", key="like_button")
    
    st.sidebar.subheader("Recommendations based on Liked Podcasts")
    st.sidebar.write("Click the button to show recommendations:")
    show_recommendations = st.sidebar.button("Show Recommendations", key="show_recommendations")

    st.sidebar.write("Click the button to generate recommendations:")
    generate_new_recommendations = st.sidebar.button("Generate Recommendations", key="generate_new_recommendations")

def change_like_status(current_status_key, row):
    if current_status_key in st.session_state:
        current_status = st.session_state[current_status_key]
        if current_status:
            st.session_state.liked_podcasts.add(row)
        else:
            st.session_state.liked_podcasts.discard(row)

def main():
    st.title("Podcasts App")

    # Sidebar for filters
    display_sidebar()

    if st.session_state.like_button:
        if st.session_state.liked_podcasts:
            # Replace this with the format you want for liked podcasts
            st.write("## Your Liked Podcasts :")
            liked_podcasts_list = get_podcast_from_titles(st.session_state.liked_podcasts)
            for podcast in liked_podcasts_list:
                st.write(f"### {podcast['Podcast Name']} - {podcast['Episode Title']}")
                expander = st.expander("### Check it out:")
                with expander:
                    st.write(f"Podcast: {podcast['Podcast Name']}")
                    st.write(f"Title: {podcast['Episode Title']}")
                    st.write(f"Summary: {podcast['Episode Summary']}")
                    try:
                        st.markdown(f"[Click here to listen]({podcast['Episode Audio']}) 🔈")
                    except Exception as e:
                        print(f"Can't Render Audio Link: {e}")
                    if podcast['Podcast Image']:
                        try:
                            st.image(f"{podcast['Podcast Image']}", use_column_width=True)
                        except Exception as e:
                            print(f"Can't Open Image: {e}")
                st.markdown("""---""")
            
        else:
            st.write("## Hey you haven't liked any Podcasts yet! Click on the Filters to view some now! :)")

    elif st.session_state.generate_new_recommendations:

        if len(st.session_state.liked_podcasts) >= 3:
            
            if len(st.session_state.liked_podcasts) <= 5:
                num_to_sample = 45
            else:
                num_to_sample = 50 - len(st.session_state.liked_podcasts)
            
            Liked_Podcasts = get_podcast_from_titles(list(st.session_state.liked_podcasts)[-10:])
            Sample_Podcasts = sample_podcasts_with_exclusion(list(st.session_state.liked_podcasts)[-10:], num_to_sample)
            #st.write(Liked_Podcasts)
            #st.write(Sample_Podcasts)
            liked_podcasts_data, sample_podcasts_data = data_for_recommendations(Liked_Podcasts, Sample_Podcasts)
            #st.write(liked_podcasts_data)
            #st.write(sample_podcasts_data)

            # Replace this with the format you want for recommendations
            recommendations = """### We saw your liked Podcasts! We would love to suggest you some new ones!\n\n"""
            st.write(recommendations)
            st.write(" ### Wait Approximately 1 minute for Recommendations to be Generated!\n\n")
            st.write("### Take a Deep Breath, and Meditate! We'll let you know as soon as they are ready!\n\n")

            st.write("### IMPORTANT Note: Please wait here while they generate and do not Interact with App!!\n\n")

            # Display loader while generating
            with st.spinner("## Loading..."):
                print("GENERATIMG!!")
                got_recs = False
                try:
                    f = modal.Function.lookup("corise-podcast-project", "get_podcast_recommendations")
                    podcast_recommendations_output = f.call(liked_podcasts_data, sample_podcasts_data)
                    print(f"OP Recommendations: {podcast_recommendations_output}")
                    podcast_json = extract_json_from_text(podcast_recommendations_output)
                    
                    if podcast_json:
                        if type(podcast_json)==dict:
                            if podcast_json.get('Recommendations', []):
                                st.session_state.current_recommendations = podcast_json.get('Recommendations', [])
                                got_recs = True
                            elif podcast_json[list(podcast_json.keys())[0]]:
                                st.session_state.current_recommendations = podcast_json[list(podcast_json.keys())[0]]
                                got_recs = True

                    #time.sleep(30)
                except Exception as e:
                    print(f"Error in Generating Recommendations!: {e}")

            if got_recs:
                st.success("### They are Ready!! Click on Show Recommendations!!")
            else:
                st.warning("### Sorry, Error in Generating Recommendations! Try Later!")
            
        else:
            st.write("### Sorry! Please Like at Least 3 Podcasts to Generate Recommendations!")

    elif st.session_state.show_recommendations:
        if st.session_state.current_recommendations:
            st.write("## Here are your Latest Recommendations!\n\n")
            if type(st.session_state.current_recommendations)==list:
                recommendations = st.session_state.current_recommendations
                try:
                    all_titles = [rec["Title for Recommendation"] for rec in recommendations]
                    all_reasons = {}
                    for rec in recommendations:
                        all_reasons[rec["Title for Recommendation"]] = rec["Reason for Recommendation"]

                    recommended_podcasts = get_podcast_from_titles(all_titles)
                    for podcast in recommended_podcasts:
                        st.write(f"### {podcast['Podcast Name']} - {podcast['Episode Title']}")
                        st.write(f"### Reason we believe you will love this Podcast:")
                        st.write(all_reasons[podcast['Episode Title']])

                        expander = st.expander("### Check it out:")
                        with expander:
                            st.write(f"Podcast: {podcast['Podcast Name']}")
                            st.write(f"Title: {podcast['Episode Title']}")
                            st.write(f"Summary: {podcast['Episode Summary']}")
                            try:
                                st.markdown(f"[Click here to listen]({podcast['Episode Audio']}) 🔈")
                            except Exception as e:
                                print(f"Can't Render Audio Link: {e}")
                            if podcast['Podcast Image']:
                                try:
                                    st.image(f"{podcast['Podcast Image']}", use_column_width=True)
                                except Exception as e:
                                    print(f"Can't Open Image: {e}")
                        st.markdown("""---""")
                except Exception as e:
                    print(f"Error in Recommendations Format: {e}")
                    st.write(recommendations)

            else:
                st.write(st.session_state.current_recommendations)

        else:
            st.write("### Sorry! Please Generate Recommendations!")
    
    else:
        st.write("### Podcasts Available Based on Filters")
        apply_filters()
        filtered_results = st.session_state.filtered_podcasts
        if not filtered_results.empty:
            # Loop through filtered podcasts and display expanders
            for idx, row in st.session_state.filtered_podcasts.iterrows():
                expander = st.expander(f"{row['Podcast Name']} - {row['Episode Title']}")
                with expander:
                    st.write(f"Podcast: {row['Podcast Name']}")
                    st.write(f"Title: {row['Episode Title']}")
                    st.write(f"Summary: {row['Episode Summary']}")
                    
                    default_liked_status = row['Episode Title'] in st.session_state.liked_podcasts
                    liked = expander.checkbox("Like this podcast?", default_liked_status, key=f"like_{row['Episode Title']}", on_change=change_like_status, args=[f"like_{row['Episode Title']}", row['Episode Title']])
                    if liked:
                        st.success(f"Added '{row['Episode Title']}' to liked podcasts!")
                    
                    try:
                        st.markdown(f"[Click here to listen]({row['Episode Audio']}) 🔈")
                    except Exception as e:
                        print(f"Can't Render Audio Link: {e}")
                    if row['Podcast Image']:
                        try:
                            st.image(f"{row['Podcast Image']}", use_column_width=True)
                        except Exception as e:
                            print(f"Can't Open Image: {e}")
                    
        else:
            st.write("### No results match your search criteria.")


if __name__ == "__main__":
    main()
