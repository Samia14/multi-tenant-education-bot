"""Generate Embedding for the set chunk of the text"""
import openai
import os
from config import OPENAI_EMBEDDING_MODEL_NAME

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_embedding(text:list):
    """This function will generate embedding for the given input text data."""
    try:
        response = openai.embeddings.create(
        input=text,
        model=OPENAI_EMBEDDING_MODEL_NAME,
        encoding_format= "float",
        dimensions=1536
    )   
        
        
        return response.data[0].embedding
    except Exception as E:
        print(E)
        return ''

input_text = "On the other hand, the impact of a loaded truck on a body coming its way is very large even if the truck is moving slowly. To explain such situation, we define a new physical quantity called momentum. Momentum of a body is the quantity of motion it possesses due to its mass and velocity. The momentum P of a body is given by the product of its mass m and velocity v. Thus P = mv .......................... (3.1) Momentum is a vector quantity. Its SI unit is kgms⁻¹. 3.2 NEWTON'S LAWS OF MOTION Newton was the first to formulate the laws of motion known as Newton's laws of motion. NEWTON'S FIRST LAW OF MOTION First law of motion deals with bodies which are either at rest or moving with uniform speed in a straight line. According to Newton's first law of motion, a body at rest remains at rest provided no net force acts on it. This part of the law is true as we observe that objects do not move by themselves unless someone moves them. For example, a book lying on a table remains at rest as long as no net force acts on it. Similarly, a moving object does not stop moving by itself. A ball rolled on a rough ground stops earlier than that rolled on a smooth ground. It is because rough surfaces offer greater friction. If there would be no force to oppose the motion of a body then the moving body would never stop. Thus Newton's first law of motion states that: A body continues its state of rest or of uniform motion in a straight line provided no net force acts on it. Physics IX 60 Unit 3: Dynamics Since Newton's first law of motion deals with the inertial property of matter, therefore, Newton's first law of motion is also known as law of inertia. We have observed that the passengers standing in a bus fall forward when its driver applies brakes suddenly. It is because the upper parts of their bodies tend to continue their motion, while lower parts of their bodies in contact with the bus stop with it. Hence, they fall forward. NEWTON'S SECOND LAW OF MOTION Newton's second law of motion deals with situations when a net force is acting on a body. It states that: When a net force acts on a body, it produces acceleration in the body in the direction of the net force. The magnitude of this acceleration is directly proportional to the net force acting on the body and inversely proportional to its mass. If a force produces an acceleration a in a body of mass m, then we can state mathematically that ( a \propto F ) and ( a \propto \frac{1}{m} ) or ( a \propto \frac{F}{m} ) or ( F \propto ma ) Putting k as proportionality constant, we get ( F = kma ) … … … (3.2) In SI units, the value of k comes out to be 1.This concept can be seen the video.3.1. Thus Eq. 3.2 becomes"
embeddings = generate_embedding([input_text])
print(embeddings)
