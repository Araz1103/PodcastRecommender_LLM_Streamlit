# A LLM Powered Podcast Recommender App

## This Streamlit app can be used to check, sort & like Podcasts, and this learns from the Liked Podcasts of a User and Generates tailored Recommendations along with explainations for why the user would love them!

---

### Introduction
Hi! This app was made as a project for an Uplimit Course of building products with OpenAI LLMs! This was a finalist out of 6500 submissions and won a shout out in front of Ted Sanders from OpenAI! :)

This ReadMe will help you understand the journey of creating such an App and how you can make your own!

---

### Structure of the Repository

#### App Dependencies

##### 1. `app.py`
This is the main code to host the app for Streamlit

##### 2. `Podcasts_Data.csv`
The data for Podcasts is present in this csv, and app.py loads the data from here! This can be modified if you want to add/edit the podcasts used in the App

##### 3. `requirements.txt`
All the libraries used to host the Streamlit app are present here. Note, this is different from the requirements for the other files for the functions to process the podcasts & make the OpenAI & Modal functions, in the Jupyter & Collab Notebooks mentioned below

#### Processing & Logic

##### 1. `Podcast Recommender App Data Preparation.ipynb`
This notebook parses through RSS Feeds of any Podcast, extracts the relevant information for the Streamlit App, and prepares the `Podcasts_Data.csv`. If you want to add/edit your own Podcasts for your App, you can use this notebook to prepare the data, and learn how to work with RSS Feeds!

##### 2. Podcasts Recommendation System & Quick Listen Features
In the Project, we used Modal Labs, to host all the functions for core recommendations and podcast summarisation. The below collab notebook goes in depth  on how they were made, the prompts used and  how to host your own functions with Modal Labs!

[Collab Notebook](https://colab.research.google.com/drive/13FTZih92XYLncRNQJVD7LCKOrltsoia-?usp=sharing)

---

### Concepts and Functions used in the Project

#### 1.   Transcribing a Podcast:

  A. Using Whisper Models from OpenAI (or WhisperX for faster inference) to transcribe

  B. Can use a RSS Feed to get the MP3 Audio of a Podcast

#### 2.   Quick Listen to a Podcast:

  A. Get the Highlights & Guests Present from a Podcast

  B. If it is within 14000 tokens, use transcription to get highlights & guests

  C. If it is greater than 14000 tokens, chunk it into portions, summarise each portion, concatenate summaries and get highlights & guests 

#### 3. Recommendations from Liked Podcasts

  A. Pass in the Liked Podcasts of User: Podcast Name, Episode Title & Summary 

  B. Pass in a list of Podcasts to choose from: Podcast Title & Summary 
  
  C. Get Top 10 Recommendations along with their reasons for the User

--- 

### Future Scope

#### 1. Use Whisper X for Transcribing a Podcast, and add the Quick Listen feature to show Highlights & Guests

#### 2. Use Embeddings from USE, MiniLM or any other Model, to fine tune the Recommendations for the User

#### 3. Take in a New RSS Feed as Input in the App, call the Data Processing Functions and expand the Podcast Selections for the User!

---

## I hope this was as fun for you as it was for me! Feel free to be creative and build on these ideas!

For any questions, reach out to me at arazsharma1103@gmail.com ! :)



