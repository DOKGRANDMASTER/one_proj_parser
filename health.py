from base64 import encode
import requests
from bs4 import BeautifulSoup
import lxml
import json
import csv 
import random
from time import sleep


# header for the browser
headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.5013.194 Safari/537.36"
    }


#################### URL parsing site 

# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
# req = requests.get(url=url, headers=headers)
# req = req.text
# soup = BeautifulSoup(req, 'lxml')

#################### search for content by the main tag
# all_eat = soup.find_all(class_='mzr-tc-group-item-href')

#################### creating a list of categoties key: value and saving the list to the file
# all_categories = {}
# for eat_name in all_eat:
#     eat_full_name = eat_name.text
#     eat_full_src = 'https://health-diet.ru' + eat_name.get('href')
#     all_categories[eat_full_name] = eat_full_src
# with open('C:\Users\dok\Documents\GitHub\one_proj_parser\health.json', 'w', encoding="utf-8") as file:
#     json.dump(all_categories, file, indent=4, ensure_ascii=False)

#################### Open saved file
with open('C:\Users\dok\Documents\GitHub\one_proj_parser\health.json', encoding="utf-8") as file:
    all_categories = json.load(file)

#################### Counting iterations, used at the beginning of the end of the cycle*, don't get bored, look at the terminal;)
iteration_count = int(len(all_categories))

#################### "count" is used in the middle of the loop for names
count = 0
print(f"all_terations: {iteration_count}")

#################### large loop ... wop wop
for category_name, category_href in all_categories.items(): 

#################### replacing characters and spaces with "_"
            rep = [',', '.', '-', '\'', ' ']
            for item in rep:
                if item in category_name:
                    category_name = category_name.replace(item, "_")
#################### open file to req
            req = requests.get(url=category_href, headers=headers)
            src = req.text

#################### replacing characters and save file
            with open(f"C:\Users\dok\Documents\GitHub\one_proj_parser\data\{count}_{category_name}.html","w", encoding='utf-8') as file:
                file.write(src)
#################### open file
            with open(f"C:\Users\dok\Documents\GitHub\one_proj_parser\data\{count}_{category_name}.html", encoding="utf-8") as file:
                src = file.read()
                soup = BeautifulSoup(src, 'lxml')


                #ALERT!!!!!!!!!!!!!!!!!!!!!!!!!!! <== my first comment 
                alert_block = soup.find(class_='uk-alert-danger')
                if alert_block is not None:
                    continue

#################### creating header for a table
            table_head = soup.find(class_='mzr-tc-group-table').find("tr").find_all("th")
            product = table_head[0].text
            calories = table_head[1].text
            proteins = table_head[2].text
            fats = table_head[3].text
            carbohydrates = table_head[4].text
#################### writing to a file by format "csv"
            with open(f"C:\Users\dok\Documents\GitHub\one_proj_parser\data\{count}_{category_name}.csv", 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow((
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                    
                ))
#################### tag search again
            products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
#################### creating a list is useful for adding data at the end of the cycle
            product_info = []
            for item in products_data:
                products_tds = item.find_all('td')
                title = products_tds[0].find('a').text
                calories = products_tds[1].text
                proteins = products_tds[2].text
                fats = products_tds[3].text
                carbohydrates = products_tds[4].text
#################### added 
                product_info.append({
                    'title': title,
                    'calories': calories,
                    'proteins': proteins,
                    'fats': fats,
                    'carbohydrates': carbohydrates
                    })
#################### saved file
                with open(f"C:\Users\dok\Documents\GitHub\one_proj_parser\data\{count}_{category_name}.csv", 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow((
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                        
                    ))
#################### savet "json"
                with open(f"C:\Users\dok\Documents\GitHub\one_proj_parser\data\{count}_{category_name}.json",'a', encoding='utf-8') as file:
                    json.dump(product_info, file, indent=4, ensure_ascii=False,)

                
            count += 1
            print(f"#Iteration: {count},{category_name} write")
            iteration_count = iteration_count - 1

            if iteration_count ==0:
                print('job is complete...')
                break 

            print(f"#iterations left: {iteration_count}")
            sleep(random.randrange(2,4))























