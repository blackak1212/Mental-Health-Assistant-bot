import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Comprehensive A to Z rule-based responses in English and Hindi
responses = {
    # English responses (A-Z)
    "angry": "It's normal to feel angry sometimes. Try to identify what's triggering this emotion.",
    "anxious": "Anxiety can be challenging. Have you tried any breathing exercises? Taking slow, deep breaths can sometimes help.",
    "afraid": "Fear is a natural response. Remember that you're not alone in feeling this way.",
    "bored": "Boredom can sometimes mask deeper feelings. Is there something you've been wanting to try or learn?",
    "bye": "Take care of yourself! Remember, it's okay to seek help when needed.",
    "confused": "It's okay to feel confused. Taking things one step at a time can help bring clarity.",
    "calm": "That's wonderful! What helps you maintain this sense of calm?",
    "depressed": "Depression can be overwhelming. Have you considered speaking with a mental health professional?",
    "disappointed": "Disappointment is difficult. Remember that setbacks are often temporary.",
    "excited": "Your excitement is contagious! What are you looking forward to?",
    "exhausted": "Being exhausted can affect your mental well-being. Are you giving yourself enough time to rest?",
    "frustrated": "Frustration is common. Sometimes taking a step back can provide a new perspective.",
    "fearful": "Fear is a natural emotion. What specifically are you fearful about?",
    "grateful": "Gratitude is powerful. What are some things you're grateful for today?",
    "guilty": "Guilt can be a heavy burden. Remember that making mistakes is part of being human.",
    "happy": "That's wonderful to hear! What's bringing you joy today?",
    "hello": "Hello! How are you feeling today?",
    "hi": "Hi there! How can I help you today?",
    "hopeful": "Hope is so important. What are you hopeful about?",
    "hopeless": "Feeling hopeless can be very difficult. Remember that circumstances can change.",
    "how are you": "I'm here to help you. More importantly, how are you feeling?",
    "hurt": "I'm sorry you're feeling hurt. Would you like to talk about what happened?",
    "irritated": "It's normal to feel irritated sometimes. What's bothering you?",
    "inspired": "That's great! What inspired you?",
    "jealous": "Jealousy is a common emotion. Try to focus on your own journey and achievements.",
    "joyful": "Joy is wonderful! What's bringing you joy right now?",
    "lonely": "Feeling lonely is a common human experience. Have you considered reaching out to a friend or family member?",
    "lost": "Feeling lost can be disorienting. Sometimes it helps to focus on small, achievable goals.",
    "motivated": "That's great! What's motivating you right now?",
    "nervous": "Feeling nervous is natural. Deep breathing can sometimes help calm your nerves.",
    "nostalgic": "Nostalgia can bring both joy and sadness. What are you reminiscing about?",
    "overwhelmed": "Feeling overwhelmed is common. Breaking tasks into smaller steps might help.",
    "optimistic": "That's a great mindset! What's making you feel optimistic?",
    "peaceful": "Peace of mind is valuable. What helps you find this peace?",
    "proud": "That's wonderful! What achievement are you proud of?",
    "puzzled": "It's okay to feel puzzled. Would talking through the situation help?",
    "quiet": "Sometimes we all need quiet moments. How are you using this time?",
    "relaxed": "That's great! What helps you relax?",
    "restless": "Restlessness can be uncomfortable. Have you tried any physical activity to release some energy?",
    "sad": "I'm sorry to hear you're feeling sad. Remember that it's okay to feel this way sometimes. Would you like to talk about what's making you feel this way?",
    "scared": "It's okay to feel scared. Would you like to talk about what's frightening you?",
    "stressed": "Stress affects us all. Consider taking short breaks throughout your day to reset your mind.",
    "surprised": "Surprises can be both good and challenging. What surprised you?",
    "thankful": "Gratitude is a powerful emotion. What are you thankful for?",
    "thank you": "You're welcome! I'm glad I could help.",
    "thanks": "You're welcome! Is there anything else you'd like to talk about?",
    "tired": "Being tired can affect our mental state. Are you getting enough rest?",
    "uncertain": "Uncertainty can be difficult. Sometimes focusing on what you can control helps.",
    "upset": "I understand that you're upset. Would you like to talk about what happened?",
    "valued": "Feeling valued is important. What made you feel this way?",
    "vulnerable": "Vulnerability takes courage. Thank you for sharing how you feel.",
    "worried": "Worry is common. Sometimes writing down your concerns can help put them in perspective.",
    "worthless": "I'm sorry you're feeling this way. Please know that you have value and worth.",
    "excited": "Excitement is wonderful! What are you excited about?",
    "yearning": "It's natural to yearn for something. What are you longing for?",
    "zealous": "Your enthusiasm is admirable! What are you passionate about?",
    "help": "I'm here to listen and provide support. What's on your mind?",
    
    # Hindi responses (A-Z equivalent)
    "akela": "अकेलापन एक सामान्य मानवीय अनुभव है। क्या आपने किसी दोस्त या परिवार के सदस्य से संपर्क करने पर विचार किया है?",
    "aasha": "आशा बहुत महत्वपूर्ण है। आप किस बारे में आशावान हैं?",
    "anand": "आनंद अद्भुत है! आपको इस समय क्या आनंद दे रहा है?",
    "bhay": "डर एक प्राकृतिक प्रतिक्रिया है। याद रखें कि आप इस तरह महसूस करने में अकेले नहीं हैं।",
    "bechani": "बेचैनी असहज हो सकती है। क्या आपने कुछ ऊर्जा निकालने के लिए कोई शारीरिक गतिविधि आज़माई है?",
    "chinta": "चिंता चुनौतीपूर्ण हो सकती है। क्या आपने कोई श्वास व्यायाम आज़माया है? धीमी, गहरी सांस लेने से कभी-कभी मदद मिल सकती है।",
    "dar": "डर महसूस करना ठीक है। क्या आप बात करना चाहेंगे कि आपको क्या डरा रहा है?",
    "dukhi": "मुझे सुनकर दुख हुआ कि आप दुखी महसूस कर रहे हैं। याद रखें कि कभी-कभी ऐसा महसूस करना ठीक है। क्या आप बताना चाहेंगे कि आप ऐसा क्यों महसूस कर रहे हैं?",
    "dhanyavad": "आपका स्वागत है! मुझे खुशी है कि मैं मदद कर सका।",
    "gussa": "कभी-कभी गुस्सा महसूस करना सामान्य है। इस भावना को ट्रिगर करने वाली चीज की पहचान करने का प्रयास करें।",
    "ghabraya": "घबराहट महसूस करना स्वाभाविक है। गहरी सांस लेने से कभी-कभी आपके तनाव को शांत करने में मदद मिल सकती है।",
    "hairani": "हैरानी अच्छी और चुनौतीपूर्ण दोनों हो सकती है। आपको किस बात ने हैरान किया?",
    "himmat": "हिम्मत रखना बहुत अच्छी बात है। आपको क्या प्रेरित कर रहा है?",
    "irkha": "ईर्ष्या एक सामान्य भावना है। अपनी खुद की यात्रा और उपलब्धियों पर ध्यान केंद्रित करने का प्रयास करें।",
    "josh": "उत्साह अद्भुत है! आप किस बारे में उत्साहित हैं?",
    "khush": "यह सुनकर बहुत अच्छा लगा! आज आपको क्या खुशी दे रहा है?",
    "kaise ho": "मैं आपकी मदद करने के लिए यहां हूं। अधिक महत्वपूर्ण बात यह है कि आप कैसा महसूस कर रहे हैं?",
    "kaise hai": "मैं आपकी मदद करने के लिए यहां हूं। अधिक महत्वपूर्ण बात यह है कि आप कैसा महसूस कर रहे हैं?",
    "lalach": "लालच एक सामान्य भावना है। अपने पास जो है उसके लिए आभारी होने का प्रयास करें।",
    "madad": "मैं सुनने और समर्थन प्रदान करने के लिए यहां हूं। आपके मन में क्या है?",
    "mayus": "निराशा मुश्किल होती है। याद रखें कि झटके अक्सर अस्थायी होते हैं।",
    "namaste": "नमस्ते! आज आप कैसा महसूस कर रहे हैं?",
    "nirash": "निराश महसूस करना बहुत कठिन हो सकता है। याद रखें कि परिस्थितियां बदल सकती हैं।",
    "pareshan": "परेशानी आम है। कभी-कभी एक कदम पीछे हटने से एक नया दृष्टिकोण मिल सकता है।",
    "prabhavit": "प्रभावित होना अच्छा है! आपको किसने प्रभावित किया?",
    "prerit": "यह बहुत अच्छा है! आपको क्या प्रेरित कर रहा है?",
    "prasann": "प्रसन्नता अद्भुत है! आपको इस समय क्या प्रसन्नता दे रहा है?",
    "roshni": "आशा की किरण महत्वपूर्ण है। आप किस बारे में आशावान हैं?",
    "shant": "शांति का अनुभव मूल्यवान है। आपको यह शांति कैसे मिलती है?",
    "shukriya": "आपका स्वागत है! क्या कुछ और है जिसके बारे में आप बात करना चाहेंगे?",
    "tension": "तनाव हम सभी को प्रभावित करता है। अपने दिन के दौरान अपने दिमाग को रीसेट करने के लिए छोटे ब्रेक लेने पर विचार करें।",
    "thaka": "थकान हमारी मानसिक स्थिति को प्रभावित कर सकती है। क्या आप पर्याप्त आराम कर रहे हैं?",
    "udas": "मुझे सुनकर दुख हुआ कि आप उदास महसूस कर रहे हैं। क्या आप बताना चाहेंगे कि आप ऐसा क्यों महसूस कर रहे हैं?",
    "utsah": "उत्साह अद्भुत है! आप किस बारे में उत्साहित हैं?",
    "vishwas": "आत्मविश्वास महत्वपूर्ण है। आपको क्या आत्मविश्वास दे रहा है?",
    "vyakul": "व्याकुलता असहज हो सकती है। क्या आपने कुछ ऊर्जा निकालने के लिए कोई शारीरिक गतिविधि आज़माई है?",
    "vyast": "व्यस्तता अच्छी हो सकती है। आप किस चीज़ में व्यस्त हैं?",
    "yad": "यादें खुशी और दुख दोनों ला सकती हैं। आप किस बारे में याद कर रहे हैं?",
    "yogya": "योग्यता महसूस करना महत्वपूर्ण है। आपको क्या योग्य महसूस करा रहा है?",
    "zinda": "जीवंत महसूस करना अद्भुत है! आपको क्या ऊर्जा दे रहा है?",
    "bhai": "क्या हुआ? बताओ, क्या मदद कर सकता हूँ?",
    "app dost ho": "क्या बात है! ऐसे दोस्त मिलना मुश्किल है।",
    "load hai": "समझ सकता हूँ! ऑफिस का काम तो कभी खत्म नहीं होता!",
    "sanjay": "मम्मी कैसी है?",
    "akash":"मम्मी कैसी है?",
    "vibhanshu": "मम्मी कैसी है?",
    "sex": "यार मुझे समझ नहीं आ रहा कि क्या करूँ।",
    "randi": "यार मुझे समझ नहीं आ रहा कि क्या करूँ।",
    "sad hun": "मैं चाहता हूँ कि हम मिलकर इसे हल करें और दोनों एक दूसरे को समझें।",
    "tumhe kuch nahi aata": "ठीक है, चलो इसे फिर से देखते हैं और किसी रास्ते पर पहुँचते हैं।",
    "tumhe kuch nahi pata": "ठीक है, चलो इसे फिर से देखते हैं और किसी रास्ते पर पहुँचते हैं।",
    "birthday": "मुझे उम्मीद है कि अगली बार हम मिलकर जिम्मेदारी साझा करेंगे।",
    "byby": "धन्यवाद! मैं सिर्फ चाहता था कि मुझे सुना जाए और समझा जाए।",
    "chal ta hun": "मुझे उम्मीद है कि अगली बार हम चीजों को साफ और स्पष्ट रखें।",
    "alvida": "अपना ख्याल रखें! याद रखें, जरूरत पड़ने पर मदद मांगना ठीक है।",
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/bot', methods=['POST'])
def bot_response():
    user_message = request.json.get('message', '').lower()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Check if we have a direct match in our responses
        for key, response in responses.items():
            if key in user_message:
                return jsonify({'response': response})
        
        # Default response if no match is found
        return jsonify({
            'response': "I'm here to listen. Could you tell me more about how you're feeling? (मैं सुनने के लिए यहां हूं। क्या आप मुझे बता सकते हैं कि आप कैसा महसूस कर रहे हैं?)"
        })

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)