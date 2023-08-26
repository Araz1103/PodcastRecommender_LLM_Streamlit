# A LLM Powered Podcast Recommender App

## This Streamlit app can be used to check, sort & like Podcasts, and this learns from the Liked Podcasts of a User and Generates tailored Recommendations along with explainations for why the user would love them!

### Introduction
Hi! This app was made as a project for an Uplimit Course of building products with OpenAI LLMs! This was a finalist out of 6500 submissions and won a shout out in front of Ted Sanders from OpenAI! :)

This ReadMe will help you understand the journey of creating such an App and how you can make your own!

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


