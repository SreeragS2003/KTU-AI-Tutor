import pdfplumber
from litellm import completion
from jinja2 import Environment, FileSystemLoader
import os
import json
#import rag

os.environ["GEMINI_API_KEY"] = os.getenv('GEMINI_API_KEY')

def pdf_txt_extract(filename):
    with pdfplumber.open(filename) as pdf:
        full_txt=""
        for page in pdf.pages:
            full_txt+=page.extract_text()
        return full_txt

def syllabus_txt_to_json(syllabus_txt):
    messages = [
        {
            "role": "user",
            "content": "Extract the course structure from the syllabus text:\n "+syllabus_txt
        }
    ]

    response_schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "Course Structure",
                "description": "Schema for a course structure with modules, topics, and time allotments",
                "type": "object",
                "properties": {
                    "course": {
                        "type": "object", 
                        "properties": {
                            "course_code": { "type": "string", "description": "Course code with no spaces" },
                            "course_title": { "type": "string", "description": "Title of the course" },                            
                            "modules": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "module_title": { "type": "string", "description": "Title of the module without 'Module X' in it" },
                                        "duration": { "type": "string", "description": "Duration of the module in hours" },
                                        "topics": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "number": { "type": "string", "description": "Unique topic identifier" },
                                                    "title": { "type": "string", "description": "Title of the topic" },
                                                    "time": { "type": "integer", "description": "Time allotted to the topic in hours" }
                                                },
                                                "required": ["number", "title", "time"]
                                            }
                                        }
                                    },
                                    "required": ["module_title", "duration", "topics"]
                                }
                            }
                        },
                        "required": ["course_code","course_title","modules"]
                    }
                },
                "required": ["course"]
            }


    res=completion(
        model="gemini/gemini-1.5-flash-8b", 
        messages=messages, 
        response_format={"type": "json_object", "response_schema": response_schema} 
        )
    return json.loads(res.choices[0].message.content)

def get_completion(message):
    messages = [
        {
            "role": "user",
            "content": message
        }
    ]
    res=completion(
        model="gemini/gemini-1.5-flash-8b", 
        messages=messages, 
    )
    return res.choices[0].message.content


syllabus_txt=pdf_txt_extract('syllabus.pdf')
syllabus_json=syllabus_txt_to_json(syllabus_txt)
print(syllabus_json)
#syllabus_json=json.load(open("out2.json",'r'))
print(json.dumps(syllabus_json))



# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))

# Load templates
syllabus_template = env.get_template('syllabus_template.html')
topic_template = env.get_template('topic_template.html')
from rag import get_rag_completion
def syllabus_json_to_file_structure(syllabus_json):
    # Base directory for the course
    base_dir = syllabus_json["course"]["course_code"]
    os.makedirs(base_dir, exist_ok=True)

    # Render main syllabus HTML
    syllabus_html = syllabus_template.render(course=syllabus_json['course'])
    with open(os.path.join(base_dir, "syllabus_structure.html"), "w") as file:
        file.write(syllabus_html)
    
    # Create module and topic structure
    for module in syllabus_json["course"]["modules"]:
        module_dir = os.path.join(base_dir, module["module_title"])
        os.makedirs(module_dir, exist_ok=True)
        
        # Generate individual topic files within each module folder
        for topic in module["topics"]:
            course_title=syllabus_json["course"]["course_title"]
            topic_title=topic["title"]
            content=get_rag_completion( f"""In the context of a college course on "{course_title}", 
                        create course text for the topic "{topic_title}"  
                        Use the content from the given documents given whenever possible with attribution.
                        Make sure that your output should have at least everything on this topic that the given notes have 
                        but strip out any credits or non-textual elements not directly relating to the topic. Explain in some detail.
            """)
            
            topic_html = topic_template.render(topic=topic,content=content)
            topic_filename = os.path.join(module_dir, f"{topic['number']}.html")
            with open(topic_filename, "w") as topic_file:
                topic_file.write(topic_html)
    
    print(f"File structure created under '{base_dir}'")


syllabus_json_to_file_structure(syllabus_json)
