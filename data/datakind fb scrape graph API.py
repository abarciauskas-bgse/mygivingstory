import sys
print sys.version
import facebook
import pandas as pd

#time senstive token associated with a facebook application that does not have users
#new tokens can be found: https://developers.facebook.com/tools/accesstoken/
token = 'EAACEdEose0cBAG8vey7WNM9fOjH7AEkX2QCgZCav4a2avUP3s5F9cKTufKrRMDazKasa4kydICaAnS5ORtaZAY6ZCRH0eVJX7NU9rl04NCIQ0xZChh2xy2b2Pc4Wp9nEvNZBhS1E9KVO2Qh1Le6fmZACkljuhkoYzGNOJOdScb6gZDZD'

def ReturnDonors():
    #Return a dictionary of donors from the excel sheet xlsm (used xlsm in order to extract hyperlinks
    #create an empty list to return
    donor_list = list()

    source_file_location = "C:\Users\\sbartashnik\datakind_fb_profiles.xlsm"
    donors = pd.read_excel(source_file_location, "Sheet1")

    #for each of the rows in the excel..
    for idex, row in donors.iterrows():
        #crate a dictioanary for indvidual donor
        donor = {}
        donor["name"] = row[0]
        #obtain just the ID from a facebook URL that contains fb user id
        donor["id"] = str(row[1]).split("/").pop()
        donor["info"] = "x"
        #append to return list
        donor_list.append(donor)
    return  donor_list

#a request URL for the Facebook graph - don't actually have access to the majority of these fields.
request_str = "fb_id?fields=id,name,about,age_range,bio,birthday,education,favorite_athletes,cover,currency,devices," \
              "favorite_teams,political,significant_other,hometown,inspirational_people,email,gender,first_name,interested_in,languages,link,quotes,relationship_status,religion,sports,timezone,website,work"

#just want to open this once
my_graph = facebook.GraphAPI(access_token=token, version='2.2')

def GetFBInfo(fb_id):
    #call the Facebook graph API and return any of the available information from the public profile that I can
    import math
    if not math.isnan(float(fb_id)):
        #some blank values in the Excel requires checking to make sure the id is valid
        try:
            #replace the fb_id holder from the request_str with a real donor id
            request_str_local = request_str.replace("fb_id", fb_id)
            #get the objects available from the request string
            fb_user = my_graph.get_object(request_str_local)
            #return a JSON representation of the fb user profile
            return fb_user
        except:
            #print 'Failed for ID ', fb_id, sys.exc_info()
            return  "x"
    else:
        "x"

#get a list of all the people that donated
my_donors = ReturnDonors()

#don't have permission  to pull all profiles (I think) so I seperate them into two lists.
found_donors = []
lost_donors = []

for person in my_donors:
    #I had set this up for multiple loops through  because I orginally thought there may have been throttling issues.
    #Now, i just think they are general permission issues.
    if person["info"] == "x":
        tmp = GetFBInfo(person["id"] )
        if tmp == "x":
            lost_donors.append(person)
        else:
            #updating the info field with the JSON object from FB
            person["info"] = tmp
            #adding to the list of found donors
            found_donors.append(person)

all_found_donors = []
for found in found_donors:
    print found

#Below code is unfished. Was going to put all the info into a CSV but
#decided to just focus on getting the age_offset value since that
#is the only thing of value.
#     print found["info"]
#
#     found_df = pd.DataFrame.from_dict(found)
#     all_found_donors.append(found_df)
#
#     all_found_donors.append(single_donor)
#
# output = pd.concat(all_found_donors)
# output.to_csv("DataKind_FoundDonor_FB_info.csv")

# troubleshoot
# request_str = "fb_id?fields=id,age_range,birthday,relationship_status"
# fb_id='913534645348395'
# request_str_local = request_str.replace("fb_id", fb_id)
# info=my_graph.get_object(request_str_local)
# print info
