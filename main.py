import time
from progress.bar import IncrementalBar
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# --------------

# название ВХОДНОГО файла с расширением
entry_file_name = "entry.csv"  

# название ИТОГОГО файла с расширением
result_file_name = "result.csv"     

# индекс колонки, в которой находится адрес сайта. Начинается с 0
index_of_site_in_entry_file = 0     

# массив строк для поиска через запятую
search_strings_array = [
    "itunes",
    "apple.com",
    "play.google.com",
    "appmetrica",
    "adjust",
    "onelink",
    "appsflyer"
]

# тег, в котором нужно искать значения
where_should_find_string = "." 
# "@href" - поиск в адресе ссылки
# "." - (просто точка) поиск в тексте

# --------------

def create_xpath(search_strings_array, tag):
    my_string = f"contains({tag}, '{search_strings_array[0][1:]}') "
    for s in search_strings_array[1:]:
        my_string = my_string + "or contains(" + tag + " , '" + s[1:] + "') "

    return f"//a[{my_string}]"


def try_find_element_on_site(site_address, search_string):
    url = site_address

    try:
        driver.get(url)
        driver.implicitly_wait(10)
        elem = driver.find_element_by_xpath(search_string)
        return "Found"
    except Exception as e:
        return(e)


def count_total_rows(file):
    row_count = 0
    with open(file, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Iterate over each row in the csv using reader object
        row_count = sum(1 for row in csv_reader)

    return row_count

options = Options()
options.add_argument("window-size=1400,800")
driver = webdriver.Chrome(options=options)

xpath_string = create_xpath(search_strings_array, where_should_find_string)
suffix = '%(index)d/%(max)d [%(elapsed_td)s / %(eta)d / %(eta_td)s]'

bar = IncrementalBar('Countdown', max=count_total_rows(entry_file_name), suffix=suffix)

with open(entry_file_name, 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        result = try_find_element_on_site(
            row[index_of_site_in_entry_file], xpath_string)
        row.append(result)

        with open(result_file_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        
        bar.next()
        time.sleep(1)

driver.close()
bar.finish()
