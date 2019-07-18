import getContents as c
import utils

oca = "https://oca.org"
goarch = "https://goarch.org"

def create_documents():
    #try:
    print("create_documents | getting arrays")
    readings_info_array = c.get_readings_text(c.get_readings_urls(oca,"readings"))
    saints_info_array = c.get_saints_info(oca,"saints/lives")
    fasting_info_array = c.get_fasting_info(goarch, "chapel")

    print("create_documents | generating strings")
    readings_string = utils.nested_list_to_string(readings_info_array)
    saints_string = utils.nested_list_to_string(saints_info_array)
    fasting_string = utils.nested_list_to_string(fasting_info_array)

    print("create_documents | saving files")
    readings_file = utils.save_to_relative_path("data","readings.txt",readings_string)
    saints_file = utils.save_to_relative_path("data","saints.txt",saints_string)
    fasting_file = utils.save_to_relative_path("data","fasting.txt",fasting_string)
    #except:
    #    print("ERROR in creating documents!")

create_documents()
