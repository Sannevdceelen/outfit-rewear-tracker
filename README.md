# Outfit Rewear Tracker

## Student Name
Sanne van der Ceelen

## App Description
The Outfit Rewear Tracker is a Streamlit web application that helps users track what they wear daily. Users can log their outfits, upload images, and monitor how often and when each outfit is worn.

The app also allows users to upload their closet and receive outfit recommendations based on items they already own, encouraging more variety and smarter wardrobe use.

## Target Users
This app is intended for individuals interested in fashion and wardrobe management. It is especially useful for students and young professionals who want to create more outfit variety without buying new clothes.

## Features
- Add and manage closet items (with images)
- Delete closet items
- Log daily outfits with images
- Track how many times each outfit is worn
- Track when each outfit was worn (dates)
- View outfit history
- Get outfit recommendations based on your closet
- Persistent cloud storage for all data and images

## How to Use the App
1. Go to **Add Closet Item** to upload your clothing items and images  
2. Go to **Closet Overview** to view or delete items  
3. Use **Log Daily Outfit** to record what you wore and upload a photo  
4. Check **Outfit History** to see wear frequency and dates  
5. Use **Recommendations** to get outfit ideas from your closet  

## Data Storage
This app uses **Supabase** for cloud-based storage:

- Closet items and outfit data are stored in a Supabase database  
- Images are stored in a Supabase Storage bucket  
- This ensures that all data and uploaded images persist across sessions, even in the deployed app  

## Deployed App
https://outfit-rewear-tracker-svdc.streamlit.app/

## GitHub Repository
https://github.com/Sannevdceelen/outfit-rewear-tracker

## Reflection

### What does your app do?
The app allows users to track their outfits, monitor wear frequency, and get outfit recommendations based on their existing wardrobe. It helps users become more aware of their clothing usage and encourages more variety.

### Who is it for?
The app is designed for people who are interested in fashion and want to manage their wardrobe more effectively, especially those who want to avoid over-wearing certain outfits.

### What was the most difficult part?
The most difficult part was implementing persistent storage for both data and images in the deployed app. This required integrating Supabase and setting up proper database and storage permissions.

### What did you learn from this project?
I learned how to build an interactive Streamlit application, manage user input, and work with external services like Supabase to store and retrieve data in a cloud environment.

### What would you improve if you had more time?
I would improve the recommendation system by making it more advanced (for example based on colors or style combinations), and enhance the user interface to make the app even more visually appealing.
