""""
Description: 
Web Scraper utilizing atleast 1 algorithm and 2 data structures that 
searches and returns a list of scholarships in a txt file
based on specific filters and keywords.

Contributors:
Halil Hamscho 
Tofik Hamscho 

Last Data Modified: 11/24/2023
"""
from datetime import datetime, date
from bs4 import BeautifulSoup
import requests

def fetch_html(url):
    """Fetch HTML content from a given URL."""
    response = requests.get(url)
    return response.text

def filter_scholarships(soup, keywords):
    """Filter scholarships based on given keywords."""
    filtered_scholarships = []
    scholarships = soup.find_all('article', class_='scholarship')

    # Iterate over each scholarship
    for scholarship in scholarships:
        # Get the 'more' section or description
        description = scholarship.find('div', class_='info')
        if description:
            description_text = description.get_text().lower() # Convert to lowercase for case-insensitive search
            # Check if any of the keywords are in the description
            if any(keyword.lower() in description_text for keyword in keywords):
                filtered_scholarships.append(scholarship)
    return filtered_scholarships

def extract_scholarship_info(filtered_scholarships):
    """Extract necessary information from each filtered scholarship."""
    matching_scholarships = []
    for scholarship in filtered_scholarships:
        scholarship_name = scholarship.find('h3').text.strip()

        # Extracting status, deadline, and location
        p_text = scholarship.find('p').get_text(strip=True)
        status, deadline, location = p_text.split('|')

        # Cleaning up the p text to remove extra spaces and the 'Deadline:' part
        deadline = deadline.replace('Deadline:', '').strip()

        scholarship_url = scholarship.find('a', {'class': 'text-btn'}).get('href')

        # Create a dictionary with the scholarship info
        scholarship_info = {
            'Name': scholarship_name,
            'Deadline': deadline,
            'URL': scholarship_url
        }
        # Append the dictionary to the list
        matching_scholarships.append(scholarship_info)

    return matching_scholarships

def convert_to_datetime(date_str):
    """Convert date string to datetime object."""
    try:
        # Creates Date to Numerical Value Ex. June 6th, 2023 -> 6 6 2023
        return datetime.strptime(date_str, '%B %d, %Y')
    except ValueError:
        # Return a default date if the parsing fails
        return datetime.max

def sort_scholarships_by_date(matching_scholarships):
    """Sort scholarships by date from today's date."""
    today = date.today()
    sorted_scholarships = sorted(matching_scholarships, key=lambda x: convert_to_datetime(x['Deadline']))

    # Implementing stack with earliest to latest
    return [sch for sch in sorted_scholarships if convert_to_datetime(sch['Deadline']).date() >= today]

def write_scholarships_to_file(scholarships, filename="scholarships.txt"):
    """Write the list of scholarships to a text file."""
    with open(filename, 'w') as file:
        for scholarship in scholarships:
            file.write(f"Name: {scholarship['Name']}\n")
            file.write(f"Deadline: {scholarship['Deadline']}\n")
            file.write(f"URL: {scholarship['URL']}\n")
            file.write("\n")  # Add a blank line between scholarships

def main():
    """Main Driver Code"""
    # Use the data processing part in Pandas Library - Teymorian
    base_url = 'https://scholarshipamerica.org/students/browse-scholarships/'

    # Total number of pages including the first one
    total_pages = 9  # Replace if page numbers change

    all_scholarships = []

    # Asking user for input keywords
    user_input = input("Enter keywords to filter scholarships (separated by commas): ")
    keywords = [keyword.strip() for keyword in user_input.split(',')]

    for page in range(1, total_pages + 1):
        if page == 1:
            url = base_url  # The first page has a different URL structure
        else:
            url = f"{base_url}?fwp_paged={page}"

        print(f"Processing page {page}...")
        html = fetch_html(url)

        # Beautiful soup object
        soup = BeautifulSoup(html, 'lxml')

        filtered_scholarships = filter_scholarships(soup, keywords)
        all_scholarships.extend(extract_scholarship_info(filtered_scholarships))

    # Sort and write all scholarships from all pages to a file
    sorted_scholarships = sort_scholarships_by_date(all_scholarships)

    # Write scholarships from stack to list them by earliest date
    write_scholarships_to_file(sorted_scholarships)
    print(f"Scholarships filtered by {', '.join(keywords)} have been written to scholarships.txt")

if __name__ == "__main__":
    main()
