from collections import Counter
import os, json, re

print('\nLoading settings...')

IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400
AMOUNT_OF_NFTS = 10000
work_path = os.getcwd().replace('\\', '/') + '/'
save_path = (work_path + 'nft/').replace('/', '\\')
files_path = work_path + 'files/'
generated_girrafes_db = { '' } #A hash dict of generated nfts, used to check for doubles
all_nfts = sorted([ file.name for file in os.scandir(save_path) if not file.is_dir() ], key=lambda f: int(''.join(list(filter(str.isdigit, f.split(',')[0])))))
#^All generated nfts filenames sorted in one list
attributes_amounts = {}

rarities = {

    'ultra_common' : 90,
    'common' : 60,
    'uncommon' : 50,
    'rare' : 30,
    'epic': 5,
    'legendary' : 1

}

not_a_trait = [
    'Skeleton'
]

impossible_combinations = {
    'Masks' : ['Holding_In_Mouth', 'Hats', 'Motorcycle_Helmet'],
    'Motorcycle_Helmet' : ['Hats', 'Eyes', 'Masks']
}

_reverse_rarities = {

    value: key for key, value in rarities.items()

}

rarities_amounts = {
    
    rarity
    :
    [
        -1,
        200, # 25 / 60
        200, # 3 / 50
        150,  # 10 / 30
        280,  # 15 / 5
        250   # 2 / 1
    ][index]
    
    for index, rarity in enumerate(_reverse_rarities)
}

positions = {

    'Shoulders' : (1, 225),
    'Holding_In_Mouth' : (3.9, 235),
    'Shirts' : (1.18, 339),
    'Skeleton' : (2, 20),
    'Skin' : (2.15, 20),
    'Earrings' : (1.46, 100),
    'Eyes' : (2.265, 143),
    'Hats' : (2.15, 14),
    'Lips' : (2.6, 221),
    'Necklace' : (1.54, 280),
    'Masks' : (2.15, 14),
    'Motorcycle_Helmet' : (2.15, 14)

}

#This function returns the trait's rarity based of filename from image_parts_files
get_trait_rarity = lambda file_name, part_name : image_parts_files[part_name][file_name][0]

#A nice wrapper for getting the name
get_trait_name = lambda file_name : file_name[:file_name.index(',')].replace('_', ' ')

#A wrapper for getting the rarity's name
get_rarity_name = lambda rarity : _reverse_rarities[rarity]

#Wrapper for getting the amount of times an item has been used
get_trait_amount = lambda file_name, part_name : image_parts_files[part_name][file_name][1]

#Generating position based on a formula
calculate_positions = lambda image, part : (int((400-image.width) / positions[part][0]) , positions[part][1])

_print_error = lambda message = '' : print('Settings: Error:', message)

delete_existing_nfts = lambda : os.system("del " + save_path + "*.*")

get_trait_name_from_filename = lambda part_index, filename : str(filename[:filename.index('.')].split(',')[part_index + 1]) if not filename == '' else ''

get_trait_rarity_from_attributes = lambda part, filename : attributes_amounts[part][filename] if part in attributes_amounts else '' #Doing this because we cant use dict inside a dict

#This is returning file's rarity based off the file name
def _generate_rarity_from_filename(file_name):
    res = 0 #Setting 0 instead of None because of random.choices
    try:
        res = rarities[file_name[file_name.index(',') + 1 : file_name.index('.')].lower()]
    except:
        _print_error('Couldn\'t get rarity for file [' + file_name + ']')
    return res

image_parts_paths = {

    file.name : files_path + file.name for file in os.scandir(files_path) if file.is_dir()
}

#Creating a dict of parts that has a dict inside with file name as key and (rarity, amount) as value
#For example: {image_parts_files} -> {Shoulders} -> {Shoulder1 : (70, 150)}
image_parts_files = { 
    
    part : { name : [_generate_rarity_from_filename(name), rarities_amounts[_generate_rarity_from_filename(name)]] for name in os.listdir(image_parts_paths[part])} for part in image_parts_paths
    
}

#This function returns a list of rarities of the part (used for random.choices)
def get_part_rarities(part_name):
    res = None
    if part_name in image_parts_files:
        res = [result[0] for result in list(image_parts_files[part_name].values())]
    else:
        _print_error('Part [' + part_name + '] is not found!')
    return res

#This function returns a list of traits of the part (used for random.choices)
def get_part_files(part_name):
    res = None
    if part_name in image_parts_files:
        res = list(image_parts_files[part_name].keys())
    else:
        _print_error('Part [' + part_name + '] is not found!')
    return res

def _load_attributes():

    parts_to_delete = []

    attributes_amounts.update( { 
        part : [
            
              get_trait_name_from_filename(index, nft) for nft in all_nfts
             
               ]
        for index, part in enumerate(positions)
        })

    for part in attributes_amounts:
        if part in not_a_trait:
            parts_to_delete.append(part)
        else:
            attributes_amounts[part] = dict(Counter(attributes_amounts[part]))

    for part in parts_to_delete: #Doing that because we cant delete dict value while iterating
        del attributes_amounts[part]

    return

def calc_nfts_rarities(format_json=True):

    _load_attributes()

    all_nfts_with_rarities = [

            {
                part :
                {'trait_name' : get_trait_name_from_filename(index, nft), 'rarity' : get_trait_rarity_from_attributes(part, get_trait_name_from_filename(index, nft))}
                
                for index, part in enumerate(positions) if part not in not_a_trait
            }
        
        for nft in all_nfts
    ]

    for index, nft_dict in enumerate(all_nfts_with_rarities):
        nft_dict['nft_id'] = index + 1


    return json.dumps(all_nfts_with_rarities) if format_json else all_nfts_with_rarities

def print_attributes_pretty(nfts, use_percentage = False):

    for part in nfts:
        print('##' + part + '## Total:', str(len(nfts[part])) + '\n')
        for item in nfts[part]:
            print(item, ': ' + ( str( 100 * nfts[part][item] / AMOUNT_OF_NFTS) + '%' if use_percentage else str(nfts[part][item])) + ', ', end ='')
        print('\n')

    return

print('Finished loading settings.\n')