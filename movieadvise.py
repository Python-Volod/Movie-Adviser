#Makes movie or series suggestion depending on user input in GUI(movadv_vis_int.py)
import requests 
import json 


# Container for movie information 
class Tape():
    def __init__(self):
        self.text = ""
        self.genre = ""
    def write(self , text):
        self.text = self.text + text
    def get_text(self):
        return self.text
    def def_genre(self , text):
        self.genre = text
    def get_genre(self):
        return self.genre
    def __str__(self):
        return "Tape object, container for movie information"

# Insert your API keys, if you don't have them just make them here - 1) https://tastedive.com/read/api   2) https://www.omdbapi.com
API_K_tastedive = # Insert your key
API_K_OMDb = # Insert you key


#Creates movie suggestions 
def get_movie_advise(name, us_in_lim, search_type):
    print("Call was Heard")


 #Takes age restriction from OMDb API and interprets it
    def filter_for_Rated(rating):
        if rating == "G":
            return "0+"
        elif rating == "PG":
            return "0+ - Parental Guidance Suggested"
        elif rating == "PG-13":
            return "13+"
        elif rating == "R":
            return "18+, if younger Parental Guidance Required"
        else:
            return "18+, No one younger allowed"


 # Takes movie rating from OMDb API
    def scores_IMDb(score_list):
        res = []
        for dic in score_list:
            if "Rotten Tomatoes" in dic["Source"]:
                temp_res = ["Rotten Tomatoes", dic["Value"]]
            elif "Metacritic" in dic["Source"]:
                temp_res = ["Metacritic" , dic["Value"]]
            elif "Internet Movie Database" in dic["Source"]:
                temp_res = ["Internet Movie Database" , dic["Value"]]
            res.append("{} score for this movie is {} \n".format(temp_res[0],temp_res[1]))
        return res


 #Makes http request to tastedive API to get similar movie suggestions
    def get_info_from_tastedive(name , search_type , k_t = API_K_tastedive):
        if search_type[0] == 1:
            search_type_l = "movies"
        elif search_type[1] == 1:
            search_type_l = "shows"
        else:
            search_type_l = "movies"
        if search_type[0] == 1 and search_type[1]:
            search_type_l = "movies&&shows"
        d_params = {"type": search_type_l , "limit":us_in_lim, "k":k_t}
        d_params["q"] = name 
        page = requests.get("https://tastedive.com/api/similar?", params = d_params)
        res_dic = json.loads(page.text)
        list_advise = res_dic["Similar"]["Results"]
        advise = []
        for movie in list_advise:
            advise.append(movie["Name"])
        return advise

 #Makes http request to OMDb API to get suggested movie description
    def get_info_from_OMDb(title, search_type, k_o = API_K_OMDb):
        if search_type[0] == 1:
            search_type_l = "movie"
        elif search_type[1] == 1:
            search_type_l = "series"
        else:
            search_type_l = "movie"
        if search_type[0] == 1 and search_type[1]:
            search_type_l = ""
        d_params_OMDb = {"apikey": k_o,"r" : "json" , "type": search_type_l}
        d_params_OMDb["t"] = title
        page = requests.get("http://www.omdbapi.com/?", params = d_params_OMDb)
        answer_initial = json.loads(page.text)
        if answer_initial["Response"] == "False":
            info_from_OMDb = {"Extendent" : ["Error" , "Error", "Error", "Error", answer_initial["Error"] , "Error", "Error"]}
        else:
            info_from_OMDb = { "Extendent": [filter_for_Rated(answer_initial["Rated"]), answer_initial["Released"], answer_initial["Runtime"], scores_IMDb(answer_initial["Ratings"]), answer_initial["Title"],  answer_initial["Plot"], answer_initial["Genre"]]}
        return info_from_OMDb


 #Main 
    extract_movie_titles = get_info_from_tastedive(name, search_type)
    movie_count = 0
    result_suggestions = []
    # Creates a list of Tape objects that are films with info about them
    for title in extract_movie_titles:
        movie_count += 1
        info_from_OMDb = get_info_from_OMDb(title, search_type)
        title = Tape()
        result_file = title
        result_file.def_genre(info_from_OMDb["Extendent"][6] )
        result_file.write("\n" + "Movie" + str(movie_count) +" : \n")
        result_file.write(info_from_OMDb["Extendent"][4] + "\n")
        result_file.write("Film genre - " + info_from_OMDb["Extendent"][6] + "\n")
        result_file.write( "Age restriction for this movie is - " + info_from_OMDb["Extendent"][0] + "\n")
        result_file.write( "Release date is - " + info_from_OMDb["Extendent"][1] + "\n")
        result_file.write( "Runtime of a movie is - "+ info_from_OMDb["Extendent"][2] + "\n")
        for rating in info_from_OMDb["Extendent"][3]:
            result_file.write(rating + "\n")
        result_file.write("\n")
        result_file.write("The short descripton of plot is - " + info_from_OMDb["Extendent"][5] + "\n" * 2)
        result_suggestions.append(result_file)
    return(result_suggestions)
