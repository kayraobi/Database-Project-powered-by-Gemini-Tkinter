import google.generativeai as genai
from DoctorStore import *
from PatientStore import *
from AppointmentStore import *

genai.configure(api_key="NO NO NO NO I CANT LEAK IT")
model = genai.GenerativeModel("gemini-1.5-flash")





class Gemini():
     
     def __init__(self,problem):
         response = model.generate_content(problem)
         print(response.text)








