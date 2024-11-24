from flask import Flask, render_template, request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import spacy
# python -m spacy download en_core_web_md
# Load the spaCy model with word vectors


app = Flask(__name__)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nlp = spacy.load("en_core_web_md")

lemmatizer = WordNetLemmatizer()
sample_skills = {'python', 'java', 'javascript', 'communication', 'teamwork', 'problem-solving', 'leadership', 'data analysis','AI','ML','c','r', 'c++','hadoop','scala','flask','pandas','spark','scikit-learn',
                'numpy','php','sql','mysql','css','mongdb','nltk','fastai' , 'keras', 'pytorch','tensorflow','linux','Ruby','django','react','reactjs','ai','ui','tableau'}
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    
    # Remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens

allSkills = [
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

def extract_skills(text):
    print(text)
    doc = nlp(text)
    skills = []
    for token in doc:
        # Check if the token is similar to any of the sample skills
        for skill in sample_skills:
            similarity = nlp(skill).similarity(token)
            if similarity > 0.7:  # Adjust the threshold as needed
                skills.append(token.text)
                break  # Move to the next token once a similar skill is found
    return list(set(skills))