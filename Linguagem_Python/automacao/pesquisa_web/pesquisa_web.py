import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs
from PIL import Image

pyautogui.FAILSAFE=True

def demo():# via NAME (html/CSS)
   
    driver = webdriver.Chrome()
    driver.get("http://www.python.org") # https://scholar.google.com.br/ , https://scielo.org/ , https://www.science.gov/ , https://eric.ed.gov/ , 
    assert "Python" in driver.title
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    time.sleep(5)
    driver.close()


def demo_2(): # barra de pesquisa google

    driver = webdriver.Chrome()
    # Clique na barra de pesquisa
    pyautogui.press('browsersearch') 
    pyautogui.typewrite('selenium python') 
    pyautogui.press('enter')
    assert "No results found." not in driver.page_source # espera carregar
    pyautogui.scroll(-600)
    time.sleep(5)
    # ...
    driver.close()


def demo_3(): #via XPath (inspecionar)
   
    driver = webdriver.Chrome()
    driver.get("http://www.python.org")
    #XPath :  navegador->bt direito->inspecionar->icon->select->Copy XPath
    driver.find_element("xpath",'//*[@id="top"]/nav/ul/li[4]/a').click() 
    driver.find_element("xpath",'//*[@id="search"]').send_keys('selenium')
    driver.find_element("xpath",'//*[@id="content"]/div[1]/div/form/button').click()
    time.sleep(5)
    driver.close()


def demo_4(): # encontra itens de um menu, e clica em cada um
   
    driver = webdriver.Chrome()
    driver.get("https://www.python.org")
    driver.maximize_window()
    #Tags : HTML (inspecionar)

    # Mapeiar elementos

    #links = driver.find_elements(By.TAG_NAME, 'a') #encontra links
    
    
    menus = driver.find_elements(By.CLASS_NAME, 'menu') #encontra menu
    ListaTitle = [item_web_element.get_attribute('title') for item_web_element in menus] #pega os atributos em strings
    print("\nLista_atributo_title: ",ListaTitle)
    menu_options = menus[0].find_elements(By.TAG_NAME, 'a') #pega primeiro menu, encontra links
    ListaTitleOptions = [item_web_element.get_attribute('title') for item_web_element in menu_options] #pega primeiro menu, encontra links
    print("\nLista_filtrada_atributo_title: ",ListaTitleOptions)

    # Navegação

    wait = WebDriverWait(driver, 3)
    #percorrer links
    i=1
    total=len(menu_options)
    for element in menu_options[i:]: # começa a partir do 'i'
        print(f"item: {i+1}/{total}\n")
        try:
            '''
            try: # botão deve estar visivel na tela
                wait.until(EC.visibility_of_element_located(title))
            except:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'})",element) # scroll na página para aparecer o botão
            '''
            
            #element.click()
            element_click = wait.until(EC.element_to_be_clickable(element)) # aguarda carregar
            element_click.click()
            print("click!\n")

            '''
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight, duration=2000);")

            time.sleep(1)
            driver.execute_script("window.scrollTo(0, -200);")
            '''

            time.sleep(2)
            url = driver.current_url
            #if(url != 'https://www.python.org/'):
            driver.back()
                
            '''
            # botão direito -> abrir em nova guia
            
            #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') # nova guia
            #wait.until(driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't'))
            #window_name = driver.window_handles[-1]
            #driver.switch_to.window(window_name)
            
            '''
            
        except:
            print(f'Erro!\n')
        print("--------------")
        i+=1

    #driver.close()

def demo_5(): #  locateAll

    driver = webdriver.Chrome()
    driver.get("https://www.python.org")
    driver.maximize_window()
    time.sleep(2)
    #pyautogui.screenshot('c:/Users/Keslley/gitHub/Portifolio/Linguagem_Python/automacao/pesquisa_web/screen.png')
    screenshot = pyautogui.screenshot()
    screenshot.save('c://Users//Keslley//gitHub//Portifolio//Linguagem_Python//automacao//pesquisa_web//screen.png')
    #Image.open('screen.png').convert('RGB').save('screen.png')
    positions_list =list(pyautogui.locateAllOnScreen('c://Users//Keslley//gitHub//Portifolio//Linguagem_Python//automacao//pesquisa_web//screen.png'))
    
    print(positions_list)
    for i in positions_list:
        if (i[0]==0 and i[1]==0): continue # pula failsafe
        pyautogui.moveTo(i[1], i[0])
        #pyautogui.click(i.x, i.y)
        #pyautogui.rightClick(i.x, i.y)
        time.sleep(2)
    print('Done!\n')
    

def demo_6(): # input de url, entra no 1o link (e salva titulo para txt)

    val = input("Enter a url: ")
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 3)
    #driver.get(val)  #apenas para url válidas
    #wait.until(EC.url_to_be(val))
    driver.get("https://www.google.com") #url qualquer
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys(val)
    elem.send_keys(Keys.RETURN)
    link = driver.find_element(By.CLASS_NAME, 'srp').find_element(By.CLASS_NAME, 'main').find_element(By.ID, 'cnt').find_element(By.ID, 'rcnt').find_element(By.TAG_NAME, 'a') #entra no primeiro link da pesquisa
    #link = driver.find_element(By.ID, 'main')
    #wait.until(EC.element_to_be_clickable(link))
    link.click()
    #time.sleep(2)

    get_url = driver.current_url
    print("The current url is:"+str(get_url)+"\n")


    # get and write ( problema com proxy do navegador )
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,features="html.parser")
    title = soup.title.text
    file=codecs.open('c:/Users/Keslley/gitHub/Portifolio/Linguagem_Python/automacao/pesquisa_web/article_titles.txt', 'a+')
    file.write(title+"\n")
    file.close()
    print('Done!\n')


def login(url,username_id,password_id,submit_button_id):
   driver.get(url)
   driver.find_element_by_id(username_id).send_keys("username")
   driver.find_element_by_id(password_id).send_keys("password")
   driver.find_element_by_id(submit_button_id).click()



if __name__ == "__main__":
    #demo()
    #demo_2()
    #demo_3()
    #demo_4()
    #demo_5()
    demo_6()
    


