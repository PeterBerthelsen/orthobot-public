import os
import re

def nested_list_to_string(list:list):
    payload = ""
    try:
        for row in list:
            for column in row:
                payload = payload + column + ","
            payload = payload[:-1] + "|"
        return payload
    except:
        return None

def save_to_relative_path(path:str, file:str, payload:str):
    root_dir = os.path.dirname(__file__)
    delivery = "0|" + payload
    try:
        with open(os.path.join(root_dir, path, file), 'wb') as write_file:
            write_file.write(delivery.encode(encoding='UTF-8',errors='ignore'))
        return True
    except:
        print("Error in creating " + path + "\\" + file)
        return False

def extract_line_from_file(path:str, file:str, delimiter:str, line: int):
    root_dir = os.path.dirname(__file__)
    iterate_flag = False
    reset_flag = False
    try:
        with open(os.path.join(root_dir, path, file), 'r', encoding='UTF-8', errors='ignore') as read_file:
            payload = str(read_file.readlines())[2:-3].split(delimiter)
            #payload = read_file.readlines()
            #print(payload)
        if line == 0:
            next_line = int(payload[0]) + 1
            extract = str(payload[next_line])[:-1].strip()
            iterate_flag = True
        elif line == -1:
            extract = ""
            for load in payload[1:]:
                extract += str(load) + delimiter
            return extract
        elif line == -2:
            extract = str(payload[1:]).strip()
            reset_flag = True
        else:
            extract = str(payload[line])[:-1].strip()
        #del payload[line]
        query_num = int(payload[0])
        if iterate_flag == True:
            query_num += 1
            payload[0] = str(query_num)
        if reset_flag == True:
            payload[0] = "0"
        delivery = ""
        for load in payload:
            delivery += str(load) + "|"
        with open(os.path.join(root_dir, path, file), 'w') as write_file:
            write_file.write(delivery)
        return extract
    except:
        return None
        
        
extract = extract_line_from_file("data", "fasting.txt","|",-1)[:-1]
print(extract)
# fast = extract.split("\', \'")
# response_thread = fast[0] + "\n" + fast[1] + "\nFasting guidelines courtesy of @goarch. For more info, visit: https://goarch.org/chapel"
        