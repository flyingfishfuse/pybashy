    arguments = parser.parse_args()     
    if arguments.testing == True and (arguments.config_file != True):
        execute_test()
    #are we using config?
    if arguments.config_file == True and (arguments.testing != True):
        config = configparser.ConfigParser()
        config.read(arguments.config_path)
        # user needs to set config file or arguments
        user_choice = config['Thing To Do']['choice']
        if user_choice== 'doofus':
            yellow_bold_print("YOU HAVE TO CONFIGURE THE DARN THING FIRST!")
            raise SystemExit
        # Doesnt run for choice = DEFAULT unless (look down)
        elif user_choice == 'DEFAULT':
            execute_test()
        #if the user chose a section in the config file
        elif config.has_section(user_choice):
            #find the list of modules they want to load
            modules_to_load:list = config['Thing To Do']['modules'].split(',')
            #sort through them to see if they are requesting something that actually exists
            for extension in modules_to_load:
                # make a pool of CommandSet() objects in a dict, named after the module
                load_modules_from_config()
        else:
            redprint("[-] Option not in config file")
     #loading a specialized module
    elif arguments.config_file == False and (arguments.dynamic_import == True):
        new_command = CommandRunner()
        new_command_pool = new_command.dynamic_import(arguments.dynamic_import_name)

