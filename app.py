from flask import Flask, request, jsonify, send_from_directory
import subprocess
from datetime import datetime
import pyjokes
import wikipedia
import os
import webbrowser
import requests  # For weather and news commands
import re
import psutil
import speedtest

  
app = Flask(__name__)

# Function to get the greeting based on the time of day
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

# Serve the frontend
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Handle commands from the frontend
@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command').lower()
    response = ""

    # Command 1: Open Notepad
    if "open notepad" in command:
        subprocess.run(["notepad.exe"])
        response = "Notepad opened."
    
    # Command 2: Get the current time
    elif "time" in command:
        time_str = datetime.now().strftime('%I:%M %p')
        response = f"The current time is {time_str}."

    # Command 3: Tell a joke
    elif "joke" in command:
        response = pyjokes.get_joke()

    elif "battery status" in command:
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                response = f"Battery is at {percent}%."
            else:
                response = "Battery information not available."
        except Exception as e:
            response = "Could not check battery status."
        
    elif "internet speed" in command:
        st = speedtest.Speedtest()
        download = st.download() / 1_000_000  # Convert to Mbps
        upload = st.upload() / 1_000_000
        response = f"Download speed: {download:.2f} Mbps, Upload speed: {upload:.2f} Mbps."

        
    # Command 4: Search Wikipedia
    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            response = f"According to Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            response = "There are multiple matches. Please be more specific."
        except wikipedia.exceptions.PageError as e:
            response = "Sorry, I couldn't find any information on that topic."

    # Command 5: Open YouTube
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube."

    # Command 6: Open Google
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        response = "Opening Google."
        
     
    elif "alien language" in command:
        response = """
        Beep boop! Zorp blorp glorp! Translation: Hello, human! How can I assist you today? 👽
        Xar noob shka'tar! Vee klorp zenthoor! Translation: I greet you in the stars' language, traveler.
        Ploxyn thrin! Drak'ka dorvash! Translation: The cosmos speaks in many tongues, but I understand you.
        Bloop bloop! Glik glik plorp! Translation: I am out of coffee, send help!
        Kreeek! Zik zoop! Translation: I told you I didn’t want pineapple on my space pizza!
        """

    # Command 7: Play music
    elif "play music" in command:
        music_dir = "C:\\music"  # Replace with your music directory
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
            response = "Playing music."
        else:
            response = "No music files found."

    # Command 8: Shutdown the system
    elif "shutdown" in command:
        response = "Shutting down the system."
        os.system("shutdown /s /t 1")  # Windows shutdown command

    # Command 9: Get the weather
    elif "weather" in command:
        city = command.replace("weather", "").strip()
        if city:
            api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your API key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            try:
                data = requests.get(url).json()
                weather = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                response = f"The weather in {city} is {weather} with a temperature of {temperature}°C."
            except Exception as e:
                response = "Sorry, I couldn't fetch the weather information."
        else:
            response = "Please specify a city."

    # Command 10: Get the latest news
    elif "news" in command:
        api_key = "178ccff7709d41e891b323376200706e"  # Replace with your API key
        url = f"http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey={api_key}"
        try:
            data = requests.get(url).json()
            articles = data["articles"][:3]  # Get top 3 headlines
            headlines = [article["title"] for article in articles]
            response = "Here are the latest news headlines: " + ". ".join(headlines)
        except Exception as e:
            response = "Sorry, I couldn't fetch the news."

    # Command 11: Open Calculator
    elif "open calculator" in command:
        subprocess.run("calc.exe")
        response = "Opening calculator."

    # Command 12: Open Camera
    elif "open camera" in command:
        subprocess.run("start microsoft.windows.camera:", shell=True)
        response = "Opening camera."

    # Command 13: Restart the system
    elif "restart" in command:
        response = "Restarting the system."
        os.system("shutdown /r /t 1")  # Windows restart command

    # Command 14: Open Task Manager
    elif "open task manager" in command:
        subprocess.run("taskmgr")
        response = "Opening Task Manager."

    # Command 15: Open Settings
    elif "open settings" in command:
        subprocess.run("start ms-settings:", shell=True)
        response = "Opening settings."

    # Command 16: Open College Website
    elif "open my college website" in command:
        webbrowser.open("https://jessbpjunnar.org/b-sc-it-home/")  # Replace with your college website URL
        response = "Opening your college website."

    # Command 17: Get the current date
    elif "date" in command:
        date_str = datetime.now().strftime('%B %d, %Y')  # Format: Month Day, Year
        response = f"Today's date is {date_str}."

    # Command 18: Open Instagram
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        response = "Opening Instagram."

    # Command 19: Open Facebook
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        response = "Opening Facebook."

    # Command 20: Open GitHub
    elif "open github" in command:
        webbrowser.open("https://github.com")
        response = "Opening GitHub."

    # Command 21: Open Twitter
    elif "open twitter" in command:
        webbrowser.open("https://www.twitter.com")
        response = "Opening Twitter."

    # Command 22: Open LinkedIn
    elif "open linkedin" in command:
        webbrowser.open("https://www.linkedin.com")
        response = "Opening LinkedIn."
    
     # Command 23: Open Reddit
    elif "open reddit" in command:
        webbrowser.open("https://www.reddit.com")
        response = "Opening Reddit."

    # Command 24: Open WhatsApp Web
    elif "open whatsapp web" in command:
        webbrowser.open("https://web.whatsapp.com")
        response = "Opening WhatsApp Web."

    # Command 25: Open Gmail
    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")
        response = "Opening Gmail."
    
    #command 26: article
    elif "random wikipedia article" in command:
        random_page = wikipedia.random(pages=1)
        summary = wikipedia.summary(random_page, sentences=2)
        response = f"Here's a random Wikipedia article: {random_page}. Summary: {summary}"
    
    elif "tell me a fun fact" in command:
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        try:
            data = requests.get(url).json()
            fun_fact = data["text"]
            response = f"Here's a fun fact: {fun_fact}"
        except Exception as e:
            response = "Sorry, I couldn't fetch a fun fact at the moment."
        
    elif "set a reminder" in command:
        reminder = command.replace("set a reminder", "").strip()
        if reminder:
            response = f"Reminder set: '{reminder}'. I'll remind you later!"
        else:
            response = "Please specify a reminder."
    
    elif "play random youtube video" in command:
        search_query = "random"
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        response = "Playing a random YouTube video."
          
    elif "show me a meme" in command:
        url = "https://meme-api.com/gimme"
        try:
            data = requests.get(url).json()
            meme_url = data["url"]
            webbrowser.open(meme_url)
            response = "Here's a random meme for you!"
        except Exception as e:
            response = "Sorry, I couldn't fetch a meme at the moment."
    
    elif "play random podcast" in command:
        webbrowser.open("https://www.listennotes.com/random-podcast/")
        response = "Opening a random podcast."
            
    # Command 26: Open Pinterest
    elif "open pinterest" in command:
        webbrowser.open("https://www.pinterest.com")
        response = "Opening Pinterest."

    # Command 27: Open Netflix
    elif "open netflix" in command:
        webbrowser.open("https://www.netflix.com")
        response = "Opening Netflix."

    # Command 28: Open Amazon
    elif "open amazon" in command:
        webbrowser.open("https://www.amazon.com")
        response = "Opening Amazon."

    # Command 29: Open Spotify
    elif "open spotify" in command:
        webbrowser.open("https://www.spotify.com")
        response = "Opening Spotify."

    # Command 32: Open Discord
    elif "open discord" in command:
        webbrowser.open("https://discord.com")
        response = "Opening Discord."

    # Command 33: Search on Google
    elif "search google" in command:
        query = command.replace("search google", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            response = f"Searching for '{query}' on Google."
        else:
            response = "Please specify a search query."

    # Command 34: Search on YouTube
    elif "search youtube" in command:
        query = command.replace("search youtube", "").strip()
        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            response = f"Searching for '{query}' on YouTube."
        else:
            response = "Please specify a search query."

    # Command 35: Open File Explorer
    elif "open file explorer" in command:
        subprocess.run("explorer")
        response = "Opening File Explorer."

    # Command 38: Launch Visual Studio Code
    elif "open visual studio code" in command:
        subprocess.run("code")
        response = "Opening Visual Studio Code."


    # Command 40: Display System Information
    elif "system info" in command:
        system_info = subprocess.check_output("systeminfo", shell=True).decode()
        response = f"System Information:\n{system_info}"

    # Command 41: Lock the System
    elif "lock system" in command:
        subprocess.run("rundll32.exe user32.dll,LockWorkStation")
        response = "Locking the system."

     # Command 42: Open Firefox
    elif "open firefox" in command:
        webbrowser.open("https://www.mozilla.org/en-US/firefox/new/")
        response = "Opening Firefox."
        
    # Command 70: Open Flipkart
    elif "open flipkart" in command:
        webbrowser.open("https://www.flipkart.com")
        response = "Opening Flipkart."

    # Command 71: Open Online Game (e.g., Miniclip)
    elif "open online game" in command:
        webbrowser.open("https://www.miniclip.com/games/en/")
        response = "Opening Miniclip online games."
               
    # Command 82: Get Motivational Quote
    elif "get motivational quote" in command:
        url = "https://zenquotes.io/api/random"
        try:
            response = requests.get(url)
            quote_data = response.json()
            quote = quote_data[0]["q"]
            author = quote_data[0]["a"]
            response = f"Here’s your motivational quote: \n'{quote}' \n- {author}"
        except Exception as e:
            response = "Sorry, I couldn't fetch the motivational quote at the moment."
            
    # Command 86: Search for Jobs
    elif "search for jobs" in command:
        job_title = command.replace("search for jobs", "").strip()
        if job_title:
            url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}"
            webbrowser.open(url)
            response = f"Searching for {job_title} jobs on LinkedIn."
        else:
            response = "Please specify a job title."
    
    
     # Command 87: Calculate Mathematical Sum
    elif "calculate" in command or "sum" in command:
        # Remove extra spaces and try to capture the math expression
        expression = command.replace("calculate", "").replace("sum", "").strip()

        # Basic validation to ensure it contains only numbers and math operators
        if re.match(r'^[\d\+\-\*\/\.\(\) ]+$', expression):
            try:
                # Evaluate the mathematical expression safely
                result = eval(expression)
                response = f"The result of {expression} is {result}."
            except Exception as e:
                response = "There was an error in calculating the expression. Please check your input."
        else:
            response = "Invalid expression. Please enter a valid mathematical expression."


    # Default response for unrecognized commands
    else:
        response = "Command not recognized."

    return jsonify({"response": response})

# Run the Flask app
if __name__ == "__main__":
    # Greet the user when the app starts
    greeting = get_greeting()
    print(f"{greeting}, I am FRIDAY.")
    app.run(debug=True)
