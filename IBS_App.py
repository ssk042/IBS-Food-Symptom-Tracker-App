import streamlit as st # streamlit lets use python to build app
from datetime import datetime, timedelta # dates and times for journal entry
import pandas as pd
import os

st.title("IBS Tracker") # big title

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["IBS Articles","FODMAP Search", "Food Journal", "Symptoms Tracker", "Patterns"]
    )

# articles section
with tab1:
    st.header("IBS Articles")

    articles = [
        {
            "title": "Irritable Bowel Syndrome",
            "summary": "Overview on Irritable Bowel Syndrome",
            "url": "https://www.ncbi.nlm.nih.gov/books/NBK534810/",
            "image": "https://1000logos.net/wp-content/uploads/2023/10/NIH-Logo.jpg"
        }, 
       {
            "title": "Irritable Bowel Syndrome",
            "summary": "IBS symptoms, causes, diagnosis, and treatment",
            "url": "https://www.mayoclinic.org/diseases-conditions/irritable-bowel-syndrome/symptoms-causes/syc-20360016",
            "image": "https://www.mayoclinichealthsystem.org/-/media/national-files/images/hometown-health/2016/2016-general/ibs_300x250.jpg?sc_lang=en"
        }, 
        {
            "title": "FODMAP Diet: What You Need to Know",
            "summary": "Discover how the FODMAP diet affects IBS",
            "url": "https://www.hopkinsmedicine.org/health/wellness-and-prevention/fodmap-diet-what-you-need-to-know",
            "image": "https://www.hopkinsmedicine.org/-/media/images/health/3_-wellness/gut-health/low-fodmap-teaser.jpg?mw=260&mh=155&hash=A131F62C0A44F2342CAC92ABFC02D87C"
        } 
    ]

    for article in articles:
        st.image(article["image"], use_container_width=True) # image fitting
        st.subheader(article["title"])
        st.write(article["summary"]) # st.write to display normal text
        st.markdown(f"[Read more]({article['url']})") # creates clickable link -> press read more to get to URL
        st.markdown("--------------------") # st.markdown for bold, italics, links, colored text, horizontal lines

#FODMAP Search
with tab2:
    st.header("Where do foods stand on the FODMAP diet?")
    st.write("""
    FODMAPs are short-chain carbohydrate sugars that are not fully absorbed in 
    the small intestine. Items high on FODMAP are generally avoided or eaten in 
    small quantities by those with IBS, whereas low FODMAP foods are considered 
    easier to digest.
    """)

    st.write("Search for an item to see its FODMAP!")

    # storing csv file in datafram variable 
    df = pd.read_csv("IBSFodmapData.csv")

    # search box to search for food
    userInputSearch = st.text_input("Search for a food: ")

    # looking up user search input if user searched anything
    if userInputSearch:
        # food column in csv and user input look compared
        # lower case to mitigate case sensitivity 
        match = df[df['Food'].str.lower() == userInputSearch.lower()]
            # datafram with matching rows is essentially returned 
       
       # if user searched a food that is in csv
        if not match.empty:
            # first matching result's level column is stored 
            fodLevel = match.iloc[0]['FODMAP Level']
            # cases:
            if fodLevel.lower() == "low":
                st.success(f"{userInputSearch.title()} is Low FODMAP")
            elif fodLevel.lower() == "high":
                st.error(f"{userInputSearch.title()} is High FODMAP")
            else:
                st.warning(f"{userInputSearch.title()} is Moderate FODMAP")
        else:
            st.info("""
            That food is not in data. Try typing its plural or 
            singular form. If it is still not appearing, you can request to add 
            it below.
            """)
            st.subheader("Request a Food to Be Added to our Records")

            # take food name requested + notes about the food
            foodRequested = st.text_input("Food Name ", value=userInputSearch)
            foodRequestedInfo = st.text_area("Any additional notes about this food?")

            if st.button("Submit Request"):
                # saving request to csv file
                if foodRequested.strip():
                    # loading request row in csv
                    request_df = pd.DataFrame({
                        "Requested Food:" : [foodRequested],
                        "Notes:" : [foodRequestedInfo]
                    })

                    # saving to csv file, appending 
                    if (os.path.exists("IBS_food_requested.csv") and 
                    os.path.getsize("IBS_food_requested.csv") > 0):
                        request_df.to_csv("IBS_food_requested.csv", mode="a", 
                                          header=False, index=False)
                    else:
                        request_df.to_csv("IBS_food_requested.csv", mode="w",
                                          header=True, index=False)
                
                st.success("Your request has been submitted and will be reviewed!")

    st.image("https://www.gastroconsa.com/wp-content/uploads/2019/09/Low-FODMAP-Diet-and-FODMAP-Foods.jpg")

# food journal section 
with tab3: 
    st.header("Log your food!") 

    date_current = datetime.now().date()
    # need to make more instances for breakfast, lunch, dinner, snack, and dessert
    
    st.subheader("Breakfast")
    # need keys to mitigate internal id issue for same text_input prompt
    bkfst_logged = st.text_input("What did you eat?", key="bkfst_input") 
    bkfst_time = st.time_input("When did you eat breakfast?") # 24 hr clock format
    # converting to 12 hr clock
    bkfst_time_12hr = bkfst_time.strftime("%I:%M %p") #12 hr clock format
    st.write("You ate breakfast at: ", bkfst_time_12hr)

    st.subheader("Snacks")
    # setting min val to 0 and increments by 1 each number, integer format
    snack_amount = st.number_input("How many snacks did you eat today?", 
                        min_value=0, step=1)
    i = 0
    snack_entries = []
    for i in range(int(snack_amount)):
        snacks_logged = st.text_input(f"What did you eat for snack #{i+1}?", key=f"snacks_input_{i}")
        snacks_time = st.time_input(f"When did you eat this snack #{i+1}?", key=f"snacks_time_{i}") # 24 hr clock format
        snacks_time_12hr = snacks_time.strftime("%I:%M %p")
        st.write(f"You ate snacks #{i+1} at: ", snacks_time_12hr)
        snack_entries.append((snacks_logged, snacks_time)) 
        # made into tuple, since append takes only one argument 

    st.subheader("Lunch")
    lunch_logged = st.text_input("What did you eat?", key="lunch_input") # text box 
    lunch_time = st.time_input("When did you eat lunch?") # 24 hr clock format
    lunch_time_12hr = lunch_time.strftime("%I:%M %p") 
    st.write("You ate lunch at: ", lunch_time_12hr)

    st.subheader("Dinner")
    dinner_logged = st.text_input("What did you eat?", key="dinner_input") # text box 
    dinner_time = st.time_input("When did you eat Dinner?") # 24 hr clock format
    dinner_time_12hr = dinner_time.strftime("%I:%M %p")
    st.write("You ate dinner at: ", dinner_time_12hr)

    st.subheader("Dessert")
    dessert_logged = st.text_input("What did you eat?", key="dessert_input") # text box 
    dessert_time = st.time_input("When did you eat Dessert?") # 24 hr clock format
    dessert_time_12hr = dessert_time.strftime("%I:%M %p")
    st.write("You ate dessert at: ", dessert_time_12hr)

    if st.button("Save Entry", key="save_entry"):
        food_entries = []

        if bkfst_logged.strip():
            food_entries.append({"Date": date_current, "Meal": "Breakfast", 
                "Food": bkfst_logged, "Time": bkfst_time.strftime("%I:%M %p")})
        
        for idx, (snacks_logged, snacks_time) in enumerate(snack_entries):
            if snacks_logged.strip():
                food_entries.append({"Date": date_current, "Meal": f"Snacks #{idx+1}", 
                "Food": snacks_logged, "Time": snacks_time.strftime("%I:%M %p")})

        if lunch_logged.strip():
            food_entries.append({"Date": date_current, "Meal": "Lunch", 
                "Food": lunch_logged, "Time": lunch_time.strftime("%I:%M %p")})  

        if dinner_logged.strip():
            food_entries.append({"Date": date_current, "Meal": "Dinner", 
                "Food": dinner_logged, "Time": dinner_time.strftime("%I:%M %p")})    

        if dessert_logged.strip():
            food_entries.append({"Date": date_current, "Meal": "Dessert", 
                "Food": dessert_logged, "Time": dessert_time.strftime("%I:%M %p")})  

        df = pd.DataFrame(food_entries)
        if os.path.exists("food_log.csv"):
            df.to_csv("food_log.csv", mode="a", header=False, index=False)
        else:
            df.to_csv("food_log.csv", mode="w", header=True, index=False)
        st.success("Your food entries have been saved!")

    if st.session_state.get("show_calendar", False): # if calendar view clicked
        st.subheader("Your Food Journal Calendar")


# symptom log section
with tab4: 
    st.header("Log your symptoms!")
    today_date = datetime.now().date()
    symptom_time = st.time_input("When did you experience the symptom?")

    symptoms = st.multiselect(
                "Which symptoms are you feeling?", 
                ["Bloating", "Cramping", "Constipation", "Diarrhea", "Nausea", "Fatigue", "Gas"]
                ) # select options stored as a list

    additional_triggers = st.text_area("Any additional triggers to note (ex: stress, insomnia)?")
    # big text area for customizable trigger input 

    if st.button("Save Entry", key="save_symptom_entry"):     # if symptom key button was clicked
        symptom_entry = {               # saving entry format
            "Date": today_date,     
            "Time": symptom_time.strftime("%I:%M %p"),
            "Symptoms": ", ".join(symptoms),
            "Triggers": additional_triggers
        }
        
        df_symptoms = pd.DataFrame([symptom_entry])
        if os.path.exists("symptom_log.csv"):
            df_symptoms.to_csv("symptom_log.csv", mode="a", header=False, index=False)
        else:
            df_symptoms.to_csv("symptom_log.csv", mode="w", header=True, index=False)
        st.success("Your symptoms have been logged")     # message to deliver

## at this point this is an interface (can interact with form on screen)
## no data is being stored, so all dissappears when app is closed/refreshed 

with tab5:
    st.header("Pattern Analysis")
    
    # loading food and symptom logs csv into dataframe
    if os.path.exists("food_log.csv") and os.path.exists("symptom_log.csv"):
        food_df = pd.read_csv("food_log.csv")   
        symptom_df = pd.read_csv("symptom_log.csv")

        # getting datetime objects in same format for food and symptoms csv 
        food_df['DateTime'] = pd.to_datetime(food_df['Date'] + ' ' + food_df['Time'],
                                                    format='%Y-%m-%d %I:%M %p')
        symptom_df['DateTime'] = pd.to_datetime(symptom_df['Date'] + ' ' + symptom_df['Time'], 
                                                    format='%Y-%m-%d %I:%M %p')

        matching_entries = [ ]

        # finding each time symptom in symptom log is experienced 
        for idx, symptom_row in symptom_df.iterrows():
            symptom_time = symptom_row['DateTime']  

            # filtering to look at foods eaten 5 hours before symptoms per entry
            # trying to detect foods that may cause symptoms over time
            recent_foods = food_df[(food_df['DateTime'] <= symptom_time) & 
                                    (food_df['DateTime'] >= symptom_time - timedelta(hours=5))]

            # from filtered recent_foods, looping through each food found 
            # appending each food-symptom matches to matching_entries list
            for fr_index, food_row in recent_foods.iterrows():
                matching_entries.append({
                    'Food': food_row['Food'],
                    'Symptom': symptom_row['Symptoms'],
                    'DateTime': symptom_time,
                    'Time Between (hrs)': round((symptom_time - food_row['DateTime'])
                                                        .total_seconds() / 3600, 2)
                })

        # turning matching_entries list into dataframe 
        # displaying dataframe table of matches
        if matching_entries:
            pattern_df = pd.DataFrame(matching_entries)
            st.write("Details of Food-Symptom Matches within 5 hours")
            # grouping table based on food and details
            groupedpattern_df = pattern_df.groupby("Food", as_index=False).agg({
                'Symptom': lambda x: ', '.join(x),
                'DateTime': lambda x: ', '.join(x.astype(str)),
                'Time Between (hrs)': lambda x: ', '.join(x.astype(str))
            })
            
            st.dataframe(groupedpattern_df)
            # st.dataframe(pattern_df.groupby('Food')['Symptom']['DateTime']['Time Between (hrs)'].apply(lambda x:x).str.cat(sep=" "))
            
            # splitting multiselect symptoms
            # using .explode to make new row for each individual symptom
            pattern_df = pattern_df.assign(Symptom=pattern_df['Symptom'].str.split(', ')).explode('Symptom')

            # new column pair in pattern dataframe has food-symptom combos
            pattern_df['Pair'] = pattern_df['Food'] + "->" + pattern_df['Symptom']
            
            # grouping the pairs number of occurences, adding count column
            # sorting by count descending
            pair_details = pattern_df.groupby('Pair').size().reset_index(name='Count').sort_values(by='Count', ascending=False)
            
            # filter dataframe where pair count has to be 2 or more 
            pair_details = pair_details[pair_details['Count'] > 1]
            # # occurence count of unique food-symptom combos, selecting top 10
            # pair_counts = pattern_df['Pair'].value_counts().head(10) 
            st.subheader("Most Frequent Food-Symptom Pairs")
            # displays pair counts as a bar chart
            # st.bar_chart(pair_counts)
            if not pair_details.empty:
                st.dataframe(pair_details)
                st.bar_chart(pair_details.set_index('Pair')['Count'])

            st.subheader("More Data Insights")
            # text box, removing spaces and standardizes to lowercase
            food_selected = st.text_input("Which food do you want to explore?").strip().lower()
            # sliders for 24 hr clock, initializing from 2-8pm 6 hr window
            starting_hour = st.slider("Starting Hour (24h)", 0, 23, 14)
            ending_hour = st.slider("Ending Hour (24h)", 0, 23, 20)

            # converting time col to datetime object, so not seen as a string
            food_df['Hour'] = pd.to_datetime(food_df['Time'], format="%I:%M %p").dt.hour
          
            # filtering by food selected by user, matching food name(s) and time window
            # accounts for if food is contained in text, i.e: rice in fried rice
            filtered_foods = food_df[
                (food_df['Food'].str.lower().str.contains(food_selected)) &
                (food_df['Hour'] >= starting_hour) &
                (food_df['Hour'] <= ending_hour)
            ]

            # merging foods with symptoms logged using inner join based on date
            filtered_merged = pd.merge(filtered_foods, symptom_df, on='Date', how='inner')

            # want to look at symptoms occuring within a 6 hr window
            # creating FoodDateTime and SymptomDateTime cols, combining Date and Time_x/y into a single string 
            # use pd to covert string to datetime obj of date and food eaten time/symptom time
            filtered_merged['FoodDateTime'] = pd.to_datetime(
                filtered_merged['Date'] + ' ' + filtered_merged['Time_x'],
                format='%Y-%m-%d %I:%M %p'
                )
            filtered_merged['SymptomDateTime'] = pd.to_datetime(
                filtered_merged['Date'] + ' ' + filtered_merged['Time_y'], 
                format='%Y-%m-%d %I:%M %p'
                )

            # users filter within how many hours post-food they are looking for symptoms
            # defaults to 6 hrs, but can slide between 1 and 24 
            time_window = st.number_input(
                "Select the window of hours after eating to look for symptoms:",
                min_value=1, max_value=24, value=6, step=1
            )

            # filters where symptom occurs during/after food is eaten base on user filter
            filtered_merged = filtered_merged[
                (filtered_merged['SymptomDateTime'] >= filtered_merged['FoodDateTime']) & 
                (filtered_merged['SymptomDateTime'] <= filtered_merged['FoodDateTime'] + pd.Timedelta(hours=time_window))
            ]          
          
            if not filtered_merged.empty:
                st.write(f"Filtered results for '{food_selected}' between {starting_hour}:00 and {ending_hour}:00")
                st.dataframe(filtered_merged[['Date', 'Food', 'Symptoms', 'Time_x', 'Time_y']])

                # visualization of symptom groupings
                symptom_groups = filtered_merged['Symptoms'].value_counts()
                st.bar_chart(symptom_groups)
            else:
                st.info("No entries found that match your filter")
          
          