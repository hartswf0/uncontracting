import json
from html.parser import HTMLParser

class ForceCardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards_data = []
        self.current_card = None
        self.current_force = None
        self.in_force_name = False
        self.in_force_content = False
        self.in_value = False
        self.in_tags = False
        self.in_description = False
        self.in_strong = False
        self.in_tag_span = False
        self.current_tags = []
        self.current_description = []
        self.force_index = 0  # 0 for opposing, 1 for supporting
        self.found_label = False
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and 'class' in attrs:
            classes = attrs['class'].split()
            if 'force-card' in classes:
                print("Creating new force card")
                self.current_card = {}
                self.force_index = 0
            elif 'force-name' in classes:
                print("Entering force name")
                self.in_force_name = True
            elif 'force-content' in classes:
                print("Entering force content")
                self.in_force_content = True
            elif 'label' in classes:
                self.found_label = True
            elif 'value' in classes and self.found_label:
                print("Entering value section")
                self.in_value = True
                self.current_force = {'tags': [], 'description': [], 'features': ''}
                self.found_label = False
            elif 'tags' in classes and self.in_value:
                print("Entering tags section in value")
                self.in_tags = True
                self.current_tags = []
        elif tag == 'strong' and self.in_value:
            self.in_strong = True
        elif tag == 'ul' and self.in_value:
            self.in_description = True
            self.current_description = []
        elif tag == 'span' and 'class' in attrs:
            classes = attrs['class'].split()
            if 'tag' in classes and self.in_tags:
                self.in_tag_span = True
            
    def handle_endtag(self, tag):
        if tag == 'div':
            if self.in_force_name:
                self.in_force_name = False
            elif self.in_value:
                if self.current_force:
                    if self.force_index == 0:
                        print(f"Adding opposing force: {self.current_force}")
                        self.current_card['opposing'] = self.current_force.copy()
                        self.force_index = 1
                    else:
                        print(f"Adding supporting force: {self.current_force}")
                        self.current_card['supporting'] = self.current_force.copy()
                        self.cards_data.append(self.current_card.copy())
                        print(f"Added card: {self.current_card}")
                        self.current_card = None
                        self.force_index = 0
                self.in_value = False
                self.current_force = None
            elif self.in_force_content:
                self.in_force_content = False
            elif self.in_tags:
                self.in_tags = False
                if self.current_force:
                    self.current_force['tags'] = self.current_tags.copy()
        elif tag == 'strong':
            self.in_strong = False
        elif tag == 'ul':
            if self.in_description and self.current_force:
                self.current_force['description'] = self.current_description.copy()
            self.in_description = False
        elif tag == 'span':
            self.in_tag_span = False
                
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
            
        if self.in_force_name and self.current_card is not None:
            emoji = data[0]
            title = data[1:].strip()
            print(f"Found force name: {title} ({emoji})")
            self.current_card['emoji'] = emoji
            self.current_card['title'] = title
        elif self.in_value:
            if 'Features:' in data:
                features = data.split('Features:')[1].strip()
                if self.current_force:
                    print(f"Found features: {features}")
                    self.current_force['features'] = features
            elif self.in_strong and not self.current_force.get('title'):
                print(f"Found force title: {data}")
                self.current_force['title'] = data.strip()
            elif self.in_description and data.startswith('-'):
                desc = data[1:].strip()
                print(f"Found description item: {desc}")
                self.current_description.append(desc)
            elif self.in_tag_span:
                tag = data.strip()
                if tag and not tag.startswith('Tags:'):
                    print(f"Found tag: {tag}")
                    self.current_tags.append(tag)

def extract_data():
    print("Starting data extraction...")
    try:
        with open('index.html', 'r') as file:
            print("Reading index.html...")
            html_content = file.read()
            print("Successfully read HTML")
            
        parser = ForceCardParser()
        parser.feed(html_content)
        print(f"Found {len(parser.cards_data)} force cards")
        
        # Write to JSON file
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(parser.cards_data, f, ensure_ascii=False, indent=2)
            print("Successfully wrote data.json")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    extract_data()
