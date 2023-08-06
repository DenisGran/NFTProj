import classes

def main():
    start_from = 1
    db_handler = classes.DatabaseHandler()

    print('Welcome!')
    print('Do you want to load an existing database? (y/n) ', end='')
    choice = input()

    if choice == 'y':
        db_handler.load_database()
        start_from = db_handler.get_database_length()
    else:
        print("Delete all existing nfts? (y/n) ", end="")
        choice = input()
        if choice == 'y':
            classes.settings.delete_existing_nfts()
    
    print("Starting from #" + str(start_from))
    
    print('How many giraffes to generate? ', end='')
    num = input()

    for x in range(start_from, int(num) + start_from):

        myGirrafe = classes.Girrafe()
        print('Giraffe number #' + str(x) +":" + str(myGirrafe))
        myGirrafe.save(file_name= str(x) + ',' + myGirrafe.print_minimal_traits() + '.png')

        db_handler.save_database()
        
    
    print("Finished!")
    print("Press any key to continue...")
    input()
    return


if __name__ == '__main__':

    main()