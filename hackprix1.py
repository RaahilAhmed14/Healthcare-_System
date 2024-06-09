import customtkinter as ctk
from tkinter import messagebox
from tkinter.font import Font

# Extended dictionary of common diseases and their corresponding symptoms
disease_symptoms = {
    "Common Cold": ["cough", "sneezing", "runny nose", "sore throat"],
    "Flu": ["fever", "chills", "body aches", "fatigue", "cough"],
    "COVID-19": ["fever", "dry cough", "tiredness", "loss of taste or smell"],
    "Strep Throat": ["sore throat", "painful swallowing", "fever", "swollen lymph nodes"],
    "Allergies": ["sneezing", "itchy eyes", "runny nose", "congestion"],
    "Asthma": ["shortness of breath", "wheezing", "coughing", "chest tightness"],
    "Bronchitis": ["cough", "mucus production", "fatigue", "shortness of breath"],
    "Pneumonia": ["fever", "cough", "shortness of breath", "chest pain"],
    "Sinusitis": ["facial pain", "nasal congestion", "headache", "runny nose"],
    "Migraine": ["headache", "nausea", "sensitivity to light", "sensitivity to sound"],
    "Diabetes": ["increased thirst", "frequent urination", "extreme hunger", "fatigue"],
    "Hypertension": ["headache", "shortness of breath", "nosebleeds", "flushing"],
    "Heart Attack": ["chest pain", "shortness of breath", "nausea", "lightheadedness"],
    "Stroke": ["sudden numbness", "confusion", "trouble speaking", "trouble walking"],
    "Chickenpox": ["itchy rash", "fever", "tiredness", "loss of appetite"],
    "Measles": ["fever", "cough", "runny nose", "rash"],
    "Mumps": ["swollen glands", "fever", "headache", "muscle aches"],
    "Malaria": ["fever", "chills", "sweating", "headache"],
    "Tuberculosis": ["persistent cough", "weight loss", "night sweats", "fever"],
    "Hepatitis": ["jaundice", "fatigue", "abdominal pain", "nausea"],
    "Lyme Disease": ["rash", "fever", "chills", "fatigue"],
    "Mononucleosis": ["fatigue", "sore throat", "fever", "swollen lymph nodes"],
    "Anemia": ["fatigue", "pale skin", "shortness of breath", "dizziness"],
    "Hypothyroidism": ["fatigue", "weight gain", "cold intolerance", "dry skin"],
    "Hyperthyroidism": ["weight loss", "rapid heartbeat", "sweating", "irritability"],
    "Rheumatoid Arthritis": ["joint pain", "stiffness", "swelling", "fatigue"],
    "Lupus": ["fatigue", "joint pain", "rash", "fever"],
    "Celiac Disease": ["diarrhea", "bloating", "weight loss", "fatigue"],
    "Irritable Bowel Syndrome (IBS)": ["abdominal pain", "bloating", "diarrhea", "constipation"],
    "Crohn's Disease": ["diarrhea", "abdominal pain", "weight loss", "fatigue"],
    "Peptic Ulcer": ["burning stomach pain", "bloating", "heartburn", "nausea"],
    "Gallstones": ["abdominal pain", "nausea", "vomiting", "jaundice"],
    "Kidney Stones": ["severe pain", "nausea", "vomiting", "blood in urine"],
    "Urinary Tract Infection (UTI)": ["painful urination", "frequent urination", "cloudy urine", "pelvic pain"],
    "Gonorrhea": ["painful urination", "abnormal discharge", "testicular pain", "pelvic pain"],
    "Chlamydia": ["abnormal discharge", "painful urination", "pelvic pain", "testicular pain"],
    "Syphilis": ["painless sore", "rash", "fever", "swollen lymph nodes"],
    "HIV/AIDS": ["fever", "night sweats", "weight loss", "fatigue"],
    "Herpes": ["painful sores", "itching", "fever", "swollen lymph nodes"],
    "Hepatitis B": ["jaundice", "dark urine", "nausea", "vomiting", "abdominal pain"],
    "Hepatitis C": ["fatigue", "joint pain", "fever", "nausea", "abdominal pain"],
    "Ebola": ["fever", "severe headache", "muscle pain", "weakness", "fatigue", "diarrhea", "vomiting", "abdominal pain"],
    "Dengue": ["high fever", "severe headache", "pain behind the eyes", "joint pain", "muscle pain", "rash", "nausea", "vomiting"],
    "Zika Virus": ["fever", "rash", "joint pain", "red eyes", "muscle pain", "headache"],
}

def diagnose(symptoms, disease_symptoms):
    """
    Function to diagnose possible diseases based on input symptoms.
    Returns a sorted list of possible diseases and their match counts.
    """
    possible_diseases = {}
    
    for disease, symptoms_list in disease_symptoms.items():
        match_count = len(set(symptoms).intersection(symptoms_list))
        if match_count > 0:
            possible_diseases[disease] = match_count
    
    if possible_diseases:
        # Sort diseases by the number of matching symptoms
        sorted_diseases = sorted(possible_diseases.items(), key=lambda item: item[1], reverse=True)
        return sorted_diseases
    else:
        return "No matching disease found."

# Create a class for the GUI application
class DiseaseDiagnosisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Disease Diagnosis")
        self.geometry("500x400")

        # Create and place the label, entry, and button widgets
        self.instruction_label = ctk.CTkLabel(self, text="Enter at least 3 symptoms separated by commas:")
        self.instruction_label.pack(pady=20)

        self.symptoms_label = ctk.CTkLabel(self, text="Symptoms:")
        self.symptoms_label.pack()

        self.symptoms_entry = ctk.CTkEntry(self, width=400)
        self.symptoms_entry.pack(pady=10)

        self.diagnose_button = ctk.CTkButton(self, text="Diagnose", command=self.diagnose)
        self.diagnose_button.pack(pady=20)

        self.result_text = ctk.CTkTextbox(self, width=400, height=200)
        self.result_text.pack(pady=10)

    def diagnose(self):
        user_symptoms = self.symptoms_entry.get().split(",")
        user_symptoms = [symptom.strip().lower() for symptom in user_symptoms]

        if len(user_symptoms) < 3:
            messagebox.showerror("Input Error", "Please enter at least 3 symptoms.")
            return

        diagnosis = diagnose(user_symptoms, disease_symptoms)
        
        if isinstance(diagnosis, str):
            result = diagnosis
        else:
            result = "Possible diseases based on symptoms:\n"
            max_matches = diagnosis[0][1]
            for disease, matches in diagnosis:
                if matches == max_matches:
                    result += f"**{disease}: {matches} matching symptoms**\n"
                else:
                    result += f"{disease}: {matches} matching symptoms\n"
        
        self.result_text.delete(1.0, ctk.END)
        self.result_text.insert(ctk.END, result)

# Run the application
    def don():
        app = DiseaseDiagnosisApp()
        app.mainloop()
if __name__ == "__main__":
    DiseaseDiagnosisApp.don()
