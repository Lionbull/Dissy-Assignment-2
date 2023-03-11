from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import requests

tree = ET.parse('db.xml')
root = tree.getroot()

print("Server started")

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
        
    
    def check_topic_exists(topic):
        """Checks if a topic exists in the database"""

        exists = False
        for child in root:
            if (child.attrib['name'] == topic):
                exists = True

        return exists
    
    server.register_function(check_topic_exists, "check_topic_exists")

    def list_topics():
        """Returns a list of all the existing topics"""

        topics = []
        for child in root:
            topics.append(child.attrib)
        return topics

    server.register_function(list_topics, "list_topics")

    def get_content_of_topic(topic):
        """Returns the content of a topic"""

        topic_content = []

        for child in root:
            if (child.attrib['name'] == topic):

                # Getting the content of the topic inside the note tag
                topic_content.append(child.find("note").find("text").text)
                topic_content.append(child.find("note").find("timestamp").text)

                return topic_content
            
    server.register_function(get_content_of_topic, "get_content_of_topic")

    def add_data_to_existing_topic(topic, text, timestamp):
        """If topic that user wants exists, appends text to the existing topic"""

        for child in root:
            # Finding the topic to which data needs to be added
            if (child.attrib['name'] == topic):

                note = child.find("note")

                # Finding the existing text and appending the new text
                existing_text = note.find("text").text
                new_text = f"{existing_text}\n{text}"
                note.find("text").text = new_text

                # Updating the timestamp
                note.find("timestamp").text = timestamp

                tree.write('db.xml')
                # Returning True if data was added successfully
                return True
        
        # Returning False if data was not added
        return False

    server.register_function(add_data_to_existing_topic, "add_data_to_existing_topic")

    def add_new_topic(topic, text, timestamp):
        """If topic that user wants does not exist, creates a new topic"""

        # Adding new topic to the root
        new_topic = ET.SubElement(root, 'topic', name=topic)
        new_note = ET.SubElement(new_topic, 'note')
        new_text = ET.SubElement(new_note, 'text')
        new_timestamp = ET.SubElement(new_note, 'timestamp')

        new_text.text = text
        new_timestamp.text = timestamp

        tree.write('db.xml')
        return True

    server.register_function(add_new_topic, "add_new_topic")

    def wikipedia_data_search(topic):
        """Function to search for a topic on Wikipedia"""
        
        S = requests.Session()

        URL = "https://en.wikipedia.org/w/api.php"

        SEARCHPAGE = topic

        PARAMS = {
            "action": "opensearch",
            "namespace": "0",
            "search": SEARCHPAGE,
            "limit": "1",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        print(DATA)
        
        return DATA

    server.register_function(wikipedia_data_search, "wikipedia_data_search")


    # Run the server's main loop
    server.serve_forever()