import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

def get_driver():
    chrome_options = webdriver.FirefoxOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Firefox(executable_path='./geckodriver', options=chrome_options)

    driver.get('https://translate.google.com/#view=home&op=translate&sl=en&tl=fr')
    time.sleep(1)	
    driver.find_element_by_xpath('/html/body/div/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button').click()
    time.sleep(1)
    driver.get("https://translate.google.com/?sl=en&tl=fr&op=translate")
    return driver

def raw_text_to_text(tabel, number_pos):
    dict_trans = {}
    
    for index in range(number_pos):
        all_trans = tabel.find_elements(By.TAG_NAME, 'tbody')[index].text.split('\n')
        pos = all_trans[0]
        number_word = len(all_trans)
        words = [all_trans[i] for i in range(number_word) if i%2 == 1]
        dict_trans[pos] = words
    return dict_trans

for file_name in range(19, 20):
    print('read file:' + str(file_name))
    df = pd.read_csv("./EN_word/" + str(file_name) + ".csv")
    words = list(df['source'].values)
    words = [str(x) for x in words]
    my_dict = []
    f = open('./dict/dict' + str(file_name) + '.txt', 'a')
    
    driver = get_driver()
    text_area = driver.find_elements_by_tag_name("textarea")[0]
    
    for word in words:
        print(word, end=' ->  ')
        text_area.clear()
        text_area.send_keys(word)
        time.sleep(1)
        try:
            trans_word_ele = WebDriverWait(driver=driver, timeout=1).until(lambda d : d.find_element_by_xpath('/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]/span[1]/span/span'))
        except:
            try:
                trans_word_ele = driver.find_element_by_xpath('/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div[2]/div[1]/span[1]')
            except:
                driver = get_driver()
                text_area = driver.find_elements_by_tag_name("textarea")[0]
                continue
        trans_word = trans_word_ele.text
        print(trans_word)
        try:
            table = driver.find_element(By.TAG_NAME, 'table')
            number_pos = len(table.find_elements(By.TAG_NAME, 'tbody'))
            temp_dict = raw_text_to_text(table, number_pos)
            for pos in list(temp_dict.keys()):
                words_trans = temp_dict[pos]
                for w_trans in words_trans:
                    line_dict = word + '\t'+ w_trans + '\t'+pos
                    my_dict.append(line_dict)
                    f.write("%s\n" % line_dict)
            my_dict.append(word + '\t'+ trans_word + '\t'+'None')
            f.write("%s\n" % (word + '\t'+ trans_word + '\t'+'None'))
        except:
            my_dict.append(word + '\t'+ trans_word + '\t'+'properNoun')
            f.write("%s\n" % (word + '\t'+ trans_word + '\t'+'properNoun'))
    f.close()
