import pickle

from selenium import webdriver


# Best time to scrap is between 3AM to 6AM -- no load on server

# Load the Chrome web driver
# Replace the chrome driver with specific to your OS
# The one included in the project is for Linux 64bit.
driver = webdriver.Chrome('./chromedriver')

# Load the SRN list.
srn_list = pickle.loads(open('srn_list.txt', 'rb').read())

# Initialize the dictionary to be pickled
marks, invalid_srn, invalid_srn_list = {}, 0, []

for srn in srn_list:
    # Build the result url
    url = 'http://results.logisys.net.in/reva/result.php?r=' + srn.lower() + '&e=E'

    # Get the result page
    driver.get(url)

    try:
        # Get the result information
        cgpa = driver.find_element_by_xpath('//*[@id="result_success_div"]/table[3]/tbody/tr[1]/td').text.split()[4].strip(',')
        name = driver.find_element_by_xpath('//*[@id="student_info"]/tbody/tr[3]/td').text.split(':')[1]

        # Add it to the marks dictionary
        marks[srn] = {'cgpa': cgpa, 'name': name}

        # Print for debug purpose
        print(marks[srn])

    except:
        print("Invalid SRN: {}".format(srn))
        invalid_srn += 1
        invalid_srn_list.append(srn)


print("Invalid srns count: {}, list: {}".format(invalid_srn, invalid_srn_list))

# Pickle and store the marks dictionary
with open('marks', 'wb') as f:
    f.write(pickle.dumps(marks))

# The End
driver.close()
