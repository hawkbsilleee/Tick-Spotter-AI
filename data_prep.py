import glob 
import pandas as pd 
import csv
import random
import os  
import shutil

# path of hardrive storage of tick database images 
hard_drive_directory1 = '/Volumes/My Passport/MLS_project/OriginalData/' 
# path of hardrive storage of HAM10000 database images 
hard_drive_directory2 = '/Volumes/My Passport/cs2_project/dataverse_files/All_HAM10000_images'

# ================================================================================
# Tick Section 

def find_nth(haystack, needle, n):
    """
    Finder function that finds the nth occurence of needle (str) in haystack (str).  

    haystack: str to search for needle in  
    needle: str to search haystack for 
    n (int): nth needle to find  

    returns: index of the nth needle in haystack 
    """
    # find first occurence of needle in haystack 
    start = haystack.find(needle)
    # excecute loop while needle is in haystack and n is greater than 1
    while start >= 0 and n > 1:
        # find new needle in refined haystack that starts after the previous' needles' position
        start = haystack.find(needle, start+len(needle))
        # each time substract 1 from one 
        n -= 1
    # return the index of the needle 
    return start
    
def get_ID(img_fname):
    """
    Returns the ID number of img_fname in the format (from database):
    '/Volumes/My Passport/MLS_project/OriginalData/41227+Ixodes_scapularis+Discard+RTS_+life_unk+feed_unk.jpg'  

    img_fname: str representing image path in database hardrive  

    returns: tuple of (ID number, filename) 
    """
    # find_nth(img_fname, '#', 1)
    # extract image ID number from the filename 
    ID = img_fname[img_fname.rfind('/')+1:find_nth(img_fname, '+', 1)]
    # output tuple containing the ID number and the original img_fname  
    return (ID, img_fname)

def search_csv(fname_ID):
    """
    Searches All_data.csv for image ID and all the attributes associated with it.   

    fname_ID: tuple of (image ID, filename)  

    returns: tuple of (img_fname,ID,Status,pixel size,Single tick,Sex,Lifestage,Feed-Stage,
    Species,Identifier_initials,ID_date,Notes,re-cropped)
    """
    # convert csv file into Pandas dataframe 
    df = pd.read_csv('dataset/All_data.csv')
    data = None
    # get image ID from the first item in the input tuple 
    ID = fname_ID[0]
    # get image filename from the second item in the input tuple 
    img_fname = fname_ID[1]
    # loop through each row in df 
    for index, row in df.iterrows():
        # check if the image ID is in the filename of the row 
        if ID in row["fname"]:
            # generate a data tuple that contains a series of attributes accessed from the df
            data = (img_fname, ID, row['Status'], row['pixel size'], row['Single tick'], row['Sex'], row['Lifestage'],
            row['Feed-Stage'], row['Species'], row['Identifier_initials'], row['ID_date'], row['Notes'],
            row['re-cropped'])
            break
    return data 

def write_to_csv():
    """
    Writes all the data attributes of an image file to current_project_data.csv file.      
    """
    # open the csv where project data is stored 
    with open('datasets/current_project_data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                # write the first row which serves as a title row 
                writer.writerow(['fname', 'ID', 'Status', 'pixel size', 'Single tick','Sex','Lifestage','Feed-Stage','Species',
                'Identifier_initials','ID_date','Notes','re-cropped'])
                # loop through each file in database, run get_ID and search_csv to access attributes of the 
                # image from external (metadata) csv, record these attributes in home csv
                for file in glob.iglob(hard_drive_directory1 + '*'):
                    # writer row takes a list of items, search_csv returns a tuple so list comprehension is 
                    # is used to generate a list from the tuple 
                    writer.writerow([attribute for attribute in search_csv(get_ID(file))])

def seperate_species():
    dst = '/Volumes/My Passport/MLS_project/Dataset/'
    df = pd.read_csv('datasets/TICK_project_data.csv')
    for index, row in df.iterrows():
        if row['Species'] == "Ixodes scapularis":
            # move to ixodes_scapularis folder
            shutil.copy(row['fname'], dst+'Ixodes_scapularis') 
        if row['Species'] == "Amblyomma americanum":
            # move to folder 
            shutil.copy(row['fname'], dst+'Amblyomma_americanum') 
        if row['Species'] == "Dermacentor variabilis":
            # move to folder
            shutil.copy(row['fname'], dst+'Dermacentor_variabilis') 

def display_species():
    species = ["Ixodes_scapularis", "Amblyomma_americanum", "Dermacentor_variabilis"]
    path = '/Volumes/My Passport/MLS_project/Dataset/'
    species_count = {
        "Ixodes_scapularis":0,
        "Amblyomma_americanum":0,
        "Dermacentor_variabilis":0
    }
    for s in species:
        for _ in glob.iglob(path+s+'/'+'*'):
            species_count[s] += 1 
    return species_count, sum(species_count.values())

def display_data():
    """
    Counts the number of images in hardrive database and in 'current_project_data.csv'      
    """
    img_count = 0
    # loop through each file in database hardrive 
    for _ in glob.iglob(hard_drive_directory1 + '*'):
        # add one for each image
        img_count += 1
    # convert 'current_project_data.csv' to df  
    df = pd.read_csv('datasets/current_project_data.csv')
    print('Number of images in hardrive database:', img_count)
    print('Number of images in current_project_data.csv:', len(df)-1)

# ================================================================================
# Skin Section

def merge_paths():
    """
    Move all images files in HAM10000 to centralized directory. Copies images from two src directories 
    into one centralized directory. 
    """
    # root for original source path 
    src_PATH = '/Volumes/My Passport/cs2_project/dataverse_files/'
    # loop through every image in src directory 1, copy image to centralized directory 
    for imagefile in glob.iglob(src_PATH+'HAM10000_images_part_1/' + '*'):
        shutil.move(imagefile, hard_drive_directory2)
    # loop through every image in src directory 2, copy image to centralized directory 
    for imagefile in glob.iglob(src_PATH+'HAM10000_images_part_2/' + '*'):
        shutil.move(imagefile, hard_drive_directory2)

def select_images():
    """
    Generates a dictionary with the attributes of each image file in HAM10000. Each key is 
    associated with a localization class in HAM10000 and a list containing tuples of each image file 
    and its attributes.  

    Returns a dictionary in the format (localization class -> tuple of (fname,lesion_id,image_id,dx,dx_type,age,sex,localization,dataset))  
    """
    # read HAM10000 metadata csv file 
    df = pd.read_csv('datasets/HAM10000_metadata')
    # store all unique localization classes in a list 
    HAM10000_classes = df['localization'].unique()
    data_by_classes = {}
    # loop through each unique localization class. For each class loop through each each imagefile with the
    # same class in metadata and append that file and its attributes to data_by_classes    
    for name in HAM10000_classes:
        # append data to dict via (localization classification -> imagefile attributes)
        data_by_classes[name] = [(hard_drive_directory2+'/'+row["image_id"], row["lesion_id"], row["image_id"], row["dx"], row["dx_type"], 
        row["age"], row["sex"], row["localization"], row["dataset"]) for index, row in df.iterrows() if row['localization'] == name]
    return data_by_classes

def select_write_csv(data_dict):
    """
    Writes data attributes for each file in data_dict in SKIN_project_data.csv. 
    """
    # open SKIN_project_data.csv in writing mode 
    with open('datasets/SKIN_project_data.csv', 'w', newline='') as file:
        # initialize writer object 
        writer = csv.writer(file)
        # write name row to csv
        writer.writerow(["fname", "lesion_id","image_id","dx","dx_type","age","sex","localization","dataset"])
        # loop through each key in data_dict, then loop through each tuple in the list corresponding to a localization class 
        # and access each files atrributes. Write a new row in csv with these attributes. 
        for key in data_dict:
            for i in range(len(data_dict[key])):
                writer.writerow([data_dict[key][i][index] for index in range(len(data_dict[key][i]))])

def copy_images():
    """
    Organizes tick photos by species. Seperates different specieis into different folders. 
    """
    df = pd.read_csv('datasets/SKIN_project_data.csv')
    dst = '/Volumes/My Passport/Dataset/Skin/'
    # loop through csv file and copy each file into corresponding species directory. 
    for index, row in df.iterrows():
        shutil.copy(row['fname']+'.jpg', dst)

def quant_data(data_dict):
    """
    Counts the total number of images per each class in HAM10000 dataset and the overall total. 

    Returns: dict (localization class -> number images)
    """
    images_per_class = {}
    for key in data_dict:
       images_per_class[key] = len(data_dict[key])
    total = 0
    for key in images_per_class:
        total += images_per_class[key]
    return images_per_class, total 

def count_imgs(directory):
    """
    Count number of images in databse hardrive for HAM10000 images. 

    Returns: number of images in hard drive  
    """
    img_count = 0
    # loop through each file in database hardrive 
    for _ in glob.iglob(directory + '*'):
        # add one for each image
        img_count += 1
    return img_count

# ================================================================================

if __name__ == '__main__':
    # write_to_csv()
    # count_images()

    # merge_paths()
    # select_write_csv(select_images())
    # print(count_imgs(dst_PATH+'/'))

    # seperate_species()
    # print(display_species())

    copy_images()
    
    
