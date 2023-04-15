import json
import os



def dataProcessingFromKeywords():
    # Specify the directory path
    directory = 'json'
    json_file = ""

    # List all files inside the directory
    files = os.listdir(directory)

    # Filter out JSON files based on their extension
    json_files = [file for file in files if file.endswith('.json')]

    # Check if there is at least one JSON file in the directory
    if json_files:
        # Assuming there is only one JSON file in the directory, you can access it using index 0
        json_file = json_files[0]

    else:
        print("No JSON file found in the directory.")

    file_path = f"./json/{json_file}"  # Update with your actual file path

    keywords = ['html', 'css', 'js', 'javascript', 'mern', 'mongo', 'node js', 'react js', 'react developer',
                'node developer', 'ui developer', 'java backend developer', 'java', 'python', 'redux', 'typescript',
                'cypress', 'jest', 'developer', 'web design', 'web development', 'jwt', 'passport js', 'docker',
                'kubernetes', 'heroku', 'firebase', 'material ui', 'react router', 'ant design', 'chakra ui',
                'tailwind css', 'storybook', 'styled components', 'express', 'mongoose', 'API', 'RESTful', 'GraphQL',
                'Apollo', 'Java Spring', 'Spring Boot',
                'Hibernate', 'JPA', 'Redux Saga', 'Next.js', 'Gatsby', 'Serverless', 'Authentication', 'Authorization',
                'OAuth',
                'Passport', 'JSON Web Tokens', 'Cookies', 'Session Management', 'Responsive Design',
                'Cross-browser Compatibility',
                'Performance Optimization', 'Code Review', 'Git', 'Agile', 'Scrum', 'Unit Testing',
                'Integration Testing']

    processedData = []  # Array to store matching objects



    with open(file_path, "r") as f:
        data = json.load(f)  # Load JSON data from file
        for obj in data:
            # Convert jobTitle and otherDetails to lowercase for case-insensitive comparison
            job_title = obj.get("jobTitle", "").lower()
            other_details = obj.get("otherDetails", "").lower()

            # Check if any of the keywords are present in jobTitle or otherDetails
            if any(keyword in job_title or keyword in other_details for keyword in keywords):
                processedData.append(obj)  # Add the object to the processedData array

    # Print the processedData array
    # Write processedData to a new JSON file inside json folder
    with open("./json/processedData.json", "w") as f:
        json.dump(processedData, f, indent=2)

    print("Processed data written to ./json/processedData.json")


