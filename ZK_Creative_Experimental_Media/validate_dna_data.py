from bs4 import BeautifulSoup
import json
import re

def extract_data_from_html(html_path):
    """Extract the data object from the creative-dna.html file."""
    with open(html_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    # Find the script tag containing our data
    scripts = soup.find_all('script')
    data_script = None
    for script in scripts:
        if script.string and 'const data = ' in script.string:
            data_script = script.string
            break
    
    if not data_script:
        raise ValueError("Could not find data object in HTML")
    
    # Extract everything between the first { and the last }
    start_idx = data_script.find('{')
    end_idx = data_script.rfind('}')
    if start_idx == -1 or end_idx == -1:
        raise ValueError("Could not find data object boundaries")
        
    json_str = data_script[start_idx:end_idx+1]
    
    # Clean up the string to make it valid JSON
    # Remove trailing commas in arrays and objects
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        # If there's still an error, print the problematic section
        error_pos = e.pos
        context = 100  # Show 100 chars before and after the error
        start = max(0, error_pos - context)
        end = min(len(json_str), error_pos + context)
        print(f"\nError near position {error_pos}:")
        print(json_str[start:end])
        print(" " * (error_pos - start) + "^")  # Point to the error
        raise ValueError(f"Invalid JSON data: {e}")

def validate_data_structure(data):
    """Validate the structure of the extracted data."""
    # Check top level structure
    assert isinstance(data, dict), "Data should be a dictionary"
    assert "documents" in data, "Data should have 'documents' key"
    assert isinstance(data["documents"], list), "Documents should be a list"
    
    # Check each document
    for doc in data["documents"]:
        assert isinstance(doc, dict), "Each document should be a dictionary"
        required_keys = ["id", "documentTitle", "color", "geneticPlatforms"]
        for key in required_keys:
            assert key in doc, f"Document missing required key: {key}"
        
        # Check platforms
        assert isinstance(doc["geneticPlatforms"], list), "geneticPlatforms should be a list"
        for platform in doc["geneticPlatforms"]:
            assert isinstance(platform, dict), "Each platform should be a dictionary"
            platform_keys = ["platformID", "title", "keyConcept", "example"]
            for key in platform_keys:
                assert key in platform, f"Platform missing required key: {key}"

def print_data_stats(data):
    """Print statistics about the data."""
    print("\nData Validation Results:")
    print("-" * 50)
    
    num_docs = len(data["documents"])
    print(f"Number of documents: {num_docs}")
    
    for doc in data["documents"]:
        print(f"\nDocument: {doc['id']}")
        print(f"Title: {doc['documentTitle']}")
        print(f"Number of platforms: {len(doc['geneticPlatforms'])}")
        print("Sample platforms:")
        for i, platform in enumerate(doc['geneticPlatforms'][:3], 1):
            print(f"  {i}. {platform['title']}")
        if len(doc['geneticPlatforms']) > 3:
            print(f"  ... and {len(doc['geneticPlatforms'])-3} more")

def main():
    html_path = "creative-dna.html"
    json_path = "creative-data.json"
    try:
        print("Extracting data from HTML...")
        data = extract_data_from_html(html_path)
        
        print("Validating data structure...")
        validate_data_structure(data)
        
        print("Saving data to JSON file...")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print_data_stats(data)
        print(f"\nData successfully saved to {json_path} ")
        
    except Exception as e:
        print(f"\nError: {str(e)} ")
        raise

if __name__ == "__main__":
    main()
