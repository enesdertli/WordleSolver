import time
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import os


def choose_random_word_from_txt(file_path):
    with open(file_path,'r', encoding="utf-8") as file:
        words = file.read().splitlines()
    return random.choice(words), words


def choose_random_word_from_list(filtered_words):
    if not filtered_words:
        print("Warning: Filtered words list is empty!")
        raise ValueError("Filtered words list is empty!")
    return random.choice(filtered_words)


def check_feedback(feedback_sequence, guessed_word, word):
    for i, feedback in enumerate(feedback_sequence):
        if feedback == '0' and guessed_word[i] in word:
            return False
        elif feedback == '1' and (guessed_word[i] not in word or guessed_word[i] == word[i]):
            return False
        elif feedback == '2' and guessed_word[i] != word[i]:
            return False
    return True


def filter_words(feedback_sequence, guessed_word, words):
    filtered_words = []

    for word in words:
        if check_feedback(feedback_sequence, guessed_word, word):
            filtered_words.append(word)
    return filtered_words


def main():
    edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')
    edge_service = Service(edge_driver_path)

    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--enable-chrome-browser-cloud-management")


    driver = webdriver.Edge(service=edge_service, options=edge_options)
    driver.get("https://wordleturkce.bundle.app")

    solved = False
    file_path = "5-letter-words.txt"
    

    try:
        # Try clicking on current mouse position
        actions = ActionChains(driver)
        actions.click()
        actions.perform()
        time.sleep(2)
    except:
        # Temporary workaround: manually close button
        print("Click the close button (auto-click failed)")
        time.sleep(3)

    selected_word, words = choose_random_word_from_txt(file_path)


    count = 0

    print("Meanings of the numbers in this sequence:")
    print("  0: The guessed letter is incorrect.")
    print("  1: The guessed letter is correct, but in the wrong position.")
    print("  2: The guessed letter is correct and in the correct position.")
    print(f"\nFirst random selected word is {selected_word}")

    while not solved:
        count += 1
        for _ in selected_word:
            actions.send_keys(_)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        
        print("\nTo end the game, type 'na'.")
        print("To change the selected word, type 'ch'.")

        feedback_sequence = input("Feedback Sequence: 0, 1, 2 : ")
        if feedback_sequence.lower() == 'na':
            solved = True
            print("game completed")
            break

    
        guessed_word = selected_word
        filtered_words = filter_words(feedback_sequence, guessed_word, words)
        time.sleep(2)
        
        with open("test_"+str(count)+".txt",'w',encoding='utf-8') as output_file:
            for word in filtered_words:
                output_file.write(word + "\n")
    
        words = filtered_words
        time.sleep(1)

        selected_word = choose_random_word_from_list(words)
        selected_word_replace = selected_word
        selected_word_replace = selected_word.replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş','s').replace('ğ','g').replace('ç','c')

        print(f"\nselected word: {selected_word_replace}")
        print("#############################")

        if not filtered_words:
            print("no suitable word found!")
            continue


if __name__ == "__main__":
    main()



     
