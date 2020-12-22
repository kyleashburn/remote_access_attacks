# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

# programmer: Kyle Ashburn
# project: Remote Access Attack Log File Transformation
# project description: takes a windows log file and distills it to just the stuff I'm interested in. It is slow and probably too brute force, but it works and the dataset is truly massive.
# Once it's got the stuff I'm interested in, it outputs it as a json formatted txt file. In the process, it goes from a 8gb file to around a 800 mb file. 
# last changes: 12/21/2020
# change log:  changes consisted of cleaning up the script and formatting it properly. 



# importing the neccessary libraries
import re
import time as t
import json

# initializing the variables
line_counter = 0
date_count = 0
event_counter = 0
start_time = t.time()

date = ""
flag = False


key = ""
key_list = ["Workstation Name", "Source Network Address","Key Length", "Security ID", "Account Name"]
value = ""

matched = False
flag_match = False
other_match = False

event_dict = {}
date_test = {}
dbl_count = 0

# reading in the textfile with all of the log files that were failures.
with open("all_the_failures.txt", "r", encoding='utf-8') as line_in:
    for line in line_in:
        
        # incrementing a counter to track how many lines of the file have been processed
        line_counter += 1
        
        
        # running a regex to match dates
        date_match = re.search(r"\d*/\d*/\d* \d*:\d*:\d* [PA]M",line)
               
        # if there's a date, then we go through
        if date_match:
            date_count = line_counter
            date = date_match.group()
            event_counter += 1
            event_dict.setdefault(event_counter, {}).setdefault(date, {})
            
            # creating an entry for the date if it doesn't exist in the json structure yet           
            if date not in date_test:
                date_test.setdefault(date, "test")
            
            # incrementing a counter if the date has occured before
            else:
                dbl_count += 1
            
            flag = False
        
        # regex looking for the structure of the information for the log entries
        other_match = re.search(r"\t(.*):\t(.*)",line)
        
        # regex looking for the account information
        flag_match = re.search(r"Account For Which Logon Failed:", line)
        
        # testing if there is a match of the flags
        if flag_match:
            flag = True
        
        # testing if there is a match of the flag condition
        # if there is, it checks if there is a match of the structure of the info from the log entry
        # if there is, then it goes ahead and creates a dict entry for it
        if other_match and flag ==True:
            key = other_match.group(1)
            value = other_match.group(2).strip()
            
            if key in key_list:
                #print(key, "\t", value)
                event_dict[event_counter].setdefault(date, {}).setdefault(key, value)
                
                   
            
# writing the reduced log file to a new file -> it's a json file
# structure is line #(log entry) as a key with the date as another key to a dictionary with the elements of the log entry as keys with their values as values.
with open('checking.txt', 'w') as outfile:
    json.dump(event_dict, outfile)
   
# marking the end time and then calculating the runtime of the restructuring process.     
end_time = t.time()
run_time = end_time - start_time


# printing off the runtime so I know how long it took. The last time I ran it, it took around 15 minutes to process the whole file; it's very much a batch processing mindset when it comes to this.
# double-checking the size of the event_dict and the event counter. 
# printing off the number of entries which are double counted ->
print("Runtime in seconds was:", run_time)
print("The total runtime was", (run_time//60), "minutes and", (run_time%60), "seconds.")
print("The size of event_dict is", len(event_dict))
print("There are", event_counter, "log entries")
print(dbl_count)