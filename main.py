from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


def makerows(row):
    """
    This is just to show a bit of string manipulation and list handling.
    Will build a string of everything until the first digit is encountered.
    Then builds a list with that and a split (on empty) of the rest of the row.
    * = unpack (unpacks list into individual elements
        Used to avoid creating a temp, throw-away variable
    :param row: current row of table (as full string)
    :return: list of Statical description(str), Team(str,int,float), and Opponents(str,int,float)
    """

    words = ""

    for i, letter in enumerate(row):
        if not letter.isdigit():
            words += letter
        else:
            return [words.strip(), *row[i:].split(" ")]


"""
Basic overview of selenium over Beautiful Soup for webscrapping.
Loads multiple select options of a table then grabs the data.
Not optimized (good candidate for moving to async or multiprocess with bots)
"""
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://fgcuathletics.com/sports/womens-soccer/stats/2022")
    assert "Page not found" not in driver.page_source
    # To get the first five - a simple loop. You could add that threading here


    for i in range(1, 4):

        select = Select(driver.find_element(By.XPATH, "//select"))
        select.select_by_index(i)

        #click automatization
        driver.find_element(By.LINK_TEXT, "GAME-BY-GAME").click()
        driver.find_element(By.ID, "ui-id-12").click()
        driver.find_element(By.LINK_TEXT, "OUR OFFENSIVE STATS").click()

        table_rows = []

        # //section[@id='game-game-our-offensive']

        table_data = driver.find_elements(By.XPATH, "//section[@id='game-game-our-offensive']//table[1]//thead//tr//th")
        # rather than [0:3] - just get any non-empty headers
        table_rows.append([h.text for h in table_data if h.text])

        table_data = driver.find_elements(By.XPATH, "//section[@id='game-game-our-offensive']//table[1]/tbody/tr")
        for row in table_data:
            if row.text:
                cur_row = makerows(row.text)
    # if cur_row is blank it will return None so check that & length
            if cur_row is None or len(cur_row) == 1:
                continue
            else:
                table_rows.append(cur_row)

        for i, row in enumerate(table_rows):
            with open('2022_sport.txt', 'w') as f:
                f.write(f"Row {i} is: {row}")
            print(f"Row {i} is: {row}")


driver.close()
