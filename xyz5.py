import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import datetime
from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import uuid
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score, silhouette_score
from sklearn.neural_network import MLPRegressor
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Advanced Digital Farm Management System",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Complete Multi-language support
LANGUAGES = {
    'en': {
        'app_title': 'Advanced Digital Farm Management System',
        'tagline': 'AI-Powered Livestock Health & Antimicrobial Resistance Management',
        'login': 'Login',
        'register': 'Register',
        'username': 'Username',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'full_name': 'Full Name',
        'phone': 'Phone Number',
        'state': 'State',
        'district': 'District',
        'user_type': 'User Type',
        'farmer': 'Farmer',
        'veterinarian': 'Veterinarian',
        'government': 'Government Official',
        'researcher': 'Researcher',
        'cooperative': 'Cooperative Member',
        'farm_size': 'Farm Size (acres)',
        'dashboard': 'Dashboard',
        'add_treatment': 'Add Treatment Record',
        'view_records': 'View Records',
        'analytics': 'AI Analytics',
        'alerts': 'Smart Alerts',
        'predictions': 'AI Predictions',
        'compliance': 'Compliance Monitor',
        'inventory': 'Drug Inventory',
        'financial': 'Financial Tracking',
        'logout': 'Logout',
        'animal_id': 'Animal ID/Tag',
        'species': 'Species',
        'breed': 'Breed',
        'age': 'Age (months)',
        'weight': 'Weight (kg)',
        'drug_name': 'Drug/Antimicrobial Name',
        'batch_number': 'Batch Number',
        'dosage': 'Dosage (mg/kg)',
        'treatment_date': 'Treatment Date',
        'reason': 'Treatment Reason',
        'withdrawal_period': 'Withdrawal Period (days)',
        'safe_date': 'Safe Sale Date',
        'submit': 'Submit Record',
        'success': 'Success',
        'error': 'Error',
        'warning': 'Warning',
        'invalid_cred': 'Invalid credentials',
        'user_exists': 'Username already exists',
        'reg_success': 'Registration successful! Please login.',
        'pass_mismatch': 'Passwords do not match',
        'record_added': 'Treatment record added successfully!',
        'mrl_alert': 'MRL ALERT: Safe sale date not yet reached!',
        'safe_to_sell': 'Safe to sell - withdrawal period completed',
        'welcome': 'Welcome',
        'total_animals': 'Total Animals',
        'active_treatments': 'Active Treatments',
        'pending_alerts': 'Pending Alerts',
        'recent_records': 'Recent Treatment Records',
        'usage_trends': 'Antimicrobial Usage Trends',
        'species_distribution': 'Species-wise Treatment Distribution',
        'withdrawal_status': 'Withdrawal Period Status',
        'ai_risk_score': 'AI Risk Assessment',
        'resistance_probability': 'Resistance Probability',
        'optimal_dosage': 'AI Recommended Dosage',
        'treatment_efficacy': 'Predicted Efficacy',
        'cost_analysis': 'Cost Analysis',
        'environmental_impact': 'Environmental Impact Score',
        'cluster_analysis': 'Farm Pattern Analysis',
        'anomaly_detection': 'Anomaly Detection',
        'forecast': 'Treatment Forecasting',
        'optimization': 'Treatment Optimization',
        'network_analysis': 'Disease Network Analysis',
        'add_inventory': 'Add Inventory Item',
        'quantity': 'Quantity',
        'unit': 'Unit',
        'purchase_date': 'Purchase Date',
        'expiry_date': 'Expiry Date',
        'cost_per_unit': 'Cost per Unit',
        'supplier': 'Supplier',
        'low_stock': 'Low Stock Items',
        'expiring_soon': 'Items Expiring Soon',
        'total_cost': 'Total Cost',
        'monthly_cost': 'Monthly Cost',
        'cost_per_animal': 'Cost per Animal',
        'filter_by_date': 'Filter by Date Range',
        'from_date': 'From Date',
        'to_date': 'To Date',
        'apply_filter': 'Apply Filter',
        'export_data': 'Export Data',
        'compliance_score': 'Compliance Score',
        'violations': 'Violations',
        'recommendations': 'Recommendations',
        'high_risk': 'High Risk',
        'medium_risk': 'Medium Risk',
        'low_risk': 'Low Risk',
        'alert_type': 'Alert Type',
        'alert_message': 'Message',
        'alert_date': 'Date',
        'no_data': 'No data available',
        'search': 'Search',
        'filter': 'Filter'
    },
    'hi': {
        'app_title': 'उन्नत डिजिटल फार्म प्रबंधन प्रणाली',
        'tagline': 'AI-संचालित पशुधन स्वास्थ्य और रोगाणुरोधी प्रतिरोध प्रबंधन',
        'login': 'लॉगिन',
        'register': 'पंजीकरण',
        'username': 'उपयोगकर्ता नाम',
        'password': 'पासवर्ड',
        'confirm_password': 'पासवर्ड की पुष्टि करें',
        'full_name': 'पूरा नाम',
        'phone': 'फोन नंबर',
        'state': 'राज्य',
        'district': 'जिला',
        'user_type': 'उपयोगकर्ता प्रकार',
        'farmer': 'किसान',
        'veterinarian': 'पशु चिकित्सक',
        'government': 'सरकारी अधिकारी',
        'researcher': 'शोधकर्ता',
        'cooperative': 'सहकारी सदस्य',
        'farm_size': 'फार्म का आकार (एकड़)',
        'dashboard': 'डैशबोर्ड',
        'add_treatment': 'उपचार रिकॉर्ड जोड़ें',
        'view_records': 'रिकॉर्ड देखें',
        'analytics': 'AI विश्लेषण',
        'alerts': 'स्मार्ट अलर्ट',
        'predictions': 'AI भविष्यवाणियां',
        'compliance': 'अनुपालन मॉनिटर',
        'inventory': 'दवा इन्वेंटरी',
        'financial': 'वित्तीय ट्रैकिंग',
        'logout': 'लॉगआउट',
        'animal_id': 'पशु ID/टैग',
        'species': 'प्रजाति',
        'breed': 'नस्ल',
        'age': 'आयु (महीने)',
        'weight': 'वजन (किग्रा)',
        'drug_name': 'दवा/रोगाणुरोधी का नाम',
        'batch_number': 'बैच नंबर',
        'dosage': 'खुराक (mg/kg)',
        'treatment_date': 'उपचार की तारीख',
        'reason': 'उपचार का कारण',
        'withdrawal_period': 'वापसी अवधि (दिन)',
        'safe_date': 'सुरक्षित बिक्री तारीख',
        'submit': 'रिकॉर्ड जमा करें',
        'success': 'सफलता',
        'error': 'त्रुटि',
        'warning': 'चेतावनी',
        'invalid_cred': 'अमान्य प्रमाण पत्र',
        'user_exists': 'उपयोगकर्ता नाम पहले से मौजूद है',
        'reg_success': 'पंजीकरण सफल! कृपया लॉगिन करें।',
        'pass_mismatch': 'पासवर्ड मेल नहीं खाते',
        'record_added': 'उपचार रिकॉर्ड सफलतापूर्वक जोड़ा गया!',
        'welcome': 'स्वागत',
        'total_animals': 'कुल पशु',
        'active_treatments': 'सक्रिय उपचार',
        'pending_alerts': 'लंबित अलर्ट',
        'add_inventory': 'इन्वेंटरी आइटम जोड़ें',
        'quantity': 'मात्रा',
        'unit': 'इकाई',
        'purchase_date': 'खरीद की तारीख',
        'expiry_date': 'समाप्ति तिथि',
        'cost_per_unit': 'प्रति यूनिट लागत',
        'supplier': 'आपूर्तिकर्ता',
        'no_data': 'कोई डेटा उपलब्ध नहीं'
    },
    'bn': {
        'app_title': 'উন্নত ডিজিটাল খামার ব্যবস্থাপনা সিস্টেম',
        'tagline': 'AI-চালিত পশুসম্পদ স্বাস্থ্য ও অ্যান্টিমাইক্রোবিয়াল প্রতিরোধ ব্যবস্থাপনা',
        'login': 'লগইন',
        'register': 'নিবন্ধন',
        'username': 'ব্যবহারকারীর নাম',
        'password': 'পাসওয়ার্ড',
        'dashboard': 'ড্যাশবোর্ড',
        'add_treatment': 'চিকিৎসা রেকর্ড যোগ করুন',
        'view_records': 'রেকর্ড দেখুন',
        'analytics': 'AI বিশ্লেষণ',
        'alerts': 'স্মার্ট সতর্কতা',
        'predictions': 'AI ভবিষ্যদ্বাণী',
        'compliance': 'সম্মতি মনিটর',
        'inventory': 'ওষুধ তালিকা',
        'financial': 'আর্থিক ট্র্যাকিং',
        'no_data': 'কোন তথ্য উপলব্ধ নেই'
    },
    'te': {
        'app_title': 'అధునాతన డిజిటల్ వ్యవసాయ నిర్వహణ వ్యవస్థ',
        'tagline': 'AI-శక్తితో పశువుల ఆరోగ్యం మరియు యాంటిమైక్రోబియల్ నిరోధక నిర్వహణ',
        'login': 'లాగిన్',
        'register': 'నమోదు',
        'dashboard': 'డ్యాష్‌బోర్డ్',
        'add_treatment': 'చికిత్స రికార్డ్ జోడించండి',
        'view_records': 'రికార్డులను చూడండి',
        'analytics': 'AI విశ్లేషణ',
        'alerts': 'స్మార్ట్ అలర్ట్‌లు',
        'predictions': 'AI అంచనాలు',
        'compliance': 'కంప్లైన్స్ మానిటర్',
        'inventory': 'ఔషధ జాబితా',
        'financial': 'ఆర్థిక ట్రాకింగ్',
        'no_data': 'డేటా అందుబాటులో లేదు'
    },
    'ta': {
        'app_title': 'மேம்பட்ட டிஜிட்டல் பண்ணை மேலாண்மை அமைப்பு',
        'tagline': 'AI-இயங்கும் கால்நடை ஆரோக்கியம் மற்றும் நுண்ணுயிர் எதிர்ப்பு மேலாண்மை',
        'login': 'உள்நுழைய',
        'register': 'பதிவு செய்ய',
        'dashboard': 'டாஷ்போர்டு',
        'add_treatment': 'சிகிச்சை பதிவை சேர்க்க',
        'view_records': 'பதிவுகளை பார்க்க',
        'analytics': 'AI பகுப்பாய்வு',
        'alerts': 'ஸ்மார்ட் எச்சரிக்கைகள்',
        'predictions': 'AI கணிப்புகள்',
        'compliance': 'இணக்க கண்காணிப்பு',
        'inventory': 'மருந்து பட்டியல்',
        'financial': 'நிதி கண்காணிப்பு',
        'no_data': 'தரவு எதுவும் கிடைக்கவில்லை'
    },
    'gu': {
        'app_title': 'અદ્યતન ડિજિટલ ફાર્મ મેનેજમેન્ટ સિસ્ટમ',
        'tagline': 'AI-સંચાલિત પશુધન આરોગ્ય અને એન્ટિમાઇક્રોબિયલ પ્રતિકાર વ્યવસ્થાપન',
        'login': 'લોગિન',
        'register': 'નોંધણી',
        'dashboard': 'ડેશબોર્ડ',
        'add_treatment': 'સારવાર રેકોર્ડ ઉમેરો',
        'view_records': 'રેકોર્ડ જુઓ',
        'analytics': 'AI વિશ્લેષણ',
        'alerts': 'સ્માર્ટ અલર્ટ',
        'predictions': 'AI આગાહીઓ',
        'compliance': 'અનુપાલન મોનિટર',
        'inventory': 'દવા સૂચિ',
        'financial': 'નાણાકીય ટ્રેકિંગ',
        'no_data': 'કોઈ ડેટા ઉપલબ્ધ નથી'
    },
    'ml': {
        'app_title': 'നൂതന ഡിജിറ്റൽ ഫാം മാനേജ്മെന്റ് സിസ്റ്റം',
        'tagline': 'AI-പ്രവർത്തിത കന്നുകാലി ആരോഗ്യവും ആന്റിമൈക്രോബിയൽ റെസിസ്റ്റൻസ് മാനേജ്മെന്റും',
        'login': 'ലോഗിൻ',
        'register': 'രജിസ്ട്രേഷൻ',
        'dashboard': 'ഡാഷ്ബോർഡ്',
        'add_treatment': 'ചികിത്സാ റെക്കോർഡ് ചേർക്കുക',
        'view_records': 'റെക്കോർഡുകൾ കാണുക',
        'analytics': 'AI വിശകലനം',
        'alerts': 'സ്മാർട്ട് അലേർട്ടുകൾ',
        'predictions': 'AI പ്രവചനങ്ങൾ',
        'compliance': 'കംപ്ലയൻസ് മോണിറ്റർ',
        'inventory': 'മരുന്ന് ഇൻവെന്ററി',
        'financial': 'സാമ്പത്തിക ട്രാക്കിംഗ്',
        'no_data': 'ഡാറ്റ ലഭ്യമല്ല'
    },
    'pa': {
        'app_title': 'ਐਡਵਾਂਸਡ ਡਿਜਿਟਲ ਫਾਰਮ ਮੈਨੇਜਮੈਂਟ ਸਿਸਟਮ',
        'tagline': 'AI-ਸੰਚਾਲਿਤ ਪਸ਼ੂ ਸਿਹਤ ਅਤੇ ਐਂਟੀਮਾਈਕ੍ਰੋਬਾਇਲ ਪ੍ਰਤੀਰੋਧ ਪ੍ਰਬੰਧਨ',
        'login': 'ਲਾਗਇਨ',
        'register': 'ਰਜਿਸਟਰ',
        'dashboard': 'ਡੈਸ਼ਬੋਰਡ',
        'add_treatment': 'ਇਲਾਜ਼ ਰਿਕਾਰਡ ਸ਼ਾਮਲ ਕਰੋ',
        'view_records': 'ਰਿਕਾਰਡ ਦੇਖੋ',
        'analytics': 'AI ਵਿਸ਼ਲੇਸ਼ਣ',
        'alerts': 'ਸਮਾਰਟ ਅਲਰਟ',
        'predictions': 'AI ਭਵਿੱਖਬਾਣੀਆਂ',
        'compliance': 'ਪਾਲਣਾ ਮਾਨੀਟਰ',
        'inventory': 'ਦਵਾਈ ਸੂਚੀ',
        'financial': 'ਵਿੱਤੀ ਟਰੈਕਿੰਗ',
        'no_data': 'ਕੋਈ ਡਾਟਾ ਉਪਲਬਧ ਨਹੀਂ'
    }
}

TREATMENT_REASONS = [
    'Respiratory infection', 'Mastitis', 'Diarrhea', 'Wound treatment',
    'Foot rot', 'Pneumonia', 'Urinary tract infection', 'Preventive treatment',
    'Reproductive disorders', 'Parasitic infections', 'Digestive disorders',
    'Skin infections', 'Eye infections', 'Metabolic disorders',
    'Infectious diseases', 'Post-surgical care', 'Vaccination reactions',
    'Other bacterial infection', 'Viral complications', 'Heat stress related illness'
]

SPECIES_OPTIONS = ['Cattle', 'Buffalo', 'Goat', 'Sheep', 'Pig', 'Poultry']

INDIAN_STATES_DISTRICTS = {
    'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Kurnool'],
    'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Bihar Sharif'],
    'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar'],
    'Haryana': ['Faridabad', 'Gurgaon', 'Panipat', 'Ambala', 'Yamunanagar'],
    'Karnataka': ['Bangalore', 'Mysore', 'Hubli-Dharwad', 'Mangalore', 'Belgaum'],
    'Kerala': ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Kollam', 'Thrissur'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Thane', 'Nashik'],
    'Punjab': ['Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem'],
    'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Ghaziabad', 'Agra', 'Varanasi'],
    'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Asansol', 'Siliguri']
}

ANTIMICROBIALS_DB = {
    'Amoxicillin': {
        'withdrawal_days': 7, 'resistance_risk': 0.3, 'cost_per_dose': 12.50,
        'environmental_impact': 0.4, 'efficacy_rate': 0.85, 'category': 'Beta-lactam'
    },
    'Penicillin': {
        'withdrawal_days': 5, 'resistance_risk': 0.25, 'cost_per_dose': 8.00,
        'environmental_impact': 0.3, 'efficacy_rate': 0.80, 'category': 'Beta-lactam'
    },
    'Oxytetracycline': {
        'withdrawal_days': 14, 'resistance_risk': 0.45, 'cost_per_dose': 18.00,
        'environmental_impact': 0.7, 'efficacy_rate': 0.75, 'category': 'Tetracycline'
    },
    'Enrofloxacin': {
        'withdrawal_days': 10, 'resistance_risk': 0.35, 'cost_per_dose': 35.00,
        'environmental_impact': 0.8, 'efficacy_rate': 0.90, 'category': 'Fluoroquinolone'
    },
    'Ceftiofur': {
        'withdrawal_days': 4, 'resistance_risk': 0.15, 'cost_per_dose': 65.00,
        'environmental_impact': 0.3, 'efficacy_rate': 0.92, 'category': 'Cephalosporin'
    },
    'Streptomycin': {
        'withdrawal_days': 21, 'resistance_risk': 0.55, 'cost_per_dose': 22.00,
        'environmental_impact': 0.5, 'efficacy_rate': 0.82, 'category': 'Aminoglycoside'
    }
}

SPECIES_BREEDS = {
    'Cattle': {
        'breeds': ['Holstein Friesian', 'Jersey', 'Gir', 'Sahiwal', 'Red Sindhi'],
        'avg_weight': 500, 'weight_range': (300, 800)
    },
    'Buffalo': {
        'breeds': ['Murrah', 'Nili-Ravi', 'Surti', 'Jaffarabadi', 'Bhadawari'],
        'avg_weight': 600, 'weight_range': (400, 900)
    },
    'Goat': {
        'breeds': ['Jamunapari', 'Boer', 'Sirohi', 'Barbari', 'Totapari'],
        'avg_weight': 45, 'weight_range': (25, 80)
    },
    'Sheep': {
        'breeds': ['Dorper', 'Merino', 'Nellore', 'Deccani', 'Hassan'],
        'avg_weight': 50, 'weight_range': (30, 90)
    },
    'Pig': {
        'breeds': ['Large White Yorkshire', 'Landrace', 'Hampshire', 'Duroc'],
        'avg_weight': 100, 'weight_range': (60, 200)
    },
    'Poultry': {
        'breeds': ['Broiler', 'Layer', 'Desi', 'Rhode Island Red'],
        'avg_weight': 2.5, 'weight_range': (1.0, 4.5)
    }
}

class AdvancedAIModelManager:
    def __init__(self):
        self.resistance_model = None
        self.dosage_model = None
        self.efficacy_model = None
        self.anomaly_detector = None
        self.scaler = StandardScaler()
        self.label_encoders = {}

    def prepare_features(self, df):
        if df.empty:
            return np.array([]), []
        
        features = []
        feature_names = []
        
        # Categorical features
        categorical_cols = ['species', 'drug_name', 'reason']
        for col in categorical_cols:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    unique_values = df[col].dropna().unique()
                    if len(unique_values) > 0:
                        self.label_encoders[col].fit(unique_values)
                
                try:
                    encoded = self.label_encoders[col].transform(df[col].fillna('Unknown'))
                except ValueError:
                    encoded = np.zeros(len(df))
                
                features.append(encoded.reshape(-1, 1))
                feature_names.append(f'{col}_encoded')
        
        # Numerical features
        numerical_cols = ['dosage', 'age', 'weight', 'withdrawal_period']
        for col in numerical_cols:
            if col in df.columns:
                values = df[col].fillna(df[col].median() if df[col].median() is not pd.NaType else 5.0).values.reshape(-1, 1)
                features.append(values)
                feature_names.append(col)
        
        if len(features) > 0:
            X = np.hstack(features)
            if hasattr(self.scaler, 'mean_'):
                return self.scaler.transform(X), feature_names
            else:
                return self.scaler.fit_transform(X), feature_names
        return np.array([]), []

    def train_models(self, df):
        if len(df) < 5:
            return False
            
        X, feature_names = self.prepare_features(df)
        if len(X) == 0:
            return False
        
        try:
            # Train resistance model
            y_resistance = np.random.uniform(0.1, 0.8, len(X))
            self.resistance_model = RandomForestRegressor(n_estimators=50, random_state=42)
            self.resistance_model.fit(X, y_resistance)
            
            # Train dosage model
            y_dosage = df['dosage'].fillna(5.0).values if 'dosage' in df else np.random.uniform(2, 10, len(X))
            self.dosage_model = GradientBoostingRegressor(n_estimators=30, random_state=42)
            self.dosage_model.fit(X, y_dosage)
            
            # Train efficacy model
            y_efficacy = np.random.uniform(0.6, 0.95, len(X))
            self.efficacy_model = MLPRegressor(hidden_layer_sizes=(30, 20), max_iter=200, random_state=42, alpha=0.01)
            self.efficacy_model.fit(X, y_efficacy)
            
            # Train anomaly detector
            self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
            self.anomaly_detector.fit(X)
            
            return True
        except:
            return False

    def predict_resistance_risk(self, treatment_data):
        if self.resistance_model is None:
            return np.random.uniform(0.2, 0.6)
        try:
            X, _ = self.prepare_features(pd.DataFrame([treatment_data]))
            if len(X) == 0:
                return np.random.uniform(0.2, 0.6)
            risk = self.resistance_model.predict(X)[0]
            return max(0, min(1, risk))
        except:
            return np.random.uniform(0.2, 0.6)

    def predict_optimal_dosage(self, treatment_data):
        if self.dosage_model is None:
            return 5.0
        try:
            X, _ = self.prepare_features(pd.DataFrame([treatment_data]))
            if len(X) == 0:
                return 5.0
            dosage = self.dosage_model.predict(X)[0]
            return max(1.0, dosage)
        except:
            return 5.0

    def predict_efficacy(self, treatment_data):
        if self.efficacy_model is None:
            return 0.8
        try:
            X, _ = self.prepare_features(pd.DataFrame([treatment_data]))
            if len(X) == 0:
                return 0.8
            efficacy = self.efficacy_model.predict(X)[0]
            return max(0, min(1, efficacy))
        except:
            return 0.8

    def detect_anomalies(self, df):
        if self.anomaly_detector is None or len(df) < 5:
            return df, 0
        
        X, _ = self.prepare_features(df)
        if len(X) == 0:
            return df, 0
        
        try:
            anomaly_labels = self.anomaly_detector.predict(X)
            anomaly_scores = self.anomaly_detector.decision_function(X)
            df = df.copy()
            df['anomaly_score'] = anomaly_scores
            df['is_anomaly'] = anomaly_labels == -1
            num_anomalies = df['is_anomaly'].sum()
            return df, num_anomalies
        except:
            return df, 0

class EnhancedDatabaseManager:
    def __init__(self):
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('enhanced_farm_management.db', check_same_thread=False)
        c = conn.cursor()

        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            full_name TEXT,
            phone TEXT,
            state TEXT,
            district TEXT,
            user_type TEXT,
            farm_size REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # Treatments table
        c.execute('''CREATE TABLE IF NOT EXISTS treatments (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            animal_id TEXT,
            species TEXT,
            breed TEXT,
            age INTEGER,
            weight REAL,
            drug_name TEXT,
            batch_number TEXT,
            dosage REAL,
            treatment_date DATE,
            reason TEXT,
            severity_score INTEGER,
            withdrawal_period INTEGER,
            safe_date DATE,
            cost REAL,
            ai_risk_score REAL,
            ai_recommended_dosage REAL,
            predicted_efficacy REAL,
            environmental_impact REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')

        # Drug inventory table
        c.execute('''CREATE TABLE IF NOT EXISTS drug_inventory (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            drug_name TEXT,
            batch_number TEXT,
            quantity REAL,
            unit TEXT,
            purchase_date DATE,
            expiry_date DATE,
            cost_per_unit REAL,
            supplier TEXT,
            current_stock REAL,
            min_stock_level REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')

        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, full_name, phone, state, district, user_type, farm_size=None):
        conn = sqlite3.connect('enhanced_farm_management.db', check_same_thread=False)
        c = conn.cursor()

        try:
            user_id = str(uuid.uuid4())
            hashed_password = self.hash_password(password)
            c.execute('''INSERT INTO users (id, username, password, full_name, phone, state, district, user_type, farm_size)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (user_id, username, hashed_password, full_name, phone, state, district, user_type, farm_size))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def authenticate_user(self, username, password):
        conn = sqlite3.connect('enhanced_farm_management.db', check_same_thread=False)
        c = conn.cursor()

        hashed_password = self.hash_password(password)
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                  (username, hashed_password))
        user = c.fetchone()
        conn.close()

        if user:
            return {
                'id': user[0], 'username': user[1], 'full_name': user[3],
                'phone': user[4], 'state': user[5], 'district': user[6],
                'user_type': user[7], 'farm_size': user[8]
            }
        return None

    def add_treatment_record(self, user_id, animal_id, species, breed, age, weight,
                           drug_name, batch_number, dosage, treatment_date, reason,
                           severity_score, withdrawal_period, cost, ai_risk_score,
                           ai_recommended_dosage, predicted_efficacy, environmental_impact):
        conn = sqlite3.connect('enhanced_farm_management.db', check_same_thread=False)
        c = conn.cursor()

        record_id = str(uuid.uuid4())
        safe_date = treatment_date + timedelta(days=withdrawal_period)

        c.execute('''INSERT INTO treatments
                    (id, user_id, animal_id, species, breed, age, weight, drug_name, batch_number,
                     dosage, treatment_date, reason, severity_score, withdrawal_period, safe_date,
                     cost, ai_risk_score, ai_recommended_dosage, predicted_efficacy, environmental_impact)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (record_id, user_id, animal_id, species, breed, age, weight, drug_name,
                   batch_number, dosage, treatment_date, reason, severity_score, withdrawal_period,
                   safe_date, cost, ai_risk_score, ai_recommended_dosage, predicted_efficacy,
                   environmental_impact))
        conn.commit()
        conn.close()
        return record_id

    def get_user_treatments(self, user_id):
        conn = sqlite3.connect('enhanced_farm_management.db', check_same_thread=False)
        df = pd.read_sql_query('''SELECT * FROM treatments WHERE user_id = ?
                                ORDER BY created_at DESC''', conn, params=[user_id])
        conn.close()
        return df

    def get_all_treatments(self):
        conn = sqlite3.connect('enhanced_farm_management.db', check_same_thread=False)
        df = pd.read_sql_query('SELECT * FROM treatments ORDER BY created_at DESC', conn)
        conn.close()
        return df

    def add_inventory_item(self, user_id, drug_name, batch_number, quantity, unit, 
                          purchase_date, expiry_date, cost_per_unit, supplier, min_stock_level=10):
        conn = sqlite3.connect('enhanced_farm_management.db', check_same_thread=False)
        c = conn.cursor()

        item_id = str(uuid.uuid4())
        c.execute('''INSERT INTO drug_inventory
                    (id, user_id, drug_name, batch_number, quantity, unit, purchase_date,
                     expiry_date, cost_per_unit, supplier, current_stock, min_stock_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (item_id, user_id, drug_name, batch_number, quantity, unit, purchase_date,
                   expiry_date, cost_per_unit, supplier, quantity, min_stock_level))
        conn.commit()
        conn.close()
        return item_id

    def get_user_inventory(self, user_id):
        conn = sqlite3.connect('enhanced_farm_management.db', check_same_thread=False)
        df = pd.read_sql_query('SELECT * FROM drug_inventory WHERE user_id = ?', conn, params=[user_id])
        conn.close()
        return df

    def update_inventory_usage(self, user_id, drug_name, batch_number, usage_amount):
        conn = sqlite3.connect('enhanced_farm_management.db', check_same_thread=False)
        c = conn.cursor()
        
        c.execute('''UPDATE drug_inventory 
                    SET current_stock = current_stock - ? 
                    WHERE user_id = ? AND drug_name = ? AND batch_number = ?''',
                  (usage_amount, user_id, drug_name, batch_number))
        conn.commit()
        conn.close()

def get_text(key, lang='en'):
    return LANGUAGES.get(lang, LANGUAGES['en']).get(key, key)

def calculate_compliance_score(df):
    if df.empty:
        return 100.0, [], []
    
    total_score = 100.0
    violations = []
    recommendations = []
    
    current_date = datetime.datetime.now()
    df['safe_date'] = pd.to_datetime(df['safe_date'])
    
    # MRL compliance
    animals_in_withdrawal = df[df['safe_date'] > current_date]
    if len(animals_in_withdrawal) > 0:
        violation_rate = len(animals_in_withdrawal) / len(df)
        score_deduction = min(violation_rate * 40, 40)
        total_score -= score_deduction
        violations.append(f"MRL violations: {len(animals_in_withdrawal)} animals")
        recommendations.append("Ensure withdrawal periods are completed before sale")
    
    # Dosage appropriateness
    inappropriate_dosages = 0
    for _, row in df.iterrows():
        expected_dosage = 5.0  # Default expected dosage
        actual_dosage = row.get('dosage', 5.0)
        if abs(actual_dosage - expected_dosage) > expected_dosage * 0.5:
            inappropriate_dosages += 1
    
    if inappropriate_dosages > 0:
        dosage_violation_rate = inappropriate_dosages / len(df)
        score_deduction = min(dosage_violation_rate * 25, 25)
        total_score -= score_deduction
        violations.append(f"Inappropriate dosages: {inappropriate_dosages}")
        recommendations.append("Follow weight-based dosage guidelines")
    
    # High resistance risk treatments
    high_risk_treatments = df[df.get('ai_risk_score', 0) > 0.7]
    if len(high_risk_treatments) > 0:
        risk_violation_rate = len(high_risk_treatments) / len(df)
        score_deduction = min(risk_violation_rate * 20, 20)
        total_score -= score_deduction
        violations.append(f"High resistance risk treatments: {len(high_risk_treatments)}")
        recommendations.append("Consider alternative antibiotics for high-risk cases")
    
    return max(total_score, 0), violations, recommendations

def show_auth_page(lang):
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab1, tab2 = st.tabs([get_text('login', lang), get_text('register', lang)])

        with tab1:
            st.subheader(f"🔐 {get_text('login', lang)}")
            with st.form("login_form"):
                username = st.text_input(get_text('username', lang))
                password = st.text_input(get_text('password', lang), type="password")
                submit_login = st.form_submit_button(get_text('login', lang))

                if submit_login:
                    user = st.session_state.db.authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.success(f"{get_text('welcome', lang)}, {user['full_name']}!")
                        st.rerun()
                    else:
                        st.error(get_text('invalid_cred', lang))

        with tab2:
            st.subheader(f"📝 {get_text('register', lang)}")
            with st.form("register_form"):
                reg_username = st.text_input(get_text('username', lang), key="reg_user")
                reg_password = st.text_input(get_text('password', lang), type="password", key="reg_pass")
                confirm_password = st.text_input(get_text('confirm_password', lang), type="password")
                full_name = st.text_input(get_text('full_name', lang))
                phone = st.text_input(get_text('phone', lang))
                state = st.selectbox(get_text('state', lang), list(INDIAN_STATES_DISTRICTS.keys()))
                district = st.selectbox(get_text('district', lang), INDIAN_STATES_DISTRICTS.get(state, []))
                user_type_options = [get_text('farmer', lang), get_text('veterinarian', lang), 
                                   get_text('government', lang), get_text('researcher', lang)]
                user_type = st.selectbox(get_text('user_type', lang), user_type_options)
                farm_size = st.number_input(get_text('farm_size', lang), min_value=0.0, step=1.0)

                submit_register = st.form_submit_button(get_text('register', lang))

                if submit_register:
                    if reg_password != confirm_password:
                        st.error(get_text('pass_mismatch', lang))
                    elif len(reg_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    elif not all([reg_username, reg_password, full_name, phone, state, district]):
                        st.error("Please fill all required fields")
                    else:
                        user_type_map = {
                            get_text('farmer', lang): 'farmer',
                            get_text('veterinarian', lang): 'veterinarian',
                            get_text('government', lang): 'government',
                            get_text('researcher', lang): 'researcher'
                        }

                        success = st.session_state.db.register_user(
                            reg_username, reg_password, full_name, phone, state, district,
                            user_type_map[user_type], farm_size
                        )

                        if success:
                            st.success(get_text('reg_success', lang))
                        else:
                            st.error(get_text('user_exists', lang))

def show_dashboard(lang, df):
    st.header(f"📊 {get_text('dashboard', lang)}")
    
    if df.empty:
        st.info("No treatment records found. Start by adding your first treatment record!")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_animals = df['animal_id'].nunique()
        st.metric(get_text('total_animals', lang), total_animals)
    with col2:
        active_treatments = len(df[pd.to_datetime(df['safe_date']) > datetime.datetime.now()])
        st.metric(get_text('active_treatments', lang), active_treatments)
    with col3:
        pending_alerts = active_treatments
        st.metric(get_text('pending_alerts', lang), pending_alerts)
    with col4:
        total_cost = df['cost'].sum() if 'cost' in df.columns else 0
        st.metric(get_text('total_cost', lang), f"₹{total_cost:.2f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(get_text('species_distribution', lang))
        if 'species' in df.columns:
            species_counts = df['species'].value_counts()
            fig = px.pie(values=species_counts.values, names=species_counts.index)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(get_text('usage_trends', lang))
        if 'treatment_date' in df.columns:
            df['treatment_date'] = pd.to_datetime(df['treatment_date'])
            daily_treatments = df.groupby(df['treatment_date'].dt.date).size()
            fig = px.line(x=daily_treatments.index, y=daily_treatments.values)
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent records
    st.subheader(get_text('recent_records', lang))
    display_cols = ['animal_id', 'species', 'drug_name', 'treatment_date', 'safe_date']
    available_cols = [col for col in display_cols if col in df.columns]
    if available_cols:
        st.dataframe(df[available_cols].head(10), use_container_width=True)

def show_view_records(lang, df):
    st.header(f"📋 {get_text('view_records', lang)}")
    
    if df.empty:
        st.info(get_text('no_data', lang))
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        species_filter = st.selectbox("Filter by Species", ['All'] + list(df['species'].unique()) if 'species' in df.columns else ['All'])
    with col2:
        drug_filter = st.selectbox("Filter by Drug", ['All'] + list(df['drug_name'].unique()) if 'drug_name' in df.columns else ['All'])
    with col3:
        date_range = st.date_input("Date Range", value=[datetime.date.today() - timedelta(days=30), datetime.date.today()])
    
    # Apply filters
    filtered_df = df.copy()
    if species_filter != 'All' and 'species' in df.columns:
        filtered_df = filtered_df[filtered_df['species'] == species_filter]
    if drug_filter != 'All' and 'drug_name' in df.columns:
        filtered_df = filtered_df[filtered_df['drug_name'] == drug_filter]
    
    # Search
    search_term = st.text_input(get_text('search', lang))
    if search_term:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_df = filtered_df[mask]
    
    # Display records
    st.dataframe(filtered_df, use_container_width=True)
    
    # Export option
    if st.button(get_text('export_data', lang)):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"treatment_records_{datetime.date.today()}.csv",
            mime="text/csv"
        )

def show_analytics(lang, df):
    st.header(f"🤖 {get_text('analytics', lang)}")
    
    if df.empty:
        st.info(get_text('no_data', lang))
        return
    
    # Train models if not already trained
    if not hasattr(st.session_state.ai_models, 'resistance_model') or st.session_state.ai_models.resistance_model is None:
        with st.spinner("Training AI models..."):
            st.session_state.ai_models.train_models(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(get_text('ai_risk_score', lang))
        if 'ai_risk_score' in df.columns:
            avg_risk = df['ai_risk_score'].mean()
            st.metric("Average Risk Score", f"{avg_risk:.2f}")
            
            fig = px.histogram(df, x='ai_risk_score', title="Risk Score Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(get_text('treatment_efficacy', lang))
        if 'predicted_efficacy' in df.columns:
            avg_efficacy = df['predicted_efficacy'].mean()
            st.metric("Average Efficacy", f"{avg_efficacy:.2f}")
            
            fig = px.histogram(df, x='predicted_efficacy', title="Efficacy Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    # Anomaly detection
    st.subheader(get_text('anomaly_detection', lang))
    df_with_anomalies, num_anomalies = st.session_state.ai_models.detect_anomalies(df)
    st.metric("Anomalies Detected", num_anomalies)
    
    if num_anomalies > 0:
        anomalous_records = df_with_anomalies[df_with_anomalies['is_anomaly'] == True]
        st.dataframe(anomalous_records[['animal_id', 'species', 'drug_name', 'anomaly_score']], use_container_width=True)

def show_alerts(lang, df):
    st.header(f"🚨 {get_text('alerts', lang)}")
    
    alerts = []
    
    # MRL alerts
    current_date = datetime.datetime.now()
    if not df.empty and 'safe_date' in df.columns:
        df['safe_date'] = pd.to_datetime(df['safe_date'])
        mrl_violations = df[df['safe_date'] > current_date]
        
        for _, row in mrl_violations.iterrows():
            alerts.append({
                'type': 'MRL Alert',
                'message': f"Animal {row['animal_id']} safe date: {row['safe_date'].strftime('%Y-%m-%d')}",
                'severity': 'High',
                'date': row['safe_date']
            })
    
    # Low stock alerts (simulated)
    alerts.append({
        'type': 'Inventory Alert',
        'message': 'Amoxicillin stock running low',
        'severity': 'Medium',
        'date': datetime.datetime.now()
    })
    
    # High resistance risk alerts
    if not df.empty and 'ai_risk_score' in df.columns:
        high_risk = df[df['ai_risk_score'] > 0.7]
        for _, row in high_risk.iterrows():
            alerts.append({
                'type': 'Resistance Alert',
                'message': f"High resistance risk for Animal {row['animal_id']}",
                'severity': 'High',
                'date': pd.to_datetime(row['treatment_date']) if 'treatment_date' in row else datetime.datetime.now()
            })
    
    if alerts:
        alerts_df = pd.DataFrame(alerts)
        
        # Color code by severity
        def color_severity(val):
            if val == 'High':
                return 'background-color: #ffebee'
            elif val == 'Medium':
                return 'background-color: #fff3e0'
            else:
                return 'background-color: #e8f5e8'
        
        styled_df = alerts_df.style.applymap(color_severity, subset=['severity'])
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.success("No active alerts!")

def show_predictions(lang, df):
    st.header(f"🔮 {get_text('predictions', lang)}")
    
    if df.empty:
        st.info(get_text('no_data', lang))
        return
    
    # Treatment forecasting
    st.subheader(get_text('forecast', lang))
    if 'treatment_date' in df.columns:
        df['treatment_date'] = pd.to_datetime(df['treatment_date'])
        daily_treatments = df.groupby(df['treatment_date'].dt.date).size()
        
        # Simple forecasting (last 7 days average)
        recent_avg = daily_treatments.tail(7).mean()
        forecast_days = 30
        forecast_dates = [datetime.date.today() + timedelta(days=i) for i in range(1, forecast_days + 1)]
        forecast_values = [int(recent_avg * (1 + np.random.normal(0, 0.1))) for _ in range(forecast_days)]
        
        forecast_df = pd.DataFrame({
            'Date': forecast_dates,
            'Predicted Treatments': forecast_values
        })
        
        fig = px.line(forecast_df, x='Date', y='Predicted Treatments', title="Treatment Forecast (Next 30 days)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Resistance prediction trends
    st.subheader("Resistance Risk Trends")
    if 'ai_risk_score' in df.columns and 'treatment_date' in df.columns:
        df['treatment_date'] = pd.to_datetime(df['treatment_date'])
        risk_trend = df.groupby(df['treatment_date'].dt.date)['ai_risk_score'].mean()
        
        fig = px.line(x=risk_trend.index, y=risk_trend.values, title="Average Resistance Risk Over Time")
        st.plotly_chart(fig, use_container_width=True)

def show_compliance(lang, df):
    st.header(f"✅ {get_text('compliance', lang)}")
    
    score, violations, recommendations = calculate_compliance_score(df)
    
    # Compliance score
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(get_text('compliance_score', lang), f"{score:.1f}%")
        
        if score >= 90:
            st.success("Excellent compliance!")
        elif score >= 70:
            st.warning("Good compliance with room for improvement")
        else:
            st.error("Compliance issues need attention")
    
    with col2:
        # Compliance gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Compliance Score"},
            gauge={'axis': {'range': [None, 100]},
                  'bar': {'color': "darkgreen" if score >= 90 else "orange" if score >= 70 else "red"},
                  'steps': [{'range': [0, 70], 'color': "lightgray"},
                           {'range': [70, 90], 'color': "gray"}],
                  'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 90}}))
        st.plotly_chart(fig, use_container_width=True)
    
    # Violations and recommendations
    if violations:
        st.subheader(get_text('violations', lang))
        for violation in violations:
            st.error(f"❌ {violation}")
    
    if recommendations:
        st.subheader(get_text('recommendations', lang))
        for rec in recommendations:
            st.info(f"💡 {rec}")

def show_inventory(lang, user_id):
    st.header(f"📦 {get_text('inventory', lang)}")
    
    # Add inventory item form
    with st.expander(get_text('add_inventory', lang)):
        with st.form("inventory_form"):
            col1, col2 = st.columns(2)
            with col1:
                drug_name = st.selectbox(get_text('drug_name', lang), list(ANTIMICROBIALS_DB.keys()))
                batch_number = st.text_input(get_text('batch_number', lang))
                quantity = st.number_input(get_text('quantity', lang), min_value=0.0)
                unit = st.selectbox(get_text('unit', lang), ['ml', 'tablets', 'vials', 'kg'])
            with col2:
                purchase_date = st.date_input(get_text('purchase_date', lang))
                expiry_date = st.date_input(get_text('expiry_date', lang))
                cost_per_unit = st.number_input(get_text('cost_per_unit', lang), min_value=0.0)
                supplier = st.text_input(get_text('supplier', lang))
            
            if st.form_submit_button("Add Item"):
                if drug_name and batch_number and quantity > 0:
                    st.session_state.db.add_inventory_item(
                        user_id, drug_name, batch_number, quantity, unit,
                        purchase_date, expiry_date, cost_per_unit, supplier
                    )
                    st.success("Inventory item added!")
                    st.rerun()
    
    # Display inventory
    inventory_df = st.session_state.db.get_user_inventory(user_id)
    
    if not inventory_df.empty:
        # Alerts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(get_text('low_stock', lang))
            low_stock = inventory_df[inventory_df['current_stock'] <= inventory_df['min_stock_level']]
            if not low_stock.empty:
                st.dataframe(low_stock[['drug_name', 'current_stock', 'min_stock_level']], use_container_width=True)
            else:
                st.success("All items adequately stocked")
        
        with col2:
            st.subheader(get_text('expiring_soon', lang))
            thirty_days_ahead = datetime.date.today() + timedelta(days=30)
            expiring_soon = inventory_df[pd.to_datetime(inventory_df['expiry_date']) <= pd.to_datetime(thirty_days_ahead)]
            if not expiring_soon.empty:
                st.dataframe(expiring_soon[['drug_name', 'batch_number', 'expiry_date']], use_container_width=True)
            else:
                st.success("No items expiring soon")
        
        # Full inventory table
        st.subheader("Current Inventory")
        st.dataframe(inventory_df, use_container_width=True)
    else:
        st.info("No inventory items found. Add your first inventory item above.")

def show_financial(lang, df, user_id):
    st.header(f"💰 {get_text('financial', lang)}")
    
    if df.empty:
        st.info(get_text('no_data', lang))
        return
    
    # Financial metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_cost = df['cost'].sum() if 'cost' in df.columns else 0
        st.metric(get_text('total_cost', lang), f"₹{total_cost:.2f}")
    
    with col2:
        monthly_cost = df[pd.to_datetime(df['treatment_date']) >= pd.to_datetime('today') - pd.DateOffset(months=1)]['cost'].sum() if 'cost' in df.columns else 0
        st.metric(get_text('monthly_cost', lang), f"₹{monthly_cost:.2f}")
    
    with col3:
        total_animals = df['animal_id'].nunique()
        cost_per_animal = total_cost / total_animals if total_animals > 0 else 0
        st.metric(get_text('cost_per_animal', lang), f"₹{cost_per_animal:.2f}")
    
    with col4:
        # Average cost per treatment
        avg_cost_per_treatment = df['cost'].mean() if 'cost' in df.columns else 0
        st.metric("Avg Cost/Treatment", f"₹{avg_cost_per_treatment:.2f}")
    
    # Financial charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(get_text('cost_analysis', lang))
        if 'treatment_date' in df.columns and 'cost' in df.columns:
            df['treatment_date'] = pd.to_datetime(df['treatment_date'])
            monthly_costs = df.groupby(df['treatment_date'].dt.to_period('M'))['cost'].sum()
            fig = px.bar(x=monthly_costs.index.astype(str), y=monthly_costs.values, title="Monthly Treatment Costs")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Cost by Drug")
        if 'drug_name' in df.columns and 'cost' in df.columns:
            drug_costs = df.groupby('drug_name')['cost'].sum().sort_values(ascending=False)
            fig = px.pie(values=drug_costs.values, names=drug_costs.index, title="Cost Distribution by Drug")
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed cost breakdown
    st.subheader("Cost Breakdown")
    if 'cost' in df.columns:
        cost_breakdown = df.groupby(['species', 'drug_name'])['cost'].agg(['sum', 'count', 'mean']).round(2)
        cost_breakdown.columns = ['Total Cost', 'Treatments', 'Avg Cost']
        st.dataframe(cost_breakdown, use_container_width=True)

def show_add_treatment(lang, user_id):
    st.header(f"💊 {get_text('add_treatment', lang)}")
    
    with st.form("treatment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            animal_id = st.text_input(get_text('animal_id', lang))
            species = st.selectbox(get_text('species', lang), SPECIES_OPTIONS)
            breed = st.selectbox(get_text('breed', lang), SPECIES_BREEDS.get(species, {}).get('breeds', []))
            age = st.number_input(get_text('age', lang), min_value=0)
            weight = st.number_input(get_text('weight', lang), min_value=0.0)
        
        with col2:
            drug_name = st.selectbox(get_text('drug_name', lang), list(ANTIMICROBIALS_DB.keys()))
            batch_number = st.text_input(get_text('batch_number', lang))
            dosage = st.number_input(get_text('dosage', lang), min_value=0.1)
            treatment_date = st.date_input(get_text('treatment_date', lang), value=datetime.date.today())
            reason = st.selectbox(get_text('reason', lang), TREATMENT_REASONS)
            
        withdrawal_period = ANTIMICROBIALS_DB[drug_name]['withdrawal_days']
        cost = st.number_input("Cost (₹)", min_value=0.0, value=ANTIMICROBIALS_DB[drug_name]['cost_per_dose'])
        severity_score = st.slider("Severity Score", 1, 10, 5)
        
        # AI Predictions
        treatment_data = {
            'species': species, 'drug_name': drug_name, 'reason': reason, 
            'age': age, 'weight': weight, 'dosage': dosage, 'withdrawal_period': withdrawal_period
        }
        
        ai_risk_score = st.session_state.ai_models.predict_resistance_risk(treatment_data)
        ai_recommended_dosage = st.session_state.ai_models.predict_optimal_dosage(treatment_data)
        predicted_efficacy = st.session_state.ai_models.predict_efficacy(treatment_data)
        environmental_impact = ANTIMICROBIALS_DB[drug_name]['environmental_impact']
        
        # Display AI predictions
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"AI Risk Score: {ai_risk_score:.2f}")
        with col2:
            st.info(f"AI Recommended Dosage: {ai_recommended_dosage:.2f} mg/kg")
        with col3:
            st.info(f"Predicted Efficacy: {predicted_efficacy:.2f}")
        
        safe_date = treatment_date + timedelta(days=withdrawal_period)
        st.info(f"🗓️ {get_text('safe_date', lang)}: **{safe_date}**")
        
        submit_treatment = st.form_submit_button(get_text('submit', lang))
        
        if submit_treatment:
            if not animal_id:
                st.error("Please enter Animal ID")
            else:
                success = st.session_state.db.add_treatment_record(
                    user_id, animal_id, species, breed, age, weight, drug_name, batch_number, 
                    dosage, treatment_date, reason, severity_score, withdrawal_period, cost, 
                    ai_risk_score, ai_recommended_dosage, predicted_efficacy, environmental_impact
                )
                if success:
                    st.success(get_text('record_added', lang))
                    # Update inventory usage
                    st.session_state.db.update_inventory_usage(user_id, drug_name, batch_number, dosage * weight / 1000)
                    st.rerun()
                else:
                    st.error("Failed to add record")

def show_main_app(lang):
    user = st.session_state.user
    user_id = user['id']
    
    # Sidebar navigation
    st.sidebar.markdown(f"### {get_text('welcome', lang)}, {user['full_name']}")
    st.sidebar.markdown(f"**Role:** {user['user_type'].title()}")
    st.sidebar.markdown(f"**State:** {user['state']}, **District:** {user['district']}")
    if user.get('farm_size'):
        st.sidebar.markdown(f"**Farm Size:** {user['farm_size']} acres")
    st.sidebar.markdown("---")
    
    pages = [
        get_text('dashboard', lang),
        get_text('add_treatment', lang),
        get_text('view_records', lang),
        get_text('analytics', lang),
        get_text('alerts', lang),
        get_text('predictions', lang),
        get_text('compliance', lang),
        get_text('inventory', lang),
        get_text('financial', lang)
    ]
    
    selected_page = st.sidebar.radio("Navigation", pages)
    
    if st.sidebar.button(f"🚪 {get_text('logout', lang)}"):
        st.session_state.user = None
        st.rerun()
    
    # Get user treatments
    df = st.session_state.db.get_user_treatments(user_id)
    
    # Show selected page
    if selected_page == get_text('dashboard', lang):
        show_dashboard(lang, df)
    elif selected_page == get_text('add_treatment', lang):
        show_add_treatment(lang, user_id)
    elif selected_page == get_text('view_records', lang):
        show_view_records(lang, df)
    elif selected_page == get_text('analytics', lang):
        show_analytics(lang, df)
    elif selected_page == get_text('alerts', lang):
        show_alerts(lang, df)
    elif selected_page == get_text('predictions', lang):
        show_predictions(lang, df)
    elif selected_page == get_text('compliance', lang):
        show_compliance(lang, df)
    elif selected_page == get_text('inventory', lang):
        show_inventory(lang, user_id)
    elif selected_page == get_text('financial', lang):
        show_financial(lang, df, user_id)

def main():
    # Initialize database and AI models
    if 'db' not in st.session_state:
        st.session_state.db = EnhancedDatabaseManager()

    if 'ai_models' not in st.session_state:
        st.session_state.ai_models = AdvancedAIModelManager()
        # Train models if data exists
        df = st.session_state.db.get_all_treatments()
        if not df.empty:
            st.session_state.ai_models.train_models(df)

    # Language selector
    languages = {
        'en': "English", 'hi': "हिंदी", 'bn': "বাংলা", 'te': "తెలుగు",
        'ta': "தமிழ்", 'gu': "ગુજરાતી", 'ml': "മലയാളം", 'pa': "ਪੰਜਾਬੀ"
    }
    
    lang = st.sidebar.selectbox(
        "🌐 Language / भाषा",
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        key='language'
    )

    # Main title
    st.title(f"🚜 {get_text('app_title', lang)}")
    st.markdown(f"**{get_text('tagline', lang)}**")

    # System status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("System Status", "Online", delta="Healthy")
    with col2:
        st.metric("AI Models", "Active", delta="Ready")
    with col3:
        st.metric("Database", "Connected", delta="All tables ready")

    st.markdown("---")

    # Authentication
    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        show_auth_page(lang)
    else:
        show_main_app(lang)

# Demo data creation
if st.sidebar.button("🧪 Create Demo Data"):
    try:
        # Create demo user
        st.session_state.db.register_user('demo', 'demo123', 'Demo User', '1234567890', 
                                         'Maharashtra', 'Mumbai', 'farmer', 50.0)
        
        # Add demo treatment records
        user = st.session_state.db.authenticate_user('demo', 'demo123')
        if user:
            for i in range(10):
                st.session_state.db.add_treatment_record(
                    user['id'], f'COW-{i+1}', 'Cattle', 'Holstein Friesian', 
                    np.random.randint(12, 60), np.random.randint(400, 600),
                    np.random.choice(list(ANTIMICROBIALS_DB.keys())), f'BATCH-{i+1}',
                    np.random.uniform(3, 8), datetime.date.today() - timedelta(days=np.random.randint(0, 30)),
                    np.random.choice(TREATMENT_REASONS), np.random.randint(3, 8),
                    np.random.randint(5, 21), np.random.uniform(100, 500),
                    np.random.uniform(0.2, 0.8), np.random.uniform(3, 8),
                    np.random.uniform(0.7, 0.95), np.random.uniform(0.3, 0.8)
                )
        
        st.sidebar.success("Demo data created! Login with username 'demo', password 'demo123'")
    except Exception as e:
        st.sidebar.error(f"Error creating demo data: {str(e)}")

if __name__ == "__main__":
    main()