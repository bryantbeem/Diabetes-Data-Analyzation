###############################################################################
#Computer Project #8
#   function to open file
#       use try and except
#   function to create dictionary
#       for loop to read through lines and creat tuple and dictionary
#   function to get country total
#       uses three four loops to loop through dictionary inputed in function
#   function to display table of data
#       uses two for loops to sort list and add up totals
#   function to prepare plot data
#       uses a for loop to create a dictionary for plotting
#   function to plot data
#   function for main
#       call for functions using two while loops
#       ask to plot data
###############################################################################
import pylab
#from operator import itemgetter   # optional, if you use itemgetter when sorting

REGIONS = {'MENA':'Middle East and North Africa','EUR':'Europe',\
               'AFR':'Africa','NAC':'North America and Caribbean',\
               'SACA':'South and Central America',\
               'WP':'Western Pacific','SEA':'South East Asia'}

def open_file():
    '''
    Prompts user to insert a file
    Checks for an error
    '''
    excel_file = input("Please enter a file name: ") #prompt to input a file name
    while True:
        try:
            return_file = open(excel_file, encoding ="windows-1252") #reads file
            return return_file #returns file
        except FileNotFoundError: #if file is not found
            excel_file = input("File not found. Please enter a valid file name: ") #print error and prompt to input a file again
    
    
def create_dictionary(fp): #create dictionary functiony
    '''
    Reads open file object
    Creates dictionary with region, country, and age group
    The dictionary consists of a dictionary of dictionaries of dictionaries of lists of tuples
    Returns the dictionary created
    '''
    fp.readline() #reads line of headers
    D = {} #initialize empty dictionary
    tup = () #initialize empty tuple
    for line in fp: #for loop for each line in the file entered
        line_list = line.split(',') #separate each line with commas
        country = line_list[1] #set country equal to index 1
        region = line_list[2] #set region equal to index 2
        age_group = line_list[3] #set age group equal to index 3
        gender = line_list[4] #set gender equal to index 4
        geographic_area = line_list[5] #set geographic area to index 5
        diabetes = int(float(line_list[6])*1000) #set diabetes to index 5 and convert to rounded integer
        population = int(float(line_list[7])*1000) #set population to index 7 and convert to rounded integer
        tup = (gender, geographic_area, diabetes, population) #create tuple for gender, geographic area, diabetes and population
        if region not in D: #region not in dictionary
            D[region] = {} #create a new empty region dictionary
        if country not in D[region]: #country not in region dictionary
            D[region][country] = {} #create a new empty region and country dictionary
        if age_group not in D[region][country]: #age group not in region and country dictionary
            D[region][country][age_group] = [] #create empty list for region country and age group
        D[region][country][age_group].append(tup) #add new dictionary to the tuple
    return D #return the dictionaru created

def get_country_total(data): #function for finding total number of diabetes and people per country
    '''
    Receives dictionary from certain region
    Creates tuple for the number of people with diabetes and the total population
    Returns dictionary of tuples
    '''
    country_dict = {} #initialize an empty dictionary
    for country, age_groups in data.items(): #consider the key and value in the data used in the function
        country_name = country #define country name
        people_total = 0 #initialize people total to 0
        diabetes_total = 0 #initialize diabetes total to 0
        for person in age_groups.values(): #loop through tuple of age groups
            for tup_1 in person:
                diabetes_total += tup_1[2] #add index 2 to diabetes total
                people_total += tup_1[3] #add index 3 to people total
        country_dict[country_name] = (diabetes_total, people_total) #add country name and two totals to country dictionary
    return country_dict #return dictionary

def display_table(data, region): #display table function
    '''
    Receives dictionary returned from get_country_total function
    Displays country name, number of people with diabetes, 
        and the total population of that country
    Uses specified format to display data
    Returns nothing
    '''
    print("     Diabetes Prevalence in {:^16s}".format(REGIONS[region]))
    print("{:<25s}{:>20s}{:>16s}".format("Country Name", "Diabetes Prevalence", "Population"))
    
    list_1 = [] #initialize empty list
    for key, value in data.items(): 
        tup = (key, value[0], value[1]) #create tuple for key and value index 0 and 1
        list_1.append(tup) #add tuple to list
        
    list_1.sort() #sort list
    diabetes_overall = 0 #initialize total diabetets count to 0
    people_overall = 0 #initialize total people count to 0
    for tup in list_1: #for loop for tuples in list created above
        country_name, diabetes_total, people_total = tup 
        print("{:<25s}{:>20,d}{:>16,d}".format(country_name, diabetes_total, people_total))
        diabetes_overall += diabetes_total #add diabetes total to overall total
        people_overall += people_total #add people total to overall total
        
    print("")
    print("{:<25s}{:>20,d}{:>16,d}".format("TOTAL", diabetes_overall, people_overall))
    
def prepare_plot(data):
    '''
    Receives a dictionary for a certain region
    Creates new dictionary with age and gender as its keys
    Adds value of the total for all the countries in that region
    Returns the dictionary created
    '''
    D = {} #initialize empty dictionary
    for value in data.values(): 
        for key, v in value.items(): #for loop for values in dictionary
            for tup in v: #for loop for the tuple in the dictionary
                age = key #set age equal to the key in the dictionary
                gender = tup[0].upper() #set gender equal to the tuple index 0
                value = tup[2]  #set value equal to the tuple index 2
                if age not in D:
                    D[age] = {} #set age in dictionary to empty dictionary
                if gender not in D[age]:
                    D[age][gender] = 0 #set dictionary to 0
                D[age][gender] += value #add value to dictionary
    return D #return the dictionary created
    
def plot_data(plot_type,data,title):
    '''
        This function plots the data. 
            1) Bar plot: Plots the diabetes prevalence of various age groups in
                         a specific region.
            2) Pie chart: Plots the diabetes prevalence by gender. 
    
        Parameters:
            plot_type (string): Indicates what plotting function is used.
            data (dict): Contains the diabetes prevalence of all the contries 
                         within a specific region.
            title (string): Plot title
            
        Returns: 
            None       
    '''
    
    plot_type = plot_type.upper()
    
    categories = data.keys() # Have the list of age groups
    gender = ['FEMALE','MALE'] # List of the genders used in this dataset
    
    if plot_type == 'BAR':
        
        # List of population with diabetes per age group and gender
        female = [data[x][gender[0]] for x in categories]
        male = [data[x][gender[1]] for x in categories] 
        
        # Make the bar plots
        width = 0.35
        p1 = pylab.bar([x for x in range(len(categories))], female, width = width)
        p2 = pylab.bar([x + width for x in range(len(categories))], male, width = width)
        pylab.legend((p1[0],p2[0]),gender)
    
        pylab.title(title)
        pylab.xlabel('Age Group')
        pylab.ylabel('Population with Diabetes')
        
        # Place the tick between both bar plots
        pylab.xticks([x + width/2 for x in range(len(categories))], categories, rotation='vertical')
        pylab.show()
        # optionally save the plot to a file; file extension determines file type
        #pylab.savefig("plot_bar.png")
        
        
    elif plot_type == 'PIE':
        
        # total population with diabetes per gender
        male = sum([data[x][gender[1]] for x in categories])
        female = sum([data[x][gender[0]] for x in categories])
        
        pylab.title(title)
        pylab.pie([female,male],labels=gender,autopct='%1.1f%%')
        pylab.show()
        # optionally save the plot to a file; file extension determines file type
        #pylab.savefig("plot_pie.png")

def main():
    '''
    Calls for each function to run test on inputed file
    Prints region codes after file is open
    Gives user option to plot data
    '''
    fp = open_file() #call for open file function
    while True:
        print("                Region Codes") #print region codes
        print("    MENA: Middle East and North Africa")
        print("    EUR: Europe")
        print("    AFR: Africa")
        print("    NAC: North America and Caribbean")
        print("    SACA: South and Central America")
        print("    WP: Western Pacific")
        print("    SEA: South East Asia")
        region_code = input("Enter region code ('quit' to terminate): ") #ask to enter a region code
        if region_code.lower() == 'quit' or region_code.upper() in REGIONS: 
            break #break out of loop if there is not an error with the input
        else:
            print("Error with the region key! Try another region") #print error, user must input again
            
    D = create_dictionary(fp) #call for create dictionary function
    while region_code != 'quit': #user does not want to quit
        region_code = region_code.upper() #turn region code into capital letters
        country_dict = get_country_total(D[region_code]) #call for get country total function
        display_table(country_dict, region_code) #call for display table function
        visualize_str = input("Do you want to visualize diabetes prevalence by age group and gender (yes/no)?: ") #ask to plot
        if visualize_str != 'no': #user wants to plot
            plot_code = D[region_code]
            P = prepare_plot(plot_code)
            title = 'Dibaetes Prevalence in Western Pacific by Age Group and Gender'
            type_1 = 'PIE' #pie gragh
            type_2 = 'BAR' #bar chart
            plot_data(type_1, P, title) #call for plot function for pie grapj
            plot_data(type_2, P, title) #call for plot function for bar chart
        else:
            print("                Region Codes") #print region codes
            print("    MENA: Middle East and North Africa")
            print("    EUR: Europe")
            print("    AFR: Africa")
            print("    NAC: North America and Caribbean")
            print("    SACA: South and Central America")
            print("    WP: Western Pacific")
            print("    SEA: South East Asia")
            region_code = input("Enter region code ('quit' to terminate): ") #ask to enter region code
            continue
        region_code = input("Enter region code ('quit' to terminate): ")
###### Main Code ######
if __name__ == "__main__":
    main()