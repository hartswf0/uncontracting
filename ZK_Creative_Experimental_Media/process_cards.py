from bs4 import BeautifulSoup
import re

def extract_force_content(value_div):
    # Extract title
    title = value_div.find('strong').text
    
    # Extract tags
    tags_div = value_div.find('div', class_='tags')
    tags = [tag.text for tag in tags_div.find_all('span', class_='tag')] if tags_div else []
    
    # Extract description
    description = []
    desc_list = value_div.find('ul')
    if desc_list:
        description = [li.text for li in desc_list.find_all('li')]
    
    # Extract features
    features = None
    features_p = value_div.find('p', string=re.compile(r'Features:'))
    if features_p:
        features = features_p.text.split('Features:')[1].strip()
    
    return {
        'title': title,
        'tags': tags,
        'description': description,
        'features': features
    }

def generate_card_html(force_type, parent_title, content):
    card_html = f'''
    <div class="notecard {force_type.lower()}">
        <div class="notecard-header">
            <div class="parent-title">{parent_title}</div>
            <div class="force-type">{force_type}</div>
        </div>
        <div class="notecard-content">
            <h3>{content['title']}</h3>
            <div class="tags">
                {' '.join(f'<span class="tag">{tag}</span>' for tag in content['tags'])}
            </div>
            <div class="description">
                <strong>Description:</strong>
                <ul>
                    {' '.join(f'<li>{item}</li>' for item in content['description'])}
                </ul>
            </div>
            <div class="features">
                <strong>Features:</strong> {content['features']}
            </div>
        </div>
    </div>
    '''
    return card_html

def generate_cards_html():
    # Read the original HTML
    with open('index.html', 'r') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    # Start building the new HTML
    cards_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Force Cards</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }
        
        .card-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .notecard {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .notecard.opposing {
            border-top: 3px solid #c0392b;
        }
        
        .notecard.supporting {
            border-top: 3px solid #27ae60;
        }
        
        .notecard-header {
            padding: 15px;
            background: #f8f9fa;
            border-bottom: 1px solid #eee;
        }
        
        .parent-title {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .force-type {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .notecard.opposing .force-type {
            color: #c0392b;
        }
        
        .notecard.supporting .force-type {
            color: #27ae60;
        }
        
        .notecard-content {
            padding: 20px;
        }
        
        .notecard-content h3 {
            margin: 0 0 15px 0;
            color: #2c3e50;
        }
        
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-bottom: 15px;
        }
        
        .tag {
            background: #f0f2f5;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            color: #2c3e50;
        }
        
        .description, .features {
            margin-bottom: 15px;
        }
        
        .description ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .description li {
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="card-container">
    '''

    # Process each force card
    force_cards = soup.find_all('div', class_='force-card')
    for card in force_cards:
        # Get the parent title
        parent_title = card.find('div', class_='force-name').text.strip()
        
        # Find opposing and supporting forces
        force_content = card.find('div', class_='force-content')
        opposing_value = force_content.find_all('div', class_='value')[0]
        supporting_value = force_content.find_all('div', class_='value')[1]
        
        # Extract content for both forces
        opposing_content = extract_force_content(opposing_value)
        supporting_content = extract_force_content(supporting_value)
        
        # Generate HTML for both cards
        cards_html += generate_card_html('Opposing Force', parent_title, opposing_content)
        cards_html += generate_card_html('Supporting Force', parent_title, supporting_content)

    # Close the HTML
    cards_html += '''
    </div>
</body>
</html>
    '''

    # Write the new HTML file
    with open('cards.html', 'w') as file:
        file.write(cards_html)

if __name__ == '__main__':
    generate_cards_html()
