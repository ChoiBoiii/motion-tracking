## Import modules
import os


## MAKE CURRENT WORKING DIRECTORY RELATIVE TO FILE
def set_CWD_to_file(absolutePath):
    '''
    Makes current working directory relative to file
      Takes the absolute path that will become the new relative path starting point
    '''

    ## MAKE WORKING DIRECTORY RELATIVE TO FILE
    try:
        directoryName = os.path.dirname(absolutePath)   # uses absolute path to locate file on local system
        os.chdir(directoryName)                         # changes cwd to the direct directory

    ## HANDLE ERROR
    except:
        print(f"\nError trying to make working directory relative to file:\n    Code from source file {__file__}")


## FUNC TO GET USER TO INPUT SCREEN WITH AND CALCULATE HEIGHT BASED OFF GIVEN RATIO
def user_input_screen_dimensions(heightMultiplier=1):
    # 'heightMultiplier' is what the input value is multiplied to give the screen height
    while True:
        try:
            tempVar = int(input('Enter screen width: '))
            try:
                if tempVar >= 100:
                    break
                elif tempVar < 100:
                    print('  Error: Invalid input v\u0332a\u0332l\u0332u\u0332e\u0332;')
                    print('    Input must be a positive intager above 100 \n')
            except NameError:
                pass
        except ValueError:
            print('  Error: Invalid input t\u0332y\u0332p\u0332e\u0332;')
            print('    Input must be a positive intager above 100 \n')
    X, Y = tempVar,int(tempVar * heightMultiplier)
    return X, Y