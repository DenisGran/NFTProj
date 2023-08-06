import settings, random, subprocess, hashlib
from wand.image import Image
from wand.color import Color
from wand.image import ALPHA_CHANNEL_TYPES

class DatabaseHandler:

    def __init__(self):
        self._database_name = 'autosave.db'
        
        return

    def save_database(self):

        with open(self._database_name, 'w') as autosave_file:
            autosave_file.write(str(settings.generated_girrafes_db))
    
        return

    def load_database(self):

        with open(self._database_name, 'r') as autosave_file:
            settings.generated_girrafes_db = eval(autosave_file.read())
        
        return
    
    def get_database_length(self):

        return len(settings.generated_girrafes_db)

class Trait:

    def __init__(self, file_name = 'None,ultra_common.png', part_name = 'Skeleton'):
        
        self.file_name = file_name
        self.part_name = part_name
        self.name = settings.get_trait_name(file_name)
        self.rarity = settings.get_trait_rarity(file_name, part_name)
        self.rarity_name = settings.get_rarity_name(self.rarity)
        self.minimal = False
        self.is_trait = False if part_name in settings.not_a_trait else True
        
        return
    
    def __str__(self):
        return (self.name if self.minimal else self.name + ' : ' + self.rarity_name + ' (' + str(self.rarity) + '%)') if self.is_trait else ''

class Girrafe:

    def _generate_part(self, part_name):

        res = None
        parts_list = settings.get_part_files(part_name)
        rarities_list = settings.get_part_rarities(part_name)

        if rarities_list.count(0) == len(rarities_list):
            print('No trait generated for [' + part_name + ']')
        
        else:
            generated_item_name = random.choices(parts_list, rarities_list, k=1)[0]
            res = Trait(generated_item_name, part_name)
 
        return res
    
    def _generate_background(self):

        generate_rgb_value = lambda : int(random.uniform(0, 1) * (255 - 100 + 1) + 100)
        generate_rgb_full = lambda : 'rgb(' + str(generate_rgb_value()) + ', ' + str(generate_rgb_value()) + ', ' + str(generate_rgb_value()) + ')'
        
        return generate_rgb_full()
    
    def _print_traits(self):

        res = ''
        total_rarity = 0
        for part in self.traits:
            if self.traits[part].is_trait:
                res += '  ' + part + ': ['
                res += str(self.traits[part]) + ']\n'
                total_rarity += self.traits[part].rarity
        res += '\nTotal traits: ' + str(len(self.traits) - len(settings.not_a_trait))
        res += '\nTotal rarity: ' + str(total_rarity / len(self.traits)) + '%'

        return res
    
    def print_minimal_traits(self):

        res = ''

        for part in self.traits.values():
            part.minimal = True
            res += str(part) + ','
            part.minimal = False

        return res[:-1]
    
    def _generate_girrafe(self):

        ok = True

        self.bgcolor = self._generate_background()
        self.image = Image(width = settings.IMAGE_WIDTH, height= settings.IMAGE_HEIGHT, background=Color(self.bgcolor))
        self.image.compression_quality = 00
        self.traits = {}

        for part in settings.positions:
            if part in settings.impossible_combinations:
                for impossible_part in settings.impossible_combinations[part]:
                    if impossible_part in self.traits and 'None' not in self.traits[impossible_part].name:
                        ok = False
            if ok:
                generated_part = self._generate_part(part)
                if generated_part:
                    temp = Image(filename=settings.files_path + part + '/' + generated_part.file_name)
                    temp_position = settings.calculate_positions(temp, part)
                    self.image.composite(temp, left = temp_position[0], top = temp_position[1])
                    self.traits[part] = generated_part
            else:
                self.traits[part] = Trait(part_name = part)
            
        return
    
    def _generate_hash(self):

        hashing_function = hashlib.md5()
        
        for part in self.traits:
            hashing_function.update(str(self.traits[part].file_name).encode())
        
        self._girrafe_hash = hashing_function.digest()

        return

    def __init__(self):
        
        self._generate_girrafe()
        self._generate_hash()

        while self._girrafe_hash in settings.generated_girrafes_db:
            
            print('\n\\\\\\Just generated a girrafe that already exists! Regenerating...///\n')
            self._generate_girrafe()
            self._generate_hash()
        
        for trait in self.traits.values():
            settings.image_parts_files[trait.part_name][trait.file_name][1] -= 1
            if settings.get_trait_amount(trait.file_name, trait.part_name) == 0:
                del settings.image_parts_files[trait.part_name][trait.file_name] #Removing the possibility of generating again

        settings.generated_girrafes_db.add(self._girrafe_hash)
        
        return
    
    def save(self, show=False, file_name = 'temp2.png'):
        
        self.image.alpha_channel = ALPHA_CHANNEL_TYPES[11]
        self.image.save(filename=settings.save_path + file_name)

        return
    
    def __str__(self):
        return '\n\n==========\n- Girrafe details -\n\n Background color: ' + self.bgcolor + '\n\n Traits:\n' + self._print_traits() + '\n==========\n'
