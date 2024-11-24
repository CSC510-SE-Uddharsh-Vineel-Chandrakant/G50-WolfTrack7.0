from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

known_skills = [
    # Technical Skills
    "Python", "Java", "JavaScript", "C", "C++", "R", "Go", "PHP", "Ruby", "SQL", "MySQL", 
    "MongoDB", "Scala", "Hadoop", "Apache Spark", "Flask", "Django", "React", "ReactJS", 
    "Node.js", "TensorFlow", "Keras", "PyTorch", "FastAI", "NLTK", "Scikit-learn", "NumPy", 
    "Pandas", "Linux", "HTML", "CSS", "TypeScript", "Swift", "Objective-C", 
    "Kubernetes", "Docker", "AWS", "Azure", "Git", "GraphQL", 
    "Tableau", "Power BI", "Google Analytics", "SQL Server", "Oracle", "Looker", 

    # Data-Oriented Skills
    "Machine Learning", "Data Science", "AI", "Data Visualization", "Data Analysis", 

    # Non-Technical Skills
    "Communication", "Teamwork", "Problem Solving", "Leadership", "Project Management", 
    "Time Management", "Critical Thinking", "Creativity", "Adaptability", "Interpersonal Skills", 
    "Conflict Resolution", "Negotiation", "Customer Service", "Analytical Skills", 
    "Presentation Skills", "Research", "Collaboration", "Emotional Intelligence"
]

def to_camel_case(string):
    """Convert a string to camel case."""
    words = string.split()
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

def extract_skills(description):
    """Extract skills from a description based on a list of known skills."""
    # Tokenize the description
    tokens = word_tokenize(description.lower())
    
    # Get English stop words
    stop_words = set(stopwords.words('english'))
    
    # Filter out stop words and create a unique set of tokens
    unique_terms = set(token for token in tokens if token.isalnum() and token not in stop_words)
    
    # Initialize an array to hold found skills
    found_skills = []
    
    # Check for known skills in the description
    for skill in known_skills:
        lower_case_skill = skill.lower()
        
        # Check for exact matches in the tokenized description
        if lower_case_skill in unique_terms:
            found_skills.append(to_camel_case(skill))
        # Also check if the skill is present as a phrase
        elif lower_case_skill in description.lower():
            found_skills.append(to_camel_case(skill))
    
    return list(set(found_skills))