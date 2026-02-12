import os
from pprint import pprint
from textCleaner import cleanTextWithBS4 , cleanTextWithBleach #This is the pattern to include external file this function help me clean text

def getListoffiles(dir):
    files_list = []
    #get files
    try:
        #loop and get files
        with os.scandir(dir) as entries:
            for entry in entries:
                if entry.is_file() and entry.path.endswith(".txt"):
                    files_list.append(entry.path)
                    #print(entry.path)
                    
    except FileNotFoundError:
        print(f"files are not available in requested dir '{dir}'")
    except Exception as e:
        print(f"An error occured : {e}")
    return files_list

files = getListoffiles('/Users/pramodyewale/Pramod/Drive2/sant tukaram')
files.sort()
# pprint(files)

def proceess_files(files):
    for index, file in enumerate(files):
        all_files = []
        #if(index < 1):
        f = open("./abhang.txt",'+a')
        with open(file, 'r') as filecontent:
            cleaned = []
            for line in filecontent:
                #row = cleanTextWithBleach(line.strip())
                row = cleanTextWithBS4(line.strip())
                if row is not None and row.strip() != "":
                    cleaned.append(row)
                    # clean_content = clean_content +' \n '+ cleanTextWithBleach(line.strip())
                    # clean_content = clean_content + line.strip()
                    #print(line.strip()) # .strip() removes leading/trailing whitespace, including newlines
            
                # all_files.append("\n".join(cleaned))
            
            f.write("\n".join(cleaned))

        # pprint(all_files)

proceess_files(files)
