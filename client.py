import xmlrpc.client
from datetime import datetime

server = xmlrpc.client.ServerProxy('http://localhost:8000')

def main():
    while True:
        # Showing the menu
        print("\nMenu: ")
        choice = input("1. Add/Edit topic\n2. Get content of a topic\n3. Search for data in Wikipedia\nEnter your choice: ")

        # Listing all the existing topics
        list_existing_topics()


        if choice == "1":
            add_edit_topic()
        elif choice == "2":
            get_content_of_topic()
        elif choice == "3":
            search_wikipedia()
        else:
            print("Invalid choice. Please try again.")
            continue

def search_wikipedia():
    """Function for initiate a search for a data on Wikipedia"""
    topic = input("\nWhat would you like to search in Wikipedia: ")

    # Getting the search results from the server
    search_results = server.wikipedia_data_search(topic)

    if search_results[1][0] == topic:
        print(f"\n##########\nYour search page '{topic}' exists on English Wikipedia")
        print(f"\n##########\nSearch results: \n{search_results[3][0]}\n##########")
        append_choise = input("Would you like to append the search results to the existing topic? (y/n): ")
        if append_choise == "y":
            # Getting current date and time to create a timestamp
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Checking if the topic exists in the database
            topic_exists = server.check_topic_exists(topic)

            # Adding a new topic to the database
            if topic_exists == False:
                new_topic_added = server.add_new_topic(topic, search_results[3][0], timestamp)
                if new_topic_added == True:
                    print(f"\n##########\nNew topic '{topic}' added to the database.\n##########")
                else:
                    print("\n##########\nError in adding new topic to the database.\n##########")
                    return
            # Adding data to the existing topic
            else:
                data_added = server.add_data_to_existing_topic(topic, search_results[3][0], timestamp)

                # Checking if data was added successfully and printing the result
                if data_added == True:
                    print(f"\n##########\nLink appended to the existing topic '{topic}'\n##########")
                else:
                    print("\n##########\nError in adding data to the existing topic.\n##########")

        elif append_choise == "n":
            print("\n##########\nLink not appended to the existing topic.\n##########")
        else:
            print("\n##########\nInvalid choice. Text not appended to the existing topic.\n##########")
    else:
        print(f"\n##########\nYour search page '{topic}' does not exist on English Wikipedia\n##########")

def list_existing_topics():
    """Function for listing all the existing topics"""

    # Getting the list of existing topics
    existing_topics = server.list_topics()

    # Printing the list of existing topics
    print("\n##########\nExisting topics: ")
    for topic in existing_topics:
        print(topic['name'])


def get_content_of_topic():
    # Getting the topic from the user
    topic = input("\nEnter the topic: ")

    topic_content = server.get_content_of_topic(topic)
    print(f"\n##########\nContent of topic '{topic}': \n{topic_content[0]} \n\nThe last edit on the topic was made: {topic_content[1]} \n##########")


def add_edit_topic():
    """Function for adding or editing a topic"""

    # Getting the topic from the user
    topic = input("\nEnter the topic: ")

    # Checking if topic exists
    topic_exists = server.check_topic_exists(topic)

    # If topic exists, append text to the existing topic
    if topic_exists == True:
        print("\n##########\nTopic already exists. Text will be appended to the existing topic.\n##########")
        text = input("Enter the text: ")

        # Getting current date and time to create a timestamp
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data_added = server.add_data_to_existing_topic(topic, text, timestamp)

        # Checking if data was added successfully and printing the result
        if data_added == True:
            print(f"\n##########\nFollowing text appended to the existing topic '{topic}': \n{text}\n##########")
        else:
            print("\n##########\nError in adding data to the existing topic.\n##########")

    # If topic does not exist, create a new topic
    else:
        print("\##########\nTopic does not exist. Topic will be created.")
        text = input("Enter the text: ")

        # Getting current date and time to create a timestamp
        timestamp = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        data_added = server.add_new_topic(topic, text, timestamp)

        # Checking if data was added successfully and printing the result
        if data_added == True:
            print(f"\n##########\nNew topic '{topic}' created with following text: \n{text}\n##########")
        else:
            print("\n##########\nError in adding new topic with the data.\n##########")

    
main()