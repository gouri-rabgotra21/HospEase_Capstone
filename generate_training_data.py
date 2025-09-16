import pandas as pd
import random

# Define possible intents and a variety of phrases for each in English, Hindi, and Punjabi
data = {
    'greeting': [
        "hi", "hello", "hey", "good morning", "good evening", "how are you", "namaste", "sat sri akal",
        "नमस्ते", "नमस्कार", "सत श्री अकाल", "क्या हाल है?", "आप कैसे हैं?",
        "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ", "ਨਮਸਤੇ", "ਹੈਲੋ", "ਤੁਹਾਡਾ ਕੀ ਹਾਲ ਹੈ?", "ਕਿਵੇਂ ਹੋ?"
    ],
    'services_query': [
        "what services do you offer?", "what departments do you have?", "what specialities are available?", 
        "i need a doctor for my heart", "can you tell me about your doctors?", "what are your medical services?",
        "आप क्या सेवाएं देते हैं?", "आपके पास कौन से विभाग हैं?", "आपके डॉक्टर कौन हैं?", "क्या सेवाएं उपलब्ध हैं?",
        "ਤੁਸੀਂ ਕਿਹੜੀਆਂ ਸੇਵਾਵਾਂ ਪੇਸ਼ ਕਰਦੇ ਹੋ?", "ਤੁਹਾਡੇ ਕੋਲ ਕਿਹੜੇ ਵਿਭਾਗ ਹਨ?", "ਕਿਹੜੀਆਂ ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ ਉਪਲਬਧ ਹਨ?",
        "ਤੁਹਾਡੇ ਡਾਕਟਰਾਂ ਬਾਰੇ ਦੱਸੋ?"
    ],
    'location_query': [
        "where are you located?", "what is your address?", "how do I get there?", "directions to the hospital",
        "can you show me on a map?", "tell me about your location",
        "आप कहाँ स्थित हैं?", "आपका पता क्या है?", "मैं वहां कैसे पहुंच सकता हूं?", "अस्पताल का रास्ता",
        "ਤੁਸੀਂ ਕਿੱਥੇ ਸਥਿਤ ਹੋ?", "ਤੁਹਾਡਾ ਪਤਾ ਕੀ ਹੈ?", "ਮੈਂ ਉੱਥੇ ਕਿਵੇਂ ਪਹੁੰਚ ਸਕਦਾ ਹਾਂ?", "ਹਸਪਤਾਲ ਦਾ ਰਸਤਾ"
    ],
    'timings_query': [
        "what are your timings?", "when are you open?", "what are the OPD hours?", "are you open on weekends?",
        "what time do you close?", "what are your office hours?",
        "आपकी समय सारिणी क्या है?", "आप कब खुले होते हैं?", "ओपीडी का समय क्या है?", "ਕੀ ਤੁਸੀਂ ਵੀਕਐਂਡ 'ਤੇ ਖੁੱਲ੍ਹੇ ਹੁੰਦੇ ਹੋ?",
        "ਤੁਹਾਡੇ ਖੁੱਲ੍ਹਣ ਦਾ ਸਮਾਂ ਕੀ ਹੈ?", "ਓਪੀਡੀ ਦਾ ਸਮਾਂ ਕੀ ਹੈ?"
    ],
    'contact_query': [
        "how can I contact you?", "what is your phone number?", "can I book an appointment?", "what's your email?",
        "how to schedule an appointment?", "how do I make an appointment?",
        "मैं आपसे कैसे संपर्क कर सकता हूं?", "आपका फोन नंबर क्या है?", "क्या मैं अपॉइंटमेंट बुक कर सकता हूं?",
        "ਤੁਸੀਂ ਮੈਨੂੰ ਕਿਵੇਂ ਮਿਲ ਸਕਦੇ ਹੋ?", "ਤੁਹਾਡਾ ਫੋਨ ਨੰਬਰ ਕੀ ਹੈ?", "ਮੈਂ ਅਪੁਆਇੰਟਮੈਂਟ ਕਿਵੇਂ ਲੈ ਸਕਦਾ ਹਾਂ?"
    ],
    'insurance_query': [
        "do you accept insurance?", "what insurance do you take?", "do you have a billing department?",
        "is my insurance plan covered?", "can you tell me about health coverage?",
        "क्या आप बीमा स्वीकार करते हैं?", "आप कौन सा बीमा लेते हैं?", "क्या मेरा बीमा योजना कवर है?",
        "ਕੀ ਤੁਸੀਂ ਬੀਮਾ ਸਵੀਕਾਰ ਕਰਦੇ ਹੋ?", "ਤੁਸੀਂ ਕਿਹੜਾ ਬੀਮਾ ਲੈਂਦੇ ਹੋ?", "ਕੀ ਮੇਰਾ ਬੀਮਾ ਪਲਾਨ ਕਵਰ ਹੈ?"
    ],
    'emergency_query': [
        "i have an emergency", "i need immediate help", "is this an emergency number?", 
        "i need to go to the emergency room", "what do i do in an emergency?",
        "मुझे एक आपातकाल है", "मुझे तुरंत मदद चाहिए", "क्या यह आपातकालीन नंबर है?",
        "ਮੈਨੂੰ ਐਮਰਜੈਂਸੀ ਹੈ", "ਮੈਨੂੰ ਤੁਰੰਤ ਮਦਦ ਚਾਹੀਦੀ ਹੈ", "ਕੀ ਇਹ ਐਮਰਜੈਂਸੀ ਨੰਬਰ ਹੈ?"
    ]
}

# Create a list to store all labeled data
labeled_data = []
for intent, phrases in data.items():
    for phrase in phrases:
        labeled_data.append({'phrase': phrase, 'intent': intent})

# Create a DataFrame and save it as a CSV file
df = pd.DataFrame(labeled_data)
df.to_csv('chatbot_training_data.csv', index=False, encoding='utf-8')
print("Multilingual chatbot training data generated and saved to 'chatbot_training_data.csv'")