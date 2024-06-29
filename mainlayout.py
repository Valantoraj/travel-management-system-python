from customtkinter import *
from tkinter import ttk
import regex as re
from tkinter import messagebox
import sqlite3
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from tkinter import Frame, BOTH, Scrollbar, RIGHT, Y
from tkinter.ttk import Notebook
from tkinter import *
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from access.train_manager import TrainManager
from access.geo_manager import GeoManager
from access.hotel_manager import HotelFinder
from ui_tab import UI
tab_display=UI()
location_access=GeoManager()
train_access=TrainManager()
hotel_access=HotelFinder()


conn = sqlite3.connect("places_details.db")
c = conn.cursor()

connb = sqlite3.connect('booking_details.db')
cu = connb.cursor()

cu.execute('''
            CREATE TABLE IF NOT EXISTS booking_details(
                rowid TEXT,
                booking_id TEXT,
                name TEXT,
                state TEXT,
                city TEXT,
                email TEXT,
                phone_no TEXT,
                destination TEXT,
                days TEXT,
                people TEXT,
                mode TEXT,
                guide TEXT,
                date TEXT
            )
            ''')
connb.commit()


def convert_rr_format_to_dmy(input_date):
    if len(input_date) != 7:
        raise ValueError("Input date format (m/d/yy) should be exactly 7 characters long.")

    month, day, year = map(int, input_date.split('/'))

    if year >= 0 and year <= 29:
        full_year = 2000 + year
    else:
        full_year = 1900 + year

    date_string = f"{month}/{day}/{full_year}"
    parsed_date = datetime.strptime(date_string, "%m/%d/%Y")

    formatted_date = parsed_date.strftime("%d-%m-%Y")

    return formatted_date


def nth_date(input_date, x):
    date_format = "%d-%m-%Y"
    start_date = datetime.strptime(input_date, date_format)

    fifth_date = start_date + timedelta(days=x)

    result_date = fifth_date.strftime("%d-%m-%Y")

    return result_date


India ={'Arunachal Pradesh': {'Anjaw': ['Hayuliang', 'HML'], 'Changlang': ['Nampong', 'NAM'], 'Dibang Valley': ['Roing', 'ROD'], 'East Kameng': ['Seppa', 'NHNL'], 'East Siang': ['Yingkiong', 'YUPI'], 'Kamle': ['Raga', 'LUK'], 'Kra Daadi': ['Pip Sorang', 'TNG'], 'Kurung Kumey': ['Koloriang', 'BYZ'], 'Lepa Rada': ['Tato', 'NMY'], 'Lohit': ['Tezu', 'MRPT'], 'Longding': ['Longding', 'LKDR'], 'Lower Dibang Valley': ['Roing', 'LDV'], 'Lower Siang': ['Yingkiong', 'SBK'], 'Lower Subansiri': ['Ziro', 'HMY'], 'Namsai': ['Namsai', 'NMY'], 'Pakke Kessang': ['Seijosa', 'NMY'], 'Papum Pare': ['Itanagar', 'LTKN'], 'Shi Yomi': ['Tato', 'KXL'], 'Siang': ['Pasighat', 'KXL'], 'Tawang': ['Tawang', 'TNH'], 'Tirap': ['Khonsa', 'RNY'], 'Upper Siang': ['Yingkiong', 'RNY'], 'Upper Subansiri': ['Daporijo', 'YUPI'], 'West Kameng': ['Bomdila', 'BAI'], 'West Siang': ['Along', 'YUPI']}, 'Andhra Pradesh': {'Anantapur': ['Anantapur', 'ATP'], 'Chittoor': ['Kathipudi', 'KHT'], 'East Godavari': ['Kakinada', 'COA'], 'Guntur': ['Guntur', 'GNT'], 'Krishna': ['Vijayawada', 'BZA'], 'Kurnool': ['Kurnool', 'GTL'], 'Prakasam': ['Ongole', 'OGL'], 'Sri Potti Sriramulu Nellore': ['Nellore', 'NEL'], 'Srikakulam': ['Srikakulam', 'CHE'], 'Visakhapatnam': ['Visakhapatnam', 'VSKP'], 'Vizianagaram': ['Vizianagaram', 'VZM'], 'West Godavari': ['Bhimavaram', 'BZA'], 'YSR Kadapa': ['Kadapa', 'HX']}, 'Assam': {'Baksa': ['Salbari', 'NBQ'], 'Barpeta': ['Barpeta Road', 'BEH'], 'Biswanath': ['Biswanath Chariali', 'BPB'], 'Bongaigaon': ['Bongaigaon', 'NBQ'], 'Cachar': ['Silchar', 'SCL'], 'Charaideo': ['Sonari', 'MXN'], 'Chirang': ['Bongaigaon', 'NBQ'], 'Darrang': ['Mangaldoi', 'RPAN'], 'Dhemaji': ['Dhemaji', 'DMG'], 'Dhubri': ['Dhubri', 'DBB'], 'Dibrugarh': ['Dibrugarh', 'DBRG'], 'Dima Hasao': ['Haflong', 'DPU'], 'Goalpara': ['Goalpara', 'GLPT'], 'Golaghat': ['Golaghat', 'GLGT'], 'Hailakandi': ['Hailakandi', 'HLKD'], 'Hojai': ['Hojai', 'JPZ'], 'Jorhat': ['Jorhat', 'JTTN'], 'Kamrup': ['Kamrup', 'RNY'], 'Kamrup Metropolitan': ['Guwahati', 'GHY'], 'Karbi Anglong': ['Diphu', 'DMV'], 'Karimganj': ['Karimganj', 'KXJ'], 'Kokrajhar': ['Kokrajhar', 'NBQ'], 'Lakhimpur': ['North Lakhimpur', 'LHBR'], 'Majuli': ['Majuli', 'JTTN'], 'Morigaon': ['Morigaon', 'MXN'], 'Nagaon': ['Nagaon', 'NGN'], 'Nalbari': ['Nalbari', 'NLV'], 'Sivasagar': ['Sivasagar', 'SVQ'], 'Sonitpur': ['Tezpur', 'TZTB'], 'South Salmara Mankachar': ['Dhubri', 'DBB'], 'Tinsukia': ['Tinsukia', 'TSK'], 'Udalguri': ['Udalguri', 'ULG']}, 'Bihar': {'Araria': ['Araria', 'ARIA'], 'Arwal': ['Arwal', 'ARW'], 'Aurangabad': ['Aurangabad', 'AWB'], 'Banka': ['Bhagalpur', 'BGP'], 'Begusarai': ['Begusarai', 'BGS'], 'Bhagalpur': ['Bhagalpur', 'BGP'], 'Bhojpur': ['Ara', 'BXR'], 'Buxar': ['Buxar', 'BXR'], 'Darbhanga': ['Darbhanga', 'DBG'], 'East Champaran': ['Motihari', 'MKI'], 'Gaya': ['Gaya', 'GAYA'], 'Gopalganj': ['Gopalganj', 'GOP'], 'Jamui': ['Jamui', 'JMU'], 'Jehanabad': ['Jehanabad', 'JHD'], 'Kaimur': ['Bhabua Road', 'BBU'], 'Katihar': ['Katihar', 'KIR'], 'Khagaria': ['Khagaria', 'KGG'], 'Kishanganj': ['Kishanganj', 'KNE'], 'Lakhisarai': ['Lakhisarai', 'LKR'], 'Madhepura': ['Madhepura', 'MNE'], 'Madhubani': ['Madhubani', 'MBI'], 'Munger': ['Munger', 'MGR'], 'Muzaffarpur': ['Muzaffarpur', 'MFP'], 'Nalanda': ['Bihar Sharif', 'BEHS'], 'Nawada': ['Nawadah', 'NWD'], 'Patna': ['Patna', 'PNBE'], 'Purnia': ['Purnia', 'PRNA'], 'Rohtas': ['Sasaram', 'SSM'], 'Saharsa': ['Saharsa', 'SHC'], 'Samastipur': ['Samastipur', 'SPJ'], 'Saran': ['Chhapra', 'CPR'], 'Sheikhpura': ['Sheikhpura', 'SHK'], 'Sheohar': ['Sheohar', 'SHR'], 'Sitamarhi': ['Sitamarhi', 'SMI'], 'Siwan': ['Siwan', 'SV'], 'Supaul': ['Supaul', 'SCL'], 'Vaishali': ['Hajipur', 'HJP'], 'West Champaran': ['Bettiah', 'BTH']}, 'Chandigarh': {'Chandigarh': ['Chandigarh', 'CDG']}, 'Chhattisgarh': {'Balod': ['Balod', 'BAO'], 'Baloda Bazar': ['Baloda Bazar', 'BPHB'], 'Balrampur': ['Balrampur', 'BRP'], 'Bastar': ['Jagdalpur', 'JDB'], 'Bemetara': ['Bemetara', 'BMTR'], 'Bijapur': ['Bijapur', 'BYP'], 'Bilaspur': ['Bilaspur', 'BSP'], 'Dantewada': ['Dantewada', 'DWZ'], 'Dhamtari': ['Dhamtari', 'DTR'], 'Durg': ['Durg', 'DURG'], 'Gariaband': ['Gariaband', 'GBQ'], 'Gaurela Pendra Marwahi': ['Gaurela', 'GAE'], 'Janjgir-Champa': ['Janjgir', 'JNR'], 'Jashpur': ['Jashpurnagar', 'JSP'], 'Kabirdham': ['Kawardha', 'KRBA'], 'Kanker': ['Kanker', 'KRAR'], 'Kondagaon': ['Kondagaon', 'KNG'], 'Korba': ['Korba', 'KRBA'], 'Koriya': ['Korea', 'KRBA'], 'Mahasamund': ['Mahasamund', 'MSMD'], 'Mungeli': ['Mungeli', 'MGG'], 'Narayanpur': ['Narayanpur', 'NRYP'], 'Raigarh': ['Raigarh', 'RIG'], 'Raipur': ['Raipur', 'R'], 'Rajnandgaon': ['Rajnandgaon', 'RJN'], 'Sukma': ['Sukma', 'SKM'], 'Surajpur': ['Surajpur', 'SRP'], 'Surguja': ['Ambikapur', 'ABKP']}, 'Dadra and Nagar Haveli and Daman and Diu': {'Dadra and Nagar Haveli': {'Dadra and Nagar Haveli': ['Dadra and Nagar Haveli', 'DNH']}, 'Daman': {'Daman': ['Daman', 'NMB']}, 'Diu': {'Diu': ['Diu', 'DUI']}}, 'Delhi': {'Central Delhi': ['Delhi', 'DL'], 'East Delhi': ['Delhi', 'DL'], 'New Delhi': ['Delhi', 'DL'], 'North Delhi': ['Delhi', 'DL'], 'North East Delhi': ['Delhi', 'DL'], 'North West Delhi': ['Delhi', 'DL'], 'Shahdara': ['Delhi', 'DL'], 'South Delhi': ['Delhi', 'DL'], 'South East Delhi': ['Delhi', 'DL'], 'South West Delhi': ['Delhi', 'DL'], 'West Delhi': ['Delhi', 'DL']}, 'Goa': {'North Goa': ['Goa', 'GOA'], 'South Goa': ['Goa', 'GOA']}, 'Gujarat': {'Ahmedabad': ['Ahmedabad', 'ADI'], 'Amreli': ['Amreli', 'AMRE'], 'Anand': ['Anand', 'ANND'], 'Aravalli': ['Aravalli', 'AVLI'], 'Banaskantha': ['Palanpur', 'PNU'], 'Bharuch': ['Bharuch', 'BH'], 'Bhavnagar': ['Bhavnagar', 'BVC'], 'Botad': ['Botad', 'BTD'], 'Chhota Udaipur': ['Chhota Udaipur', 'CTD'], 'Dahod': ['Dahod', 'DHD'], 'Dang': ['Ahwa', 'DGI'], 'Devbhoomi Dwarka': ['Khambhalia', 'KMBL'], 'Gandhinagar': ['Gandhinagar', 'GNC'], 'Gir Somnath': ['Veraval', 'VRL'], 'Jamnagar': ['Jamnagar', 'JAM'], 'Junagadh': ['Junagadh', 'JND'], 'Kheda': ['Nadiad', 'ND'], 'Kutch': ['Bhuj', 'BHUJ'], 'Mahisagar': ['Godhra', 'GDA'], 'Mehsana': ['Mehsana', 'MSH'], 'Morbi': ['Morbi', 'MORBI'], 'Narmada': ['Rajpipla', 'RJPI'], 'Navsari': ['Navsari', 'NVS'], 'Panchmahal': ['Godhra', 'GDA'], 'Patan': ['Patan', 'PTN'], 'Porbandar': ['Porbandar', 'PBR'], 'Rajkot': ['Rajkot', 'RJT'], 'Sabarkantha': ['Himmatnagar', 'HMT'], 'Surat': ['Surat', 'ST'], 'Surendranagar': ['Surendranagar', 'SRNR'], 'Tapi': ['Vyara', 'VYA'], 'Vadodara': ['Vadodara', 'BRC'], 'Valsad': ['Valsad', 'BL']}, 'Haryana': {'Ambala': ['Ambala Cantt', 'UMB'], 'Bhiwani': ['Bhiwani', 'BNW'], 'Charkhi Dadri': ['Charkhi Dadri', 'CKD'], 'Faridabad': ['Faridabad', 'FDB'], 'Fatehabad': ['Fatehabad', 'FAB'], 'Gurugram': ['Gurgaon', 'GGN'], 'Hisar': ['Hisar', 'HSR'], 'Jhajjar': ['Jhajjar', 'JHJ'], 'Jind': ['Jind', 'JIND'], 'Kaithal': ['Kaithal', 'KLE'], 'Karnal': ['Karnal', 'KUN'], 'Kurukshetra': ['Kurukshetra', 'KUN'], 'Mahendragarh': ['Nangal Chaudhary', 'NNU'], 'Nuh': ['Nuh', 'NUH'], 'Palwal': ['Palwal', 'PW'], 'Panchkula': ['Panchkula', 'PKL'], 'Panipat': ['Panipat', 'PNP'], 'Rewari': ['Rewari', 'RE'], 'Rohtak': ['Rohtak', 'ROK'], 'Sirsa': ['Sirsa', 'SSA'], 'Sonipat': ['Sonipat', 'SNP'], 'Yamunanagar': ['Jagadhri', 'JUD']}, 'Himachal Pradesh': {'Bilaspur': ['Bilaspur', 'BLSP'], 'Chamba': ['Chamba', 'CHMB'], 'Hamirpur': ['Hamirpur', 'HMR'], 'Kangra': ['Pathankot', 'PTKC'], 'Kinnaur': ['Kinnaur', 'KML'], 'Kullu': ['Kullu', 'KUU'], 'Lahaul and Spiti': ['Lahul', 'LHL'], 'Mandi': ['Mandi', 'MNDI'], 'Shimla': ['Simla', 'SML'], 'Sirmaur': ['Sirmaur', 'SRMR'], 'Solan': ['Solan', 'SLN'], 'Una': ['Una', 'UNA']}, 'Jammu and Kashmir': {'Anantnag': ['Anantnag', 'ANT'], 'Bandipora': ['Bandipore', 'BDPR'], 'Baramulla': ['Baramula', 'BRML'], 'Budgam': ['Badgam', 'BDGM'], 'Doda': ['Doda', 'DODA'], 'Ganderbal': ['Ganderbal', 'GABL'], 'Jammu': ['Jammu Tawi', 'JAT'], 'Kathua': ['Kathua', 'KTHU'], 'Kishtwar': ['Kishtwar', 'KSTR'], 'Kulgam': ['Kulgam', 'KM'], 'Kupwara': ['Kupwara', 'KIR'], 'Poonch': ['Poonch', 'PON'], 'Pulwama': ['Pulwama', 'PLM'], 'Rajouri': ['Rajouri', 'RJY'], 'Ramban': ['Ramban', 'RMF'], 'Reasi': ['Reasi', 'RSI'], 'Samba': ['Samba', 'SMB'], 'Shopian': ['Shupiyan', 'SPN'], 'Srinagar': ['Srinagar', 'SINA'], 'Udhampur': ['Udhampur', 'UHP']}, 'Jharkhand': {'Bokaro': ['Bokaro Steel City', 'BKSC'], 'Chatra': ['Chatra', 'CTR'], 'Deoghar': ['Deoghar', 'DGHR'], 'Dhanbad': ['Dhanbad', 'DHN'], 'Dumka': ['Dumka', 'DUMK'], 'East Singhbhum': ['Tatanagar', 'TATA'], 'Garhwa': ['Garwa Road', 'GHD'], 'Giridih': ['Giridih', 'GRD'], 'Godda': ['Godda', 'GODA'], 'Gumla': ['Gumla', 'GUMI'], 'Hazaribagh': ['Hazaribagh', 'HZD'], 'Jamtara': ['Jamtara', 'JMT'], 'Khunti': ['Khunti', 'KXN'], 'Koderma': ['Koderma', 'KQR'], 'Latehar': ['Latehar', 'LTHR'], 'Lohardaga': ['Lohardaga', 'LAD'], 'Pakur': ['Pakur', 'PKR'], 'Palamu': ['Daltonganj', 'DTO'], 'Ramgarh': ['Ramgarh', 'RRME'], 'Ranchi': ['Ranchi', 'RNC'], 'Sahebganj': ['Sahebganj', 'SHW'], 'Seraikela Kharsawan': ['Sini', 'SINI'], 'Simdega': ['Simdega', 'SMH'], 'West Singhbhum': ['Chaibasa', 'CBSA']}, 'Karnataka': {'Bagalkot': ['Bagalkot', 'BGK'], 'Ballari': ['Bellary', 'BAY'], 'Belagavi': ['Belgaum', 'BGM'], 'Bengaluru Rural': ['Bengaluru', 'SBC'], 'Bengaluru Urban': ['Bengaluru', 'SBC'], 'Bidar': ['Bidar', 'BIDR'], 'Chamarajanagar': ['Chamarajanagar', 'CMNR'], 'Chikballapur': ['Chik Ballapur', 'CBP'], 'Chikkamagaluru': ['Chikmagalur', 'CMGR'], 'Chitradurga': ['Chitradurga', 'CTA'], 'Dakshina Kannada': ['Mangalore', 'MAQ'], 'Davanagere': ['Davangere', 'DVG'], 'Dharwad': ['Dharwar', 'DWR'], 'Gadag': ['Gadag', 'GDG'], 'Hassan': ['Hassan', 'HAS'], 'Haveri': ['Haveri', 'HVR'], 'Kalaburagi': ['Gulbarga', 'GR'], 'Kodagu': ['Mysore', 'MYS'], 'Kolar': ['Kolar', 'KQZ'], 'Koppal': ['Koppal', 'KBL'], 'Mandya': ['Mandya', 'MYA'], 'Mysuru': ['Mysore', 'MYS'], 'Raichur': ['Raichur', 'RC'], 'Ramanagara': ['Ramanagar', 'RMGM'], 'Shivamogga': ['Shimoga', 'SME'], 'Tumakuru': ['Tumkur', 'TK'], 'Udupi': ['Udupi', 'UD'], 'Uttara Kannada': ['Karwar', 'KAWR'], 'Vijayapura': ['Vijayapura', 'BJP'], 'Yadgir': ['Yadgir', 'YG']}, 'Kerala': {'Alappuzha': ['Alleppey', 'ALLP'], 'Ernakulam': ['Ernakulam', 'ERS'], 'Idukki': ['Idukki', 'IDK'], 'Kannur': ['Kannur', 'CAN'], 'Kasaragod': ['Kasaragod', 'KGQ'], 'Kollam': ['Quilon', 'QLN'], 'Kottayam': ['Kottayam', 'KTYM'], 'Kozhikode': ['Calicut', 'CLT'], 'Malappuram': ['Malappuram', 'MLPM'], 'Palakkad': ['Palghat', 'PGT'], 'Pathanamthitta': ['Tiruvalla', 'TRVL'], 'Thiruvananthapuram': ['Trivandrum', 'TVC'], 'Thrissur': ['Trichur', 'TCR'], 'Wayanad': ['Kalpetta', 'KT'], 'Lakshadweep': ['Lakshadweep', 'LD']}, 'Ladakh': {'Kargil': ['Kargil', 'IXK'], 'Leh': ['Leh', 'IXL']}, 'Lakshadweep': {'Agatti Island': ['Agatti Island', 'AGX'], 'Amini Island': ['Amini Island', 'AMN'], 'Androth Island': ['Androth Island', 'ANU'], 'Bithra Island': ['Bithra Island', 'IXL'], 'Chetlat Island': ['Chetlat Island', 'CHT'], 'Kadmat Island': ['Kadmat Island', 'KXT'], 'Kalpeni Island': ['Kalpeni Island', 'KAX'], 'Kavaratti': ['Kavaratti', 'KJT'], 'Kiltan Island': ['Kiltan Island', 'ILT'], 'Minicoy Island': ['Minicoy Island', 'MCI'], 'North Island': ['North Island', 'NRI'], 'Pitti Island': ['Pitti Island', 'PIT'], 'South Island': ['South Island', 'SXO'], 'Suheli Par': ['Suheli Par', 'SZL'], 'Thinnakara Island': ['Thinnakara Island', 'THL']}, 'Madhya Pradesh': {'Agar Malwa': ['Agar Malwa', 'AGAR'], 'Alirajpur': ['Alirajpur', 'ARJ'], 'Anuppur': ['Anuppur', 'APR'], 'Ashoknagar': ['Ashoknagar', 'ASKN'], 'Balaghat': ['Balaghat', 'BTC'], 'Barwani': ['Barwani', 'BAW'], 'Betul': ['Betul', 'BZU'], 'Bhind': ['Bhind', 'BIX'], 'Bhopal': ['Bhopal', 'BPL'], 'Burhanpur': ['Burhanpur', 'BAU'], 'Chhatarpur': ['Chhatarpur', 'CTC'], 'Chhindwara': ['Chhindwara', 'CWA'], 'Damoh': ['Damoh', 'DMO'], 'Datia': ['Datia', 'DAA'], 'Dewas': ['Dewas', 'DWX'], 'Dhar': ['Dhar', 'DAR'], 'Dindori': ['Dindori', 'DND'], 'Guna': ['Guna', 'GUNA'], 'Gwalior': ['Gwalior', 'GWL'], 'Harda': ['Harda', 'HD'], 'Hoshangabad': ['Hoshangabad', 'HBD'], 'Indore': ['Indore', 'INDB'], 'Jabalpur': ['Jabalpur', 'JBP'], 'Jhabua': ['Jhabua', 'JHW'], 'Katni': ['Katni', 'KTE'], 'Khandwa': ['Khandwa', 'KNW'], 'Khargone': ['Khargone', 'KGN'], 'Mandla': ['Mandla', 'MMD'], 'Mandsaur': ['Mandsaur', 'MDS'], 'Morena': ['Morena', 'MRA'], 'Narsinghpur': ['Narsinghpur', 'NU'], 'Neemuch': ['Neemuch', 'NAD'], 'Panna': ['Panna', 'PNR'], 'Raisen': ['Raisen', 'BXR'], 'Rajgarh': ['Rajgarh', 'DAV'], 'Ratlam': ['Ratlam', 'RTM'], 'Rewa': ['Rewa', 'REWA'], 'Sagar': ['Sagar', 'SGO'], 'Satna': ['Satna', 'STA'], 'Sehore': ['Sehore', 'SEH'], 'Seoni': ['Seoni', 'SEY'], 'Shahdol': ['Shahdol', 'SDL'], 'Shajapur': ['Shajapur', 'SFY'], 'Sheopur': ['Sheopur', 'SOE'], 'Shivpuri': ['Shivpuri', 'SVPI'], 'Sidhi': ['Sidhi', 'SDY'], 'Singrauli': ['Singrauli', 'SGRL'], 'Tikamgarh': ['Tikamgarh', 'TKMG'], 'Ujjain': ['Ujjain', 'UJN'], 'Umaria': ['Umaria', 'UMR'], 'Vidisha': ['Vidisha', 'BHS']}, 'Maharashtra': {'Ahmednagar': ['Ahmednagar', 'ANG'], 'Akola': ['Akola', 'AK'], 'Amravati': ['Amravati', 'AMI'], 'Aurangabad': ['Aurangabad', 'AWB'], 'Beed': ['Bid', 'BID'], 'Bhandara': ['Bhandara', 'BRD'], 'Buldhana': ['Buldana', 'BD'], 'Chandrapur': ['Chandrapur', 'CD'], 'Dhule': ['Dhulia', 'DHL'], 'Gadchiroli': ['Gadchiroli', 'GCH'], 'Gondia': ['Gondia', 'G'], 'Hingoli': ['Hingoli', 'HNL'], 'Jalgaon': ['Jalgaon', 'JL'], 'Jalna': ['Jalna', 'J'], 'Kolhapur': ['Kolhapur', 'KOP'], 'Latur': ['Latur', 'LTR'], 'Mumbai City': ['Mumbai', 'BCT'], 'Mumbai Suburban': ['Mumbai', 'BCT'], 'Nagpur': ['Nagpur', 'NGP'], 'Nanded': ['Nanded', 'NED'], 'Nandurbar': ['Nandurbar', 'NDB'], 'Nashik': ['Nasik Road', 'NK'], 'Osmanabad': ['Osmanabad', 'OM'], 'Palghar': ['Palghar', 'PLG'], 'Parbhani': ['Parbhani', 'PBN'], 'Pune': ['Pune', 'PUNE'], 'Raigad': ['Panvel', 'PNVL'], 'Ratnagiri': ['Ratnagiri', 'RN'], 'Sangli': ['Sangli', 'SLI'], 'Satara': ['Satara', 'STR'], 'Sindhudurg': ['Sawantwadi Road', 'SWV'], 'Solapur': ['Solapur', 'SUR'], 'Thane': ['Thane', 'TNA'], 'Wardha': ['Wardha', 'WR'], 'Washim': ['Washim', 'WHM'], 'Yavatmal': ['Yeola', 'YL']}, 'Manipur': {'Bishnupur': ['Bishnupur', 'BPR'], 'Chandel': ['Chandel', 'HKN'], 'Churachandpur': ['Churachandpur', 'CCP'], 'Imphal East': ['Imphal', 'IMPH'], 'Imphal West': ['Imphal', 'IMPH'], 'Jiribam': ['Jiribam', 'JIRB'], 'Kakching': ['Kakching', 'KKH'], 'Kamjong': ['Kamjong', 'KKN'], 'Kangpokpi': ['Kangpokpi', 'KKI'], 'Noney': ['None', 'NNY'], 'Pherzawl': ['Pherzawl', 'PHZ'], 'Senapati': ['Senapati', 'SEN'], 'Tamenglong': ['Tamenglong', 'TML'], 'Tengnoupal': ['Tengnoupal', 'TNG'], 'Thoubal': ['Thoubal', 'THB'], 'Ukhrul': ['Ukhrul', 'UKR']}, 'Meghalaya': {'East Garo Hills': ['Williamnagar', 'WMG'], 'East Jaintia Hills': ['Khliehriat', 'KLGT'], 'East Khasi Hills': ['Shillong', 'SGUJ'], 'North Garo Hills': ['Nongstoin', 'NST'], 'Ri Bhoi': ['Nongpoh', 'NPL'], 'South Garo Hills': ['Baghmara', 'BGRA'], 'South West Garo Hills': ['Ampati', 'AXA'], 'South West Khasi Hills': ['Mawkyrwat', 'MWK'], 'West Garo Hills': ['Tura', 'TURA'], 'West Jaintia Hills': ['Jowai', 'JOW']}, 'Mizoram': {'Aizawl': ['Aizawl', 'AIZ'], 'Champhai': ['Champhai', 'CMF'], 'Hnahthial': ['Hnahthial', 'HHTL'], 'Khawzawl': ['Khawzawl', 'KAWZ'], 'Kolasib': ['Kolasib', 'KOLS'], 'Lawngtlai': ['Lawngtlai', 'LAW'], 'Lunglei': ['Lunglei', 'LUL'], 'Mamit': ['Mamit', 'MMT'], 'Saiha': ['Saiha', 'SAI'], 'Saitual': ['Saitual', 'SITL'], 'Serchhip': ['Serchhip', 'SCR']}, 'Nagaland': {'Dimapur': ['Dimapur', 'DMV'], 'Kiphire': ['Kiphire', 'KPHR'], 'Kohima': ['Kohima', 'KHMA'], 'Longleng': ['Longleng', 'LGG'], 'Mokokchung': ['Mokokchung', 'MXN'], 'Mon': ['Mon', 'MN'], 'Peren': ['Peren', 'PE'], 'Phek': ['Phek', 'PEK'], 'Tuensang': ['Tuensang', 'TUS'], 'Wokha': ['Wokha', 'WK'], 'Zunheboto': ['Zunheboto', 'ZNZ']}, 'Odisha': {'Angul': ['Angul', 'ANGL'], 'Balangir': ['Balangir', 'BLGR'], 'Balasore': ['Balasore', 'BLS'], 'Bargarh': ['Bargarh', 'BRGA'], 'Bhadrak': ['Bhadrak', 'BHC'], 'Boudh': ['Boudh', 'BOUD'], 'Cuttack': ['Cuttack', 'CTC'], 'Deogarh': ['Deogarh', 'DEG'], 'Dhenkanal': ['Dhenkanal', 'DNKL'], 'Gajapati': ['Paralakhemundi', 'PLH'], 'Ganjam': ['Berhampur', 'BAM'], 'Jagatsinghapur': ['Jagatsinghapur', 'JGDP'], 'Jajpur': ['Jajpur Keonjhar Road', 'JJKR'], 'Jharsuguda': ['Jharsuguda', 'JSG'], 'Kalahandi': ['Kalahandi', 'KRPU'], 'Kandhamal': ['Phulbani', 'PHUL'], 'Kendrapara': ['Kendrapara', 'KDJR'], 'Kendujhar': ['Kendujhar', 'KDJ'], 'Khordha': ['Bhubaneswar', 'BBS'], 'Koraput': ['Koraput', 'KRPU'], 'Malkangiri': ['Malkangiri', 'MKG'], 'Mayurbhanj': ['Baripada', 'BPO'], 'Nabarangpur': ['Nabarangpur', 'NBR'], 'Nayagarh': ['Nayagarh', 'NYG'], 'Nuapada': ['Nuapada', 'NOP'], 'Puri': ['Puri', 'PURI'], 'Rayagada': ['Rayagada', 'RGDA'], 'Sambalpur': ['Sambalpur', 'SBP'], 'Subarnapur': ['Sonepur', 'SONP'], 'Sundargarh': ['Rourkela', 'ROU']}, 'Puducherry': {'Karaikal': ['Karaikal', 'KKL'], 'Mahe': ['Mahe', 'MAHE'], 'Puducherry': ['Puducherry', 'PDY'], 'Yanam': ['Yanam', 'YNM']}, 'Punjab': {'Amritsar': ['Amritsar', 'ASR'], 'Barnala': ['Barnala', 'BNN'], 'Bathinda': ['Bhatinda', 'BTI'], 'Faridkot': ['Faridkot', 'FDK'], 'Fatehgarh Sahib': ['Sirhind-Fatehgarh', 'SIR'], 'Fazilka': ['Firozpur', 'FZP'], 'Ferozepur': ['Firozpur', 'FZR'], 'Gurdaspur': ['Gurdaspur', 'GSP'], 'Hoshiarpur': ['Hoshiarpur', 'HSX'], 'Jalandhar': ['Jalandhar Cant', 'JRC'], 'Kapurthala': ['Kapurthala', 'KRE'], 'Ludhiana': ['Ludhiana', 'LDH'], 'Mansa': ['Mansa', 'MSZ'], 'Moga': ['Moga', 'MOGA'], 'Muktsar': ['Muktsar', 'MTS'], 'Pathankot': ['Pathankot', 'PTKC'], 'Patiala': ['Patiala', 'PTA'], 'Rupnagar': ['Rupnagar', 'RPAR'], 'Sahibzada Ajit Singh Nagar': ['Mohali', 'SASN'], 'Sangrur': ['Sangrur', 'SAG'], 'Tarn Taran': ['Tarn Taran', 'TTO']}, 'Rajasthan': {'Ajmer': ['Ajmer', 'AII'], 'Alwar': ['Alwar', 'AWR'], 'Banswara': ['Banswara', 'BNL'], 'Baran': ['Baran', 'BAZ'], 'Barmer': ['Barmer', 'BME'], 'Bharatpur': ['Bharatpur', 'BTE'], 'Bhilwara': ['Bhilwara', 'BHL'], 'Bikaner': ['Bikaner', 'BKN'], 'Bundi': ['Bundi', 'BUDI'], 'Chittorgarh': ['Chittaurgarh', 'COR'], 'Churu': ['Churu', 'CUR'], 'Dausa': ['Dausa', 'DO'], 'Dholpur': ['Dholpur', 'DHO'], 'Dungarpur': ['Dungarpur', 'DNRP'], 'Hanumangarh': ['Hanumangarh', 'HMH'], 'Jaipur': ['Jaipur', 'JP'], 'Jaisalmer': ['Jaisalmer', 'JSM'], 'Jalore': ['Jalore', 'JOR'], 'Jhalawar': ['Jhalawar', 'JHW'], 'Jhunjhunu': ['Jhunjhunu', 'JJN'], 'Jodhpur': ['Jodhpur', 'JDH'], 'Karauli': ['Karauli', 'KRLI'], 'Kota': ['Kota', 'KOTA'], 'Nagaur': ['Nagaur', 'NGO'], 'Pali': ['Pali', 'PMY'], 'Pratapgarh': ['Pratapgarh', 'PDBG'], 'Rajsamand': ['Rajsamand', 'RJS'], 'Sawai Madhopur': ['Sawai Madhopur', 'SMR'], 'Sikar': ['Sikar', 'SIKR'], 'Sirohi': ['Sirohi', 'SOH'], 'Sri Ganganagar': ['Shri Ganganagar', 'SGNR'], 'Tonk': ['Tonk', 'TONK'], 'Udaipur': ['Udaipur', 'UDZ']}, 'Sikkim': {'East Sikkim': ['Gangtok', 'GTM'], 'North Sikkim': ['Mangan', 'MNG'], 'South Sikkim': ['Namchi', 'NAM'], 'West Sikkim': ['Gyalshing', 'GAS']}, 'Tamil Nadu': {'Ariyalur': ['Ariyalur', 'ALU'], 'Chengalpattu': ['Chengalpattu', 'CGL'], 'Chennai': ['Chennai Central', 'MAS'], 'Coimbatore': ['Coimbatore Jn', 'CBE'], 'Cuddalore': ['Cuddalore Port', 'CUPJ'], 'Dharmapuri': ['Dharmapuri', 'DPJ'], 'Dindigul': ['Dindigul Jn', 'DG'], 'Erode': ['Erode Jn', 'ED'], 'Kallakurichi': ['Kallakurichi', 'KLKI'], 'Kanchipuram': ['Kanchipuram', 'CJM'], 'Kanyakumari': ['Kanyakumari', 'CAPE'], 'Karur': ['Karur', 'KRR'], 'Krishnagiri': ['Krishnagiri', 'KNGR'], 'Madurai': ['Madurai Jn', 'MDU'], 'Mayiladuthurai': ['Mayiladuthurai Jn', 'MV'], 'Nagapattinam': ['Nagapattinam', 'NGT'], 'Namakkal': ['Namakkal', 'NMKL'], 'Nilgiris': ['Nilgiris', 'ONR'], 'Perambalur': ['Perambalur', 'PE'], 'Pudukkottai': ['Pudukkottai', 'PUK'], 'Ramanathapuram': ['Ramanathapuram', 'RMD'], 'Ranipet': ['Ranipet', 'RAN'], 'Salem': ['Salem Jn', 'SA'], 'Sivaganga': ['Sivaganga', 'SVGA'], 'Tenkasi': ['Tenkasi Jn', 'TSI'], 'Thanjavur': ['Thanjavur', 'TJ'], 'Theni': ['Theni', 'TEN'], 'Thoothukudi': ['Tuticorin', 'TN'], 'Tiruchirappalli': ['Tiruchchirapalli', 'TPJ'], 'Tirunelveli': ['Tirunelveli', 'TEN'], 'Tirupattur': ['Tirupattur', 'TPT'], 'Tiruppur': ['Tiruppur', 'TUP'], 'Tiruvallur': ['Tiruvallur', 'TRL'], 'Tiruvannamalai': ['Tiruvannamalai', 'TNM'], 'Vellore': ['Vellore Cant', 'VLR'], 'Viluppuram': ['Villupuram Jn', 'VM'], 'Virudhunagar': ['Virudunagar Jn', 'VPT']}, 'Telangana': {'Adilabad': ['Adilabad', 'ADB'], 'Bhadradri Kothagudem': ['Bhadrachalam Road', 'BDCR'], 'Hyderabad': ['Secunderabad Jn', 'SC'], 'Jagtial': ['Jagtial', 'JGTL'], 'Jangaon': ['Jangaon', 'ZN'], 'Jayashankar Bhupalpally': ['Bhupalpally', 'BPA'], 'Jogulamba Gadwal': ['Gadwal', 'GWD'], 'Kamareddy': ['Kamareddy', 'KMC'], 'Karimnagar': ['Karimnagar', 'KRMR'], 'Khammam': ['Khammam', 'KMT'], 'Komaram Bheem': ['Sirpur Kaghaznagar', 'SKZR'], 'Mahabubabad': ['Mahbubabad', 'MABD'], 'Mahabubnagar': ['Mahbubnagar', 'MBNR'], 'Mancherial': ['Manchiryal', 'MCI'], 'Medak': ['Medak', 'MED'], 'Medchal': ['Medchal', 'MEDC'], 'Nagarkurnool': ['Nalgonda', 'NLDA'], 'Nalgonda': ['Nalgonda', 'NLDA'], 'Nirmal': ['Nizamabad', 'NZB'], 'Nizamabad': ['Nizamabad', 'NZB'], 'Peddapalli': ['Peddapalli', 'PDPL'], 'Rajanna Sircilla': ['Siricilla', 'SIRC'], 'Rangareddy': ['Falaknuma', 'FM'], 'Sangareddy': ['Sangareddi', 'SC'], 'Siddipet': ['Siddipet', 'SPD'], 'Suryapet': ['Suryapet', 'SKZR'], 'Vikarabad': ['Vikarabad', 'VKB'], 'Wanaparthy': ['Wanparti Road', 'WPR'], 'Warangal Urban': ['Warangal', 'WL'], 'Yadadri Bhuvanagiri': ['Bhongir', 'BG']}, 'Tripura': {'Dhalai': ['Ambasa', 'ABSA'], 'Gomati': ['Udaipur', 'UCN'], 'Khowai': ['Khowai', 'KTW'], 'North Tripura': ['Dharmanagar', 'DMR'], 'Sepahijala': ['Bishramganj', 'BOP'], 'South Tripura': ['Agartala', 'AGTL'], 'Unakoti': ['Kumarghat', 'KUGT'], 'West Tripura': ['Agartala', 'AGTL']}, 'Uttar Pradesh': {'Agra': ['Agra Cantt', 'AGC'], 'Aligarh': ['Aligarh Jn', 'ALJN'], 'Ambedkar Nagar': ['Akbarpur', 'ABP'], 'Amethi': ['Amethi', 'AME'], 'Amroha': ['Amroha', 'AMRO'], 'Auraiya': ['Auraiya', 'AUA'], 'Ayodhya': ['Faizabad Jn', 'FD'], 'Azamgarh': ['Azamgarh', 'AMH'], 'Baghpat': ['Baraut', 'BTU'], 'Bahraich': ['Bahraich', 'BRK'], 'Ballia': ['Ballia', 'BUI'], 'Balrampur': ['Balrampur', 'BLP'], 'Banda': ['Banda', 'BNDA'], 'Barabanki': ['Barabanki Jn', 'BBK'], 'Bareilly': ['Bareilly', 'BE'], 'Basti': ['Basti', 'BST'], 'Bhadohi': ['Bhadohi', 'BOY'], 'Bijnor': ['Bijnor', 'BJO'], 'Budaun': ['Budaun', 'BEM'], 'Bulandshahr': ['Bulandshahr', 'BSC'], 'Chandauli': ['Chandauli Majhwar', 'CDMR'], 'Chitrakoot': ['Chitrakoot', 'CKTD'], 'Deoria': ['Deoria Sadar', 'DEOS'], 'Etah': ['Etah', 'ETAH'], 'Etawah': ['Etawah', 'ETW'], 'Farrukhabad': ['Farrukhabad', 'FBD'], 'Fatehpur': ['Fatehpur', 'FTP'], 'Firozabad': ['Firozabad', 'FZD'], 'Gautam Buddha Nagar': ['Dadri', 'DER'], 'Ghaziabad': ['Ghaziabad', 'GZB'], 'Ghazipur': ['Ghazipur City', 'GCT'], 'Gonda': ['Gonda Jn', 'GD'], 'Gorakhpur': ['Gorakhpur Jn', 'GKP'], 'Hamirpur': ['Hamirpur', 'HAR'], 'Hapur': ['Hapur', 'HPU'], 'Hardoi': ['Hardoi', 'HRI'], 'Hathras': ['Hathras Jn', 'HRS'], 'Jalaun': ['Orai', 'ORAI'], 'Jaunpur': ['Jaunpur City', 'JOP'], 'Jhansi': ['Jhansi Jn', 'JHS'], 'Kannauj': ['Kannauj', 'KJN'], 'Kanpur Dehat': ['Rura', 'RURA'], 'Kanpur Nagar': ['Kanpur Central', 'CNB'], 'Kasganj': ['Kasganj', 'KSJ'], 'Kaushambi': ['Sirathu', 'SRO'], 'Kushinagar': ['Kaptanganj Jn', 'CPJ'], 'Lakhimpur Kheri': ['Lakhimpur', 'LMP'], 'Lalitpur': ['Lalitpur', 'LAR'], 'Lucknow': ['Lucknow Ne', 'LJN'], 'Maharajganj': ['Maharajganj', 'MG'], 'Mahoba': ['Mahoba', 'MBA'], 'Mainpuri': ['Mainpuri', 'MNQ'], 'Mathura': ['Mathura Jn', 'MTJ'], 'Mau': ['Muhammadabad', 'MMA'], 'Meerut': ['Meerut City', 'MTC'], 'Mirzapur': ['Mirzapur', 'MZP'], 'Moradabad': ['Moradabad', 'MB'], 'Muzaffarnagar': ['Muzaffarnagar', 'MOZ'], 'Pilibhit': ['Pilibhit Jn', 'PBE'], 'Pratapgarh': ['Pratapgarh Jn', 'PBH'], 'Prayagraj': ['Prayagraj Jn', 'PRYJ'], 'Raebareli': ['Rae Bareli Jn', 'RBL'], 'Rampur': ['Rampur', 'RMU'], 'Saharanpur': ['Saharanpur', 'SRE'], 'Sambhal': ['Sambhal Hatim Sarai', 'SHSS'], 'Sant Kabir Nagar': ['Khalilabad', 'KLD'], 'Shahjahanpur': ['Shahjahanpur', 'SPN'], 'Shamli': ['Shamli', 'SMQL'], 'Shravasti': ['Balrampur', 'BLP'], 'Siddharthnagar': ['Bansi Paharpur', 'BSNR'], 'Sitapur': ['Sitapur', 'STP'], 'Sonbhadra': ['Chopan', 'CPU'], 'Sultanpur': ['Sultanpur Jn', 'SLN'], 'Unnao': ['Unnao Jn', 'ON'], 'Varanasi': ['Varanasi Jn', 'BSB']}, 'Uttarakhand': {'Almora': ['Almora', 'AMO'], 'Bageshwar': ['Bageshwar', 'BSZ'], 'Chamoli': ['Chamoli', 'CMN'], 'Champawat': ['Champawat', 'CPWT'], 'Dehradun': ['Dehradun', 'DDN'], 'Haridwar': ['Haridwar', 'HW'], 'Nainital': ['Kathgodam', 'KGM'], 'Pauri Garhwal': ['Kotdwara', 'KTW'], 'Pithoragarh': ['Pithoragarh', 'PGH'], 'Rudraprayag': ['Rudraprayag', 'RPY'], 'Tehri Garhwal': ['Rishikesh', 'RKSH'], 'Udham Singh Nagar': ['Rudrapur City', 'RUPC'], 'Uttarkashi': ['Uttarkashi', 'UTK']}, 'West Bengal': {'Alipurduar': ['Alipurduar Jn', 'APDJ'], 'Bankura': ['Bankura', 'BQA'], 'Birbhum': ['Bolpur Shantiniketan', 'BHP'], 'Cooch Behar': ['Cooch Behar', 'COB'], 'Dakshin Dinajpur': ['Balurghat', 'BLGT'], 'Darjeeling': ['New Jalpaiguri', 'NJP'], 'Hooghly': ['Howrah Jn', 'HWH'], 'Howrah': ['Howrah Jn', 'HWH'], 'Jalpaiguri': ['New Jalpaiguri', 'NJP'], 'Jhargram': ['Jhargram', 'JGM'], 'Kalimpong': ['New Jalpaiguri', 'NJP'], 'Kolkata': ['Sealdah', 'SDAH'], 'Malda': ['Malda Town', 'MLDT'], 'Murshidabad': ['Lalgola', 'LGL'], 'Nadia': ['Krishnanagar City', 'KNJ'], 'North 24 Parganas': ['Sealdah', 'SDAH'], 'Paschim Bardhaman': ['Asansol Jn', 'ASN'], 'Paschim Medinipur': ['Medinipur', 'MDN'], 'Purba Bardhaman': ['Barddhaman Jn', 'BWN'], 'Purba Medinipur': ['Haldia', 'HLZ'], 'Purulia': ['Purulia Jn', 'PRR'], 'South 24 Parganas': ['Sealdah', 'SDAH'], 'Uttar Dinajpur': ['Malda Town', 'MLDT']}}
railway_stations = {"Andhra Pradesh": ["VSKP", "NHLN"],"Arunachal Pradesh": ["GHY"],"Assam": ["GHY"],"Bihar": ["PNBE", "R"],"Chhattisgarh": ["R"],"Goa": ["MAO"],"Gujarat": ["ADI", "UMB"],"Haryana": ["UMB"],"Himachal Pradesh": ["SML"],"Jammu and Kashmir": ["UMB"],"Jharkhand": ["RNC"],"Karnataka": ["SBC"],"Kerala": ["TVC"],"Madhya Pradesh": ["BPL"],"Maharashtra": ["BCT", "JRM", "MPR"],"Manipur": ["GHY"],"Meghalaya": ["GHY"],"Mizoram": ["GHY"],"Nagaland": ["GHY"],"Odisha": ["BRBI", "DMV", "BBS"],"Punjab": ["ASR", "JP"],"Rajasthan": ["UMB"],"Sikkim": ["NJP"],"Tamil Nadu": ["MAS", "MS"],"Telangana": ["SC"],"Tripura": ["AGTL"],"Uttar Pradesh": ["LJN"],"Uttarakhand": ["DVN"],"West Bengal": ["HWH"]}

def check(start_state, end_state, start_station, end_station, date, way, time_filter):
            d = {}
            tok, x1 = train_access.get_train_details(start_station, end_station, date, 1, time_filter)
            if tok == 1:
                if x1:
                    k = list(x1.keys())[0]
                    d[f'{x1[k]['from']} --> {x1[k]['to']}'] = x1
                    return d
            else:
                for a in x1:
                    tok, x2 = train_access.get_train_details(start_station, a, date, 1, time_filter)
                    if tok == 1:
                        if x2:
                            k = list(x2.keys())[0]
                            d[f'{x2[k]['from']} --> {x2[k]['to']}'] = x2
                            return d

            alter_start = railway_stations[start_state]
            for i in alter_start:
                tok, y1 = train_access.get_train_details(i, end_station, date, way, time_filter)
                if tok == 1:
                    if y1:
                        k = list(y1.keys())[0]
                        d[f"{y1[k]['from']} --> {y1[k]['to']}"] = y1
                        return d
                else:
                    for a in y1:
                        tok, y2 = train_access.get_train_details(i, a, date, 1, time_filter)
                        if tok == 1:
                            if y2:
                                k = list(y2.keys())[0]
                                d[f'{y2[k]['from']} --> {y2[k]['to']}'] = y2
                                return d
            alter_end = railway_stations[end_state]
            for k in alter_end:
                tok, v1 = train_access.get_train_details(start_station, k, date, way, time_filter)
                if tok == 1:
                    if v1:
                        k = list(v1.keys())[0]
                        d[f"{v1[k]['from']} --> {v1[k]['to']}"] = v1
                        return d
                else:
                    for a in v1:
                        tok, v2 = train_access.get_train_details(start_station, k, date, 1, time_filter)
                        if tok == 1:
                            if v2:
                                k = list(v2.keys())[0]
                                d[f'{v2[k]['from']} --> {v2[k]['to']}'] = v2
                                return d

            alter_end = railway_stations[end_state]
            for j in alter_end:
                tok, z1 = train_access.get_train_details(i, j, date, way, time_filter)
                if tok == 1:
                    if z1:
                        k = list(z1.keys())[0]
                        d[f"{z1[k]['from']} --> {z1[k]['to']}"] = z1
                        return d
                else:
                    for a in z1:
                        tok, z2 = train_access.get_train_details(i, a, date, 1, time_filter)
                        if tok == 1:
                            if z2:
                                k = list(z2.keys())[0]
                                d[f'{z2[k]['from']} --> {z2[k]['to']}'] = z2
                                return d
            return None

def login_to_main(root, frame1, canvas, uid, rid):
    
    
    #main window creation----------------------------------------
    
    
    frame1.destroy()
    canvas.destroy()
    root.state("zoomed")
    
    label = Label(root, text="TravelEasy", font=("Stencil", 25), bg="grey", width=205, height=3)
    label.pack()
    
    notebook = ttk.Notebook(root)

    tab1 = Frame(notebook)
    tab2 = Frame(notebook)
    tab3 = Frame(notebook)
    tab4 = Frame(notebook)
    tab5 = Frame(notebook)
    tab6 = Frame(notebook)

    country_label = Label(tab2, text="India", font=("Constantia", 15)).pack()

    notebook.add(tab1, text="HOME")
    notebook.add(tab2, text="PACKAGES")
    notebook.add(tab3, text="BOOKING")
    notebook.add(tab4, text="BOOKING DETAILS")
    notebook.add(tab6, text="ABOUT US")
    notebook.add(tab5, text="CONTACT")
    notebook.pack(fill=BOTH, expand=True)

    tab_display.tab1_page(tab1)
    tab_display.tab2_page(tab2)
    tab_display.tab6_page(tab6)
    tab_display.tab5_page(tab5)

    
    
    #transport -----------------------------------------------------
    
    def show_transport(display, bid, dict_store):
        messagebox.showinfo("Please wait!","Fetching Transport data.")
        hn = []
        hp = []
        for n, p in dict_store.values():
            hn.append(n)
            hp.append(str(p))
        cu.execute("UPDATE booking_records SET hotel_name=? WHERE bid=?", ("|".join(hn), bid))
        connb.commit()
        cu.execute("UPDATE booking_records SET hotel_price=? WHERE bid=?", ("|".join(hp), bid))
        connb.commit()
        cu.execute("SELECT * FROM booking_records")
        print(cu.fetchall())


        cu.execute("SELECT mode FROM booking_details WHERE booking_id=?", (bid,))
        mode_of_transport = cu.fetchone()[0]
        

        def car_clicked(i, price):
            print("Car Confirmed", i)
            cu.execute("UPDATE booking_records SET pt=? WHERE bid=?", (i, bid))
            cu.execute("UPDATE booking_records SET transport_price=? WHERE bid=?", (price, bid))
            connb.commit()
            cu.execute("SELECT * FROM booking_records")
            print(cu.fetchall())            
            display5.pack_forget()
            root.update()
            display1.pack()
            root.update()
            tab_display.booking_details(bid,tab4)
            messagebox.showinfo("Booking successful!","Booking details sent to registered email.")
            notebook.select(tab4)
        # if mode=='pvt.transport' ----------------------------------------------------
        
        if mode_of_transport == '0':
            display.pack_forget()
            root.update()
            display5 = Frame(tab3)
            display5.pack(fill=BOTH, expand=True)

            label_cars = Label(display5, text="Cars", font=("Arial", 20, "bold"), height=2)
            label_cars.pack()

            def vehicle_price(days, people, start_dest_district, end_dest_district, dest_state):
                vehicle_details = {
                    4: {"Maruti Suzuki Swift": 0.97,"Tata Altroz": 1.09,"Honda City": 1.20,"Maruti Suzuki Dzire": 1.17,"Tata Nexon": 1.15,"Maruti Suzuki Vitara Brezza": 1.16},
                    6: {"Maruti Suzuki Ertiga": 1.06,"Toyota Innova Crysta": 1.14,"Mahindra Marazzo": 1.10,"Renault Triber": 0.94,"Mahindra XUV500": 1.11,"MG Hector Plus": 1.18},
                    8: {"Toyota Innova Crysta": 1.20,"Mahindra Marazzo": 1.16,"Mahindra Scorpio": 1.09,"Mahindra Xylo": 1.10,"Kia Carnival": 1.20},
                    10: {"Force Traveller": 1.17,"Tata Winger": 1.12,"Mahindra Supro": 1.08},
                    20: {"Force Traveller 3050": 1.13,"Ashok Leyland Stile": 1.09},
                    30: {"Ashok Leyland Cheetah": 1.15,"Tata Starbus": 1.04},
                    40: {"Ashok Leyland Viking": 1.20,"Tata LPO 1618": 1.18},
                    50: {"Volvo B9R": 1.20,"Mercedes-Benz Super High Deck": 1.20,"Scania Metrolink HD": 1.20}
                }

                vehicle_costs = {4: (1800, 15), 6: (3200, 18), 8: (4500, 22), 10: (7500, 25), 20: (10500, 28),30: (14500, 33), 40: (28000, 36), 50: (38300, 39)}

                start_destination_address = start_dest_district + ' ' + dest_state + ' ' + ' India'
                destination_location_from = location_access.address_to_lat_long(start_destination_address)
                
                cu.execute("SELECT city,state FROM booking_details WHERE booking_id=?",(bid,))
                list_start=cu.fetchall()[0]
                
                start_loc=list_start[0]+' '+list_start[1]
                current_location = location_access.address_to_lat_long(start_loc)
                
                if not destination_location_from:
                    print(f"Unable to fetch the destination location {start_destination_address} please enter correct location")
                elif not current_location:
                    print(f"Unable to fetch your location {current_location}")
                else:
                    distance_from = geodesic(current_location, destination_location_from).km
                    print("from:", distance_from)

                end_destination_address = end_dest_district + ' ' + dest_state + ' ' + ' India'
                destination_location_to = location_access.address_to_lat_long(end_destination_address)
                
                if not destination_location_to:
                    print(f"Unable to fetch the destination location {end_destination_address} please enter correct location")
                elif not current_location:
                    print(f"Unable to fetch your location {current_location}")
                else:
                    distance_to = geodesic(current_location, destination_location_to).km
                    print("to:", distance_to)

                def calc_vehicle_price(distance_from, distance_to, days):
                    travel_cost = 0
                    transport_list = []
                    if people > 0 and people <= 4:
                        for k, v in vehicle_details[4].items():
                            travel_cost = vehicle_costs[4][1] * distance_from + ((vehicle_costs[4][0] * days) * v) + \
                                          vehicle_costs[4][1] * distance_to
                            travel_cost = f"{travel_cost:.2f}"
                            transport_list.append((k, travel_cost))
                    elif people > 4 and people <= 6:
                        for k, v in vehicle_details[6].items():
                            travel_cost = round(
                                vehicle_costs[6][1] * distance_from + ((vehicle_costs[6][0] * days) * v) +
                                vehicle_costs[6][1] * distance_to, 2)
                            transport_list.append((k, travel_cost))

                    elif people > 6 and people <= 8:
                        for k, v in vehicle_details[8].items():
                            travel_cost = round(
                                vehicle_costs[8][1] * distance_from + ((vehicle_costs[8][0] * days) * v) +
                                vehicle_costs[8][1] * distance_to, 2)
                            transport_list.append((k, travel_cost))

                    elif people > 8 and people <= 10:
                        for k, v in vehicle_details[10].items():
                            travel_cost = round(
                                vehicle_costs[10][1] * distance_from + ((vehicle_costs[10][0] * days) * v) +
                                vehicle_costs[10][1] * distance_to, 2)
                            transport_list.append((k, travel_cost))

                    elif people > 10 and people <= 20:
                        for k, v in vehicle_details[20].items():
                            travel_cost = round(
                                vehicle_costs[20][1] * distance_from + ((vehicle_costs[20][0] * days) * v) +
                                vehicle_costs[20][1] * distance_to, 2)
                            transport_list.append((k, travel_cost))

                    elif people > 20 and people <= 30:
                        for k, v in vehicle_details[30].items():
                            travel_cost = round(
                                vehicle_costs[30][1] * distance_from + ((vehicle_costs[30][0] * days) * v) +
                                vehicle_costs[30][1] * distance_to, 2)
                            transport_list.append((k, travel_cost))

                    elif people > 30 and people <= 40:
                        for k, v in vehicle_details[40].items():
                            travel_cost = round(
                                vehicle_costs[40][1] * distance_from + ((vehicle_costs[40][0] * days) * v) +
                                vehicle_costs[40][1] * distance_to, 2)
                            transport_list.append((k, travel_cost))

                    elif people > 40 and people <= 50:
                        for k, v in vehicle_details[50].items():
                            travel_cost = round(
                                vehicle_costs[50][1] * distance_from + ((vehicle_costs[50][0] * days) * v) +
                                vehicle_costs[50][1] * distance_to, 2)
                            transport_list.append((k, travel_cost))
                    return transport_list

                return calc_vehicle_price(distance_from, distance_to, days)

            cu.execute("SELECT days,people FROM booking_details WHERE booking_id=?", (bid,))
            x = cu.fetchall()[0]
            
            days, people = x[0], x[1]
            days, people = int(days), int(people)
            
            cu.execute("SELECT places FROM booking_records WHERE bid=?", (bid,))
            places = list((cu.fetchone()[0]).split('|'))
            
            start_dest_district = places[0]
            end_dest_district = places[len(places) - 1]
            
            cu.execute("SELECT state_name FROM booking_records WHERE bid=?", (bid,))
            dest_state = cu.fetchone()[0]
            
            transport_list = vehicle_price(days, people, start_dest_district, end_dest_district, dest_state)

            for i in range(len(transport_list)):
                car_frame = Frame(display5, bd=1, relief="solid", height=10, bg="lightgrey")
                car_frame.pack(fill="x", padx=5, pady=2)

                car_label = Label(car_frame, text=transport_list[i][0], font=("Arial", 15, "bold"), height=5,anchor='w', width=30)
                car_label.pack(side="left", padx=30)

                car_label = Label(car_frame, text=f"Price:{transport_list[i][1]}", font=("Arial", 15), height=5,anchor='w', width=30)
                car_label.pack(side="left", padx=30)

                confirm_button = Button(car_frame, text="Confirm", bg="lightblue", font=("Arial", 14), width=25,command=lambda i=i: car_clicked(transport_list[i][0], transport_list[i][1]))
                confirm_button.pack(pady=20, side=RIGHT, padx=30)

        # if mode==train ---------------------------------------------
        
        elif mode_of_transport == '1':
            cu.execute("SELECT places FROM booking_records WHERE bid=?", (bid,))
            places = list((cu.fetchone()[0]).split('|'))
            
            cu.execute("SELECT state,city,destination FROM booking_details WHERE booking_id=?", (bid,))
            start_det = (cu.fetchall()[0])
            
            cu.execute("SELECT days FROM booking_details WHERE booking_id=?", (bid,))
            days = cu.fetchone()[0]
            
            cu.execute("SELECT date FROM booking_details WHERE booking_id=?", (bid,))
            date_start = (cu.fetchone()[0])
            
            start_date = convert_rr_format_to_dmy(date_start)

            end_date = nth_date(start_date, int(days))

            end_dest_district = places[len(places) - 1]
            start_dest_district = places[0]

            start_state = start_det[0]
            start_district = start_det[1]

            end_state = start_det[2]
            
            start_station = India[start_state][start_district][1]
            end_station = India[end_state][start_dest_district][1]
            
            time_filter = datetime.strptime('08:00', '%H:%M')
            d_train = {}
            
            d_train['1'] = (check(start_state, end_state, start_station, end_station, start_date, 1, time_filter))
            
            time_filter = datetime.strptime('17:00', '%H:%M')
            start_station = India[start_state][start_district]
            end_station = India[end_state][end_dest_district]
            
            d_train['-1'] = (check(end_state, start_state, end_station, start_station, end_date, -1, time_filter))

            if d_train['1'] == None:
                desc = messagebox.askyesno("No train found", "Do you want to book car/bus?")
                if desc:
                    cu.execute("UPDATE booking_details SET mode=? WHERE booking_id=?", ('0', bid))
                    show_transport(display, bid)

                else:
                    display.pack_forget()
                    root.update()
                    display1.pack()
                    root.update()
                return
            elif d_train['-1'] == None:
                desc = messagebox.askyesno("No train found", "Do you want to book car/bus?")
                if desc:
                    cu.execute("UPDATE booking_details SET mode=? WHERE booking_id=?", ('0', bid))
                    show_transport(display, bid)

                else:
                    display.pack_forget()
                    root.update()
                    display1.pack()
                    root.update()
                return

            def confirm_train_final(train_from, train_to, cls_to, arg_from,display):
                cu.execute("SELECT days,people FROM booking_details WHERE booking_id=?", (bid,))
                x = cu.fetchall()[0]
                days, people = x[0], x[1]
                days, people = int(days), int(people)
                if arg_from.get():
                    if train_to:
                        train_det_to = ('|'.join(
                            [train_to['train_name'], train_to['date'], train_to['from_time'], train_to['to_time'],
                             cls_to[0]]))
                        price_to = cls_to[1]
                    if train_from:
                        list_class_from = []
                        for k, v in train_from['available_class'].items():
                            list_class_from.append((k, v))
                        cls_from = list_class_from[arg_from.get()]
                        train_det_from = ('|'.join(
                            [train_from['train_name'], train_from['date'], train_from['from_time'],
                             train_from['to_time'], cls_from[0]]))
                        price_from = cls_from[1]
                    cu.execute("SELECT * FROM booking_records WHERE bid=?", (bid,))
                    print(cu.fetchall())
                    train_text = ('$'.join([train_det_to, train_det_from]))
                    tot_train_price = (price_to + price_from) * people
                    cu.execute('UPDATE booking_records SET train=? WHERE bid=?', (train_text, bid))
                    connb.commit()
                    cu.execute('UPDATE booking_records SET transport_price=? WHERE bid=?', (tot_train_price, bid))
                    connb.commit()
                    cu.execute("SELECT * FROM booking_records WHERE bid=?", (bid,))
                    print(cu.fetchall())
                    print(tot_train_price)

                    messagebox.showinfo("Train Booked", "Booking successful!")
                    display.pack_forget()
                    root.update()
                    display1.pack()
                    root.update()
                    tab_display.booking_details(bid,tab4)
                    messagebox.showinfo("Booking successful!","Booking details sent to registered email.")
                    notebook.select(tab4)
                else:
                    messagebox.showerror('Input error!', "Choose a class!")
                    return

            def show_train_details_from(train_to, cls_to, display):
                display.pack_forget()
                root.update()
                display7 = Frame(tab3)
                display7.pack()
                radio_var_back = IntVar()
                for k, v in d_train['-1'].items():
                    label_from_back = Label(display7, text=f"{k}", font=("Arial", 15), height=2)
                    label_from_back.pack()
                    for key, value in v.items():
                        train_frame_back = Frame(display7, bd=1, relief="solid", height=10, bg="lightgrey")
                        train_frame_back.pack(fill="x", padx=5, pady=2)

                        train_number_back = Label(train_frame_back, text=f"{key}", font=("Arial", 15, "bold"),
                                                  anchor='w', width=10)
                        train_number_back.pack(side="left", padx=30)

                        train_name_back = Label(train_frame_back, text=f"{value['train_name']}", font=("Arial", 15),
                                                anchor='w', width=40)
                        train_name_back.pack(side="left", padx=30)

                        train_date_back = Label(train_frame_back, text=f"{value['date']}", font=("Arial", 15),
                                                anchor='w', width=10)
                        train_date_back.pack(side="right", padx=90)

                        train_from_time_back = Label(train_frame_back, text=f"{value['from_time']}", font=("Arial", 15),
                                                     anchor='w', width=5)
                        train_from_time_back.pack(side="right", padx=60)

                        train_to_time_back = Label(train_frame_back, text=f"{value['to_time']}", font=("Arial", 15),
                                                   anchor='w', width=5)
                        train_to_time_back.pack(side="right", padx=30)

                        radio_frame_back = Frame(train_frame_back)
                        radio_frame_back.pack()
                        list_train_radio_back = []
                        for cls, prc in value['available_class'].items():
                            list_train_radio_back.append(f"{cls}:{prc}")
                        for j, text in enumerate(list_train_radio_back):
                            radio_button_back = Radiobutton(radio_frame_back, text=text, variable=radio_var_back,
                                                            value=j, font=("Arial", 15), bd=1, relief="solid")
                            radio_button_back.pack(side="left")

                        confirm_button_back = Button(train_frame_back, text="Confirm",
                                                     command=lambda v=value: confirm_train_final(v, train_to, cls_to,
                                                                                                 radio_var_back,display7),
                                                     bg="lightblue", font=("Arial", 12), width=20)
                        confirm_button_back.pack(pady=20, padx=30)

            radio_var_front = IntVar()

            def confirm_to(train_to, arg, display):
                if arg.get():
                    if train_to:
                        list_class_to = []
                        for k, v in train_to['available_class'].items():
                            list_class_to.append((k, v))
                    else:
                        messagebox.showerror('Input error!', "Choose a class!")
                        return

                    show_train_details_from(train_to, list_class_to[arg.get()], display)

            def show_train_details_to(display):
                display.forget()
                root.update()
                display6 = Frame(tab3)
                display6.pack(fill=BOTH, expand=True)
                label_train = Label(display6, text="Trains", font=("Arial", 20, "bold"), height=2)
                label_train.pack()

                for k, v in d_train['1'].items():
                    label_from_front = Label(display6, text=f"{k}", font=("Arial", 15), height=2)
                    label_from_front.pack()
                    count = 0
                    for key, value in v.items():
                        count += 1
                        train_frame_front = Frame(display6, bd=1, relief="solid", height=10, bg="lightgrey")
                        train_frame_front.pack(fill="x", padx=5, pady=2)

                        train_number_front = Label(train_frame_front, text=f"{key}", font=("Arial", 15, "bold"),
                                                   anchor='w', width=10)
                        train_number_front.pack(side="left", padx=30)

                        train_name_front = Label(train_frame_front, text=f"{value['train_name']}", font=("Arial", 15),
                                                 anchor='w', width=40)
                        train_name_front.pack(side="left", padx=30)

                        train_date_front = Label(train_frame_front, text=f"{value['date']}", font=("Arial", 15),
                                                 anchor='w', width=10)
                        train_date_front.pack(side="right", padx=90)

                        train_from_time_front = Label(train_frame_front, text=f"{value['from_time']}",
                                                      font=("Arial", 15), anchor='w', width=5)
                        train_from_time_front.pack(side="right", padx=60)

                        train_to_time_front = Label(train_frame_front, text=f"{value['to_time']}", font=("Arial", 15),
                                                    anchor='w', width=5)
                        train_to_time_front.pack(side="right", padx=30)

                        radio_frame_front = Frame(train_frame_front)
                        radio_frame_front.pack()
                        list_train_radio_front = []
                        for cls, prc in value['available_class'].items():
                            list_train_radio_front.append(f"{cls}:{prc}")

                        for j, text in enumerate(list_train_radio_front):
                            radio_button_front = Radiobutton(radio_frame_front, text=text, variable=radio_var_front,
                                                             value=j, font=("Arial", 15), bd=1, relief="solid")
                            radio_button_front.pack(side="left")
                        print(radio_var_front)
                        arg = radio_var_front
                        confirm_button_front = Button(train_frame_front, text="Confirm",
                                                      command=lambda v=value: confirm_to(v, arg, display6),
                                                      bg="lightblue", font=("Arial", 12), width=20)
                        confirm_button_front.pack(pady=20, padx=30)

            show_train_details_to(display)

    # show hotel -----------------------------------------------------------------
    
    
    def show_hotels(display3, l_final, m, bid):
        messagebox.showinfo("Please wait!","Fetching Hotels data.")
        d = {}
        
        display3.pack_forget()
        root.update()
        display4 = Frame(tab3)
        display4.pack(fill=BOTH, expand=True)
        
        conn = sqlite3.connect("places_details.db")
        c = conn.cursor()
        
        dict_store = {}
        
        for i in range(1, len(l_final) + 1):
            dict_store[f"Day{i}"] = None

        def view_hotel_check(display4, bid, d):
            
            show_transport(display4, bid, dict_store)

        def toggle_details(details_label):
            if details_label.winfo_viewable():
                details_label.pack_forget()
            else:
                details_label.pack(fill="x", padx=5, pady=5)

        def create_day_section(display4, day, details):
            hotel_frame = Frame(display4, bd=1, relief="solid", height=12)
            hotel_frame.pack(fill="x", padx=5, pady=2)
            day_label = Label(hotel_frame, text=day, font=("Arial", 15, "bold"), height=5, anchor='w', width=50)
            day_label.pack(side="left", padx=10)
            selected = StringVar()

            def radio_button_command(place, d):
                l = []
                for key, value in d.items():
                    l.append(value)
                for i in range(len(l)):
                    for j in l[i]:
                        if j[0] == place:
                            dict_store[f'Day{i + 1}'] = j

            for i, (place, score) in enumerate(details):
                radio_button = Radiobutton(hotel_frame, text=f"{place}      {score}", font=("Arial", 15),
                                           variable=selected, value=place,
                                           command=lambda place=place: radio_button_command(place, d))
                radio_button.pack(anchor=W)
                radio_button.config(takefocus=0)

        label_package = Label(display4, text=f"HOTELS", font=("Arial", 25, "bold"))
        label_package.pack()
        hotel_final = []
        for district in l_final:
            c.execute("SELECT state_name FROM states WHERE state_id=?", (m,))
            state_name = c.fetchone()[0]
            address = district + ' ' + state_name + ' India'

            def call():
                x, y = location_access.address_to_lat_long(address)
                r = 1500
                flag = 0
                t = 1
                while flag == 0:
                    tok, max_dist, d = hotel_access.find_nearest_hotels(r, x, y)
                    if tok == 1 and len(d) > 3:
                        if d:
                            flag = 1
                    else:
                        r += 1000
                    if r > 75000:
                        t = 0
                        break
                return t, d, max_dist

            def price_calc():
                t, hotel_d, max_dist = call()
                l = []
                base_price = 398.34
                if t:
                    for k, v in hotel_d.items():
                        price = ((max_dist / v) * base_price)
                        price=round(price,2)
                        if price > 5000:
                            price = 5000
                        l.append((k, price))
                    return l
                else:
                    print('No hotels found')
                    messagebox.showerror("Error Occured", "No Hotels Found!")
                    display4.pack_forget()
                    root.update()
                    display1.pack()
                    root.update()
                    
                    return None

            hotel_final.append(price_calc())


        for i in range(len(hotel_final)):
            d[f"Day {i + 1} : {l_final[i]}"] = hotel_final[i]
            
        for day, details in d.items():
            create_day_section(display4, day, details)
            
        confirm_button = Button(display4, text="Confirm", bg="lightblue", font=("Arial", 14), width=25,
                                command=lambda: view_hotel_check(display4, bid, d))
        confirm_button.pack(pady=20)

    def view_details_submit_check(display3, l_final, m, bid, state_name):
        cu.executemany("INSERT INTO booking_records VALUES(?,?,?,?,?,?,?,?)", [(bid, "", "", "", "", "", "", "")])
        cu.execute("UPDATE booking_records SET places=? WHERE bid=?", ("|".join(l_final), bid))
        cu.execute("UPDATE booking_records SET state_name=? WHERE bid=?", (state_name, bid))
        cu.execute("SELECT * FROM booking_records")
        
        show_hotels(display3, l_final, m, bid)
    
    
    # package displayer -----------------------------------------------------------
    
    
    def show_package(bid):
        display1.pack_forget()
        root.update()
        display2 = Frame(tab3)
        display2.pack(fill=BOTH, expand=True)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def view_details(p_no, l_final, m, l):
            display2.pack_forget()
            root.update()
            display3 = Frame(tab3)
            display3.pack(fill=BOTH, expand=True)

            def toggle_details(details_label):
                if details_label.winfo_viewable():
                    details_label.pack_forget()
                else:
                    details_label.pack(fill="x", padx=5, pady=5)

            def create_day_section(display3, day, details):
                day_frame = Frame(display3, bd=1, relief="solid", height=12, bg="lightgrey")
                day_frame.pack(fill="x", padx=5, pady=2)

                day_label = Label(day_frame, text=day, font=("Arial", 15, "bold"), height=5, anchor='w', width=50)
                day_label.pack(side="left", padx=10)

                details_label = Label(day_frame, text=details, font=("Arial", 14), wraplength=350, justify="left",
                                      anchor='w')
                details_label.pack(padx=5, pady=5)
                details_label.pack_forget()

                toggle_button = Button(day_frame, text="View Places", command=lambda: toggle_details(details_label),
                                       bg="lightblue", font=("Arial", 14), width=12)
                toggle_button.pack(side="right", padx=10)

            label_package = Label(display3, text=f"Package Number: {p_no}", font=("Arial", 25, "bold"))
            label_package.pack()

            label_view_space = Label(display3)
            label_view_space.pack()

            c.execute("SELECT state_name FROM states WHERE state_id=?", (m,))
            state_name = c.fetchone()[0]
            label_view_state = Label(display3, text=f"State:{state_name}", font=("Arial", 18, "bold"))
            label_view_state.pack(padx=0, pady=0)

            d = {}
            
            for i in range(len(l_final)):
                c.execute("SELECT district_id FROM districts WHERE district_name=?", (l_final[i],))
                dist_id = c.fetchone()[0]

                c.execute("SELECT place_name FROM places WHERE district_id=? AND state_id=?", (dist_id, m))
                places_lis = c.fetchall()
                places_lis = list(map(lambda x: x[0], places_lis))
                for j in range(len(places_lis)):
                    places_lis[j] = str(j + 1) + '.' + places_lis[j]
                x = '\n'.join(places_lis)
                d[f"Day {i + 1} : {l_final[i]}"] = x

            for day, details in d.items():
                create_day_section(display3, day, details)

            confirm_button = Button(display3, text="Confirm", bg="lightblue", font=("Arial", 14), width=25,
                                    command=lambda: view_details_submit_check(display3, l_final, m, bid, state_name))
            confirm_button.pack(pady=20)

        cu.execute("SELECT destination FROM booking_details WHERE booking_id=?", (bid,))
        x = cu.fetchone()[0]
        print(x)
        c.execute("SELECT state_id from states  WHERE state_name=?", (x,))
        m = c.fetchone()[0]
        cu.execute("SELECT days FROM booking_details")
        n_temp = cu.fetchall()
        n = n_temp[len(n_temp) - 1][0]
        n = int(n)
        c.execute("SELECT * FROM places WHERE state_id=?", (m,))
        l = c.fetchall()
        
        d = {}
        for i in l:
            if i[3] == "must":
                if i[2] in d:
                    d[i[2]] += 1
                else:
                    d[i[2]] = 1
        s = list(sorted(d.items(), key=lambda x: x[1], reverse=True))
        print(s)

        for i in range(n):
            l_new = list(filter(lambda x: x[2] == s[i][0], l))
            print()
            for j in l_new:
                print("Place:", j[1])

        sorted_dis = [s[i][0] for i in range(n)]

        dis_list = []
        for i in sorted_dis:
            c.execute("SELECT district_name FROM districts WHERE district_id=? AND state_id=?", (i, m))
            dis_list.append(c.fetchone()[0])

        c.execute("SELECT district_name FROM districts WHERE state_id=?", (m,))
        l_get_dist = (c.fetchall())
        list_dist = list(map(lambda x: x[0], l_get_dist))
        
        l_group = []
        l_final = []
        i = 0
        while i < len(list_dist):
            l_group.append(list_dist[i])
            if len(l_group) % n == 0:
                l_final.append(l_group)
                l_group = []
            i += 1
        shuffled = random.shuffle(l_final)
        dis_list = ([list(dis_list)])
        l_final = ((dis_list) + (l_final))

        canvas = Canvas(display2)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(display2, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        frame.bind("<Configure>", on_frame_configure)

        for i in range(len(l_final)):
            box = Frame(frame, relief=RIDGE, borderwidth=5)
            box.pack(fill=BOTH, padx=5, pady=20)

            button = Button(box, text="View Details", command=lambda i=i: view_details(i + 1, l_final[i], m, l),
                            width=25, bg="light blue", borderwidth=3)

            button.pack(side=RIGHT, pady=5, padx=30)
            if i == 0:
                label = Label(box, font=("Constantia", 15),
                              text=f"Recommended Package *: {i + 1}:"
                                   f"{' ' + ','.join(l_final[i])} ", width=98,
                              height=5, anchor='w')
                label.pack(side=LEFT, pady=5, padx=30)
            else:
                label = Label(box, font=("Constantia", 15), text=f"Package {i + 1}:"
                                                                 f"{' ' + ','.join(l_final[i])}",
                              width=98,
                              height=5, anchor='w')
                label.pack(side=LEFT, pady=5, padx=30)

    
    #booking page validator functions --------------------------------------------------
    
    def email_checker(email):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return 1
        return 0

    districts_in_states = {
        'Andhra Pradesh': ['Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Krishna', 'Kurnool', 'Prakasam','Srikakulam', 'Sri Potti Sriramulu Nellore', 'Visakhapatnam', 'Vizianagaram','West Godavari', 'YSR Kadapa'],
        'Arunachal Pradesh': ['Tawang', 'West Kameng', 'East Kameng', 'Papum Pare', 'Kurung Kumey', 'Kra Daadi','Lower Subansiri', 'Upper Subansiri', 'West Siang', 'East Siang', 'Siang', 'Upper Siang','Lower Siang', 'Dibang Valley', 'Lower Dibang Valley', 'Anjaw', 'Lohit', 'Namsai','Changlang', 'Tirap', 'Longding'],
        'Assam': ['Baksa', 'Barpeta', 'Biswanath', 'Bongaigaon', 'Cachar', 'Charaideo', 'Chirang', 'Darrang', 'Dhemaji','Dhubri', 'Dibrugarh', 'Dima Hasao', 'Goalpara', 'Golaghat', 'Hailakandi', 'Hojai', 'Jorhat','Kamrup Metropolitan', 'Kamrup', 'Karbi Anglong', 'Karimganj', 'Kokrajhar', 'Lakhimpur', 'Majuli','Morigaon', 'Nagaon', 'Nalbari', 'Dima Hasao', 'Sivasagar', 'Sonitpur', 'South Salmara-Mankachar','Tinsukia', 'Udalguri', 'West Karbi Anglong'],
        'Bihar': ['Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur', 'Bhojpur', 'Buxar', 'Darbhanga','East Champaran', 'Gaya', 'Gopalganj', 'Jamui', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria','Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nalanda', 'Nawada','Patna', 'Purnia', 'Rohtas', 'Saharsa', 'Samastipur', 'Saran', 'Sheikhpura', 'Sheohar', 'Sitamarhi','Siwan', 'Supaul', 'Vaishali', 'West Champaran'],
'Chhattisgarh': ['Balod', 'Baloda Bazar', 'Balrampur', 'Bastar', 'Bemetara', 'Bijapur', 'Bilaspur', 'Dantewada','Dhamtari', 'Durg', 'Gariaband', 'Janjgir-Champa', 'Jashpur', 'Kabirdham', 'Kanker','Kondagaon', 'Korba', 'Koriya', 'Mahasamund', 'Mungeli', 'Narayanpur', 'Raigarh', 'Raipur','Rajnandgaon', 'Sukma', 'Surajpur', 'Surguja'],
        'Goa': ['North Goa', 'South Goa'],
        'Gujarat': ['Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar', 'Botad','Chhota Udaipur', 'Dahod', 'Dang', 'Devbhoomi Dwarka', 'Gandhinagar', 'Gir Somnath', 'Jamnagar','Junagadh', 'Kutch', 'Kheda', 'Mahisagar', 'Mehsana', 'Morbi', 'Narmada', 'Navsari', 'Panchmahal','Patan', 'Porbandar', 'Rajkot', 'Sabarkantha', 'Surat', 'Surendranagar', 'Tapi', 'Vadodara','Valsad'],
        'Haryana': ['Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurugram', 'Hisar', 'Jhajjar','Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 'Nuh', 'Palwal', 'Panchkula', 'Panipat','Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamunanagar'],
        'Himachal Pradesh': ['Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu', 'Lahaul and Spiti','Mandi', 'Shimla', 'Sirmaur', 'Solan', 'Una'],
        'Jharkhand': ['Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum', 'Garhwa', 'Giridih', 'Godda','Gumla', 'Hazaribagh', 'Jamtara', 'Khunti', 'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu','Ramgarh', 'Ranchi', 'Sahebganj', 'Seraikela-Kharsawan', 'Simdega', 'West Singhbhum'],
        'Karnataka': ['Bagalkot', 'Ballari', 'Belagavi', 'Bengaluru Rural', 'Bengaluru Urban', 'Bidar','Chamarajanagar', 'Chikballapur', 'Chikkamagaluru', 'Chitradurga', 'Dakshina Kannada','Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi', 'Kodagu', 'Kolar', 'Koppal','Mandya', 'Mysuru', 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada','Vijayapura', 'Yadgir'],
        'Kerala': ['Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 'Kozhikode','Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'],
        'Madhya Pradesh': ['Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani', 'Betul', 'Bhind','Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dhar','Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua','Katni', 'Khandwa', 'Khargone', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch','Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni','Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain','Umaria', 'Vidisha'],
        'Maharashtra': ['Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur','Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur','Mumbai City', 'Mumbai Suburban', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad','Palghar', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg','Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal'],
        'Manipur': ['Bishnupur', 'Chandel', 'Churachandpur', 'Imphal East', 'Imphal West', 'Jiribam', 'Kakching','Kamjong', 'Kangpokpi', 'Noney', 'Pherzawl', 'Senapati', 'Tamenglong', 'Tengnoupal', 'Thoubal','Ukhrul'],
        'Meghalaya': ['East Garo Hills', 'East Jaintia Hills', 'East Khasi Hills', 'North Garo Hills', 'Ri-Bhoi','South Garo Hills', 'South West Garo Hills', 'South West Khasi Hills', 'West Garo Hills','West Jaintia Hills', 'West Khasi Hills'],
        'Mizoram': ['Aizawl', 'Champhai', 'Hnahthial', 'Khawzawl', 'Kolasib', 'Lawngtlai', 'Lunglei', 'Mamit', 'Saiha','Serchhip'],
        'Nagaland': ['Dimapur', 'Kiphire', 'Kohima', 'Longleng', 'Mokokchung', 'Mon', 'Peren', 'Phek', 'Tuensang','Wokha', 'Zunheboto'],
        'Odisha': ['Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh', 'Dhenkanal','Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 'Jharsuguda', 'Kalahandi', 'Kandhamal','Kendrapara', 'Kendujhar', 'Khordha', 'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur','Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur', 'Sundargarh'],
        'Punjab': ['Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozepur','Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Mansa', 'Moga', 'Muktsar','Pathankot', 'Patiala', 'Rupnagar', 'Sangrur', 'SAS Nagar', 'SBS Nagar', 'Sri Muktsar Sahib','Tarn Taran'],
        'Rajasthan': ['Ajmer', 'Alwar', 'Banswara', 'Baran', 'Barmer', 'Bharatpur', 'Bhilwara', 'Bikaner', 'Bundi','Chittorgarh', 'Churu', 'Dausa', 'Dholpur', 'Dungarpur', 'Hanumangarh', 'Jaipur', 'Jaisalmer','Jalore', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Karauli', 'Kota', 'Nagaur', 'Pali', 'Pratapgarh','Rajsamand', 'Sawai Madhopur', 'Sikar', 'Sirohi', 'Sri Ganganagar', 'Tonk', 'Udaipur'],
        'Sikkim': ['East Sikkim', 'North Sikkim', 'South Sikkim', 'West Sikkim'],
        'Tamil Nadu': ['Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul','Erode', 'Kallakurichi', 'Kancheepuram', 'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai','Mayiladuthurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai','Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur', 'Theni','Thoothukudi', 'Tiruchirappalli', 'Tirunelveli', 'Tirupathur', 'Tiruppur', 'Tiruvallur','Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar'],
        'Telangana': ['Adilabad', 'Bhadradri Kothagudem', 'Hyderabad', 'Jagtial', 'Jangaon', 'Jayashankar Bhupalapally','Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam', 'Kumuram Bheem', 'Mahabubabad','Mahabubnagar', 'Mancherial', 'Medak', 'Medchal-Malkajgiri', 'Mulugu', 'Nagarkurnool', 'Nalgonda','Narayanpet', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla', 'Ranga Reddy','Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad', 'Wanaparthy', 'Warangal Rural','Warangal Urban', 'Yadadri Bhuvanagiri'],
        'Tripura': ['Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sepahijala', 'South Tripura', 'Unakoti','West Tripura'],
        'Uttar Pradesh': ['Agra', 'Aligarh', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 'Ayodhya', 'Azamgarh','Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti','Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah','Etawah', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad','Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 'Jalaun','Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kasganj', 'Kaushambi','Kheri', 'Kushinagar', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura','Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh','Prayagraj', 'Raebareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabir Nagar','Shahjahanpur', 'Shamli', 'Shrawasti', 'Siddharthnagar', 'Sitapur', 'Sonbhadra', 'Sultanpur','Unnao', 'Varanasi'],
        'Uttarakhand': ['Almora', 'Bageshwar', 'Chamoli', 'Champawat', 'Dehradun', 'Haridwar', 'Nainital','Pauri Garhwal', 'Pithoragarh', 'Rudraprayag', 'Tehri Garhwal', 'Udham Singh Nagar','Uttarkashi'],
        'West Bengal': ['Alipurduar', 'Bankura', 'Birbhum', 'Cooch Behar', 'Dakshin Dinajpur', 'Darjeeling', 'Hooghly','Howrah', 'Jalpaiguri', 'Jhargram', 'Kalimpong', 'Kolkata', 'Malda', 'Murshidabad', 'Nadia''North 24 Parganas', 'Paschim Bardhaman', 'Paschim Medinipur', 'Purba Bardhaman','Purba Medinipur', 'Purulia', 'South 24 Parganas', 'Uttar Dinajpur']
    }

    def submit_check():
        cu.execute('''CREATE TABLE IF NOT EXISTS booking_records(
                   bid TEXT,
                   state_name TEXT,
                   places TEXT,
                   hotel_name TEXT,
                   hotel_price TEXT,
                   train TEXT,
                   pt TEXT,
                   transport_price TEXT
                   )''')
        connb.commit()
        name_tab3 = Name_Entry.get()
        if not name_tab3:
            messagebox.showerror("Error", "Enter your name!")
            return

        state_tab3 = state_entry.get()
        print('hgjhg', state_tab3)
        if not state_tab3:
            messagebox.showerror("Error", "Choose a state!")
            return
        if state_tab3 not in districts_in_states:
            messagebox.showerror("Error", "Choose a valid state!")
            return
        city_tab3 = city_entry.get()
        if not city_tab3:
            messagebox.showerror("Error", "Choose a city!")
            return
        if city_tab3 not in districts_in_states[state_tab3]:
            messagebox.showerror("Error", "Chosen city not in selected state!")
            return

        email_tab3 = email_Entry.get()
        if not email_tab3:
            messagebox.showerror("Error", "Enter your email!")
            return
        if not email_checker(email_Entry.get()):
            messagebox.showerror("Error", "Invalid email format!")
            return

        phone_no_tab3 = phone_no_Entry.get()
        if len(phone_no_tab3) != 10:
            messagebox.showerror("Error", "Invalid phone number!")
            return

        destination_tab3 = destination_Entry.get()
        if not destination_tab3:
            messagebox.showerror("Error", "Enter your destination!")
            return

        # date validation
        date_format = "%m/%d/%y"
        date_str = date_entry.get()
        entered_date = datetime.strptime(date_str, date_format)
        print(entered_date)
        today_date = datetime.today()
        print(today_date)
        if entered_date < today_date:
            messagebox.showerror("Date Error", "Date is invalid")
            return

        days_tab3 = days_spinbox.get()
        people_tab3 = people_spinbox.get()

        mode_of_transport_tab3 = var.get()

        guide_tab3 = switch.get()
        cu.execute("SELECT * FROM booking_details")
        booking_id = len(cu.fetchall()) + 1
        cu.executemany("INSERT INTO booking_details VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", [(rid, booking_id, name_tab3,state_tab3, city_tab3,email_tab3, phone_no_tab3,destination_tab3, days_tab3,people_tab3,mode_of_transport_tab3,guide_tab3,date_entry.get())])
        connb.commit()
        show_package(booking_id)
    

    
    #-----------------------------------------------------
    #main booking tab
    
    cities = []
    def filter_cities(event):
        typed = city_entry.get()
        if typed == '':
            city_entry['values'] = cities
        else:
            data = []
            for city in city_entry['values']:
                if city.lower().startswith(typed.lower()):
                    data.append(city)
            city_entry['values'] = data

    def filter_states(event):
        typed = state_entry.get()
        if typed == '':
            state_entry['values'] = all_states
        else:
            data = []
            for state in all_states:
                if state.lower().startswith(typed.lower()):
                    data.append(state)
            state_entry['values'] = data

    def filter_states_destination(event):
        typed = destination_Entry.get()
        if typed == '':
            destination_Entry['values'] = all_states
        else:
            data = []
            for state in all_states:
                if state.lower().startswith(typed.lower()):
                    data.append(state)
            destination_Entry['values'] = data

    def show_city_list(event):
        state = state_entry.get()
        if state not in districts_in_states:
            cities=[]
        else:
           cities=districts_in_states[state] 

        city_entry['values'] = cities


    display1 = Frame(tab3)
    display1.pack(fill=BOTH,expand=True)
    
    Name_Label = Label(display1, text="Name:", font=("Constantia", 12), width=50, height=5)
    Name_Label.grid(row=0, column=0, sticky=E, padx=(20, 5), pady=(20, 5), columnspan=2)
    Name_Entry = Entry(display1, width=30)
    Name_Entry.grid(row=0, column=2, padx=5, pady=(20, 5), columnspan=2)

    state_label = Label(display1, text="State of Residence:", font=("Constantia", 12), width=50, height=5)
    state_label.grid(row=1, column=0, sticky=E, padx=(20, 5), pady=5, columnspan=2)
    state_var = StringVar()
    all_states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana","Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur","Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu","Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]
    state_entry = ttk.Combobox(display1, textvariable=state_var, values=all_states, width=27, height=3)
    state_entry.grid(row=1, column=2, padx=5, pady=5, columnspan=2)
    state_entry.bind("<KeyRelease>", filter_states)
    state_entry.bind("<<ComboboxSelected>>", show_city_list)
    
    city_label = Label(display1, text="City of Residence:", font=("Constantia", 12), width=50, height=5)
    city_label.grid(row=2, column=0, sticky=E, padx=(20, 5), pady=5, columnspan=2)
    city_var = StringVar()
    city_entry = ttk.Combobox(display1, textvariable=city_var, width=27, height=3)
    city_entry.grid(row=2, column=2, padx=5, pady=5, columnspan=2)
    city_entry.bind("<KeyRelease>", filter_cities)

    email_Label = Label(display1, text="Email:", font=("Constantia", 12), width=50, height=5)
    email_Label.grid(row=3, column=0, sticky=E, padx=(20, 5), pady=5, columnspan=2)
    email_Entry = Entry(display1, width=30)
    email_Entry.grid(row=3, column=2, padx=5, pady=5, columnspan=2)

    phone_no_Label = Label(display1, text="Phone No:", font=("Constantia", 12), width=50, height=5)
    phone_no_Label.grid(row=4, column=0, sticky=E, padx=(20, 5), pady=5, columnspan=2)
    phone_no_Entry = Entry(display1, width=30)
    phone_no_Entry.grid(row=4, column=2, padx=5, pady=5, columnspan=2)

    destination_Label = Label(display1, text="Destination:", font=("Constantia", 12), width=50, height=5)
    destination_Label.grid(row=0, column=4, sticky=E, padx=(20, 5), pady=(20, 5), columnspan=2)
    destination_Entry = Entry(display1, width=30)
    state_var = StringVar()
    destination_Entry = ttk.Combobox(display1, textvariable=state_var, values=all_states, width=27, height=3)
    destination_Entry.grid(row=0, column=6, padx=5, pady=5, columnspan=2)
    destination_Entry.bind("<KeyRelease>", filter_states_destination)

    days_Label = Label(display1, text="No of Days:", font=("Constantia", 12), width=50, height=5)
    days_Label.grid(row=1, column=4, sticky=E, padx=(20, 5), pady=5, columnspan=2)
    days_spinbox = Spinbox(display1, from_=1, to=5, width=27)
    days_spinbox.grid(row=1, column=6, padx=5, pady=5, columnspan=2)

    people_Label = Label(display1, text="No of People:", font=("Constantia", 12), width=50, height=5)
    people_Label.grid(row=2, column=4, sticky=E, padx=(20, 5), pady=5, columnspan=2)
    people_spinbox = Spinbox(display1, from_=1, to=50, width=27)
    people_spinbox.grid(row=2, column=6, padx=5, pady=5, columnspan=2)

    mode_of_transport_Label = Label(display1, text="Mode of Transport:", font=("Constantia", 12), width=50, height=5)
    mode_of_transport_Label.grid(row=3, column=4, sticky=E, padx=(20, 5), pady=5, columnspan=2)

    way_of_transport = ["Private Transport", "Train"]
    var = IntVar()
    for i in range(len(way_of_transport)):
        radiobutton = Radiobutton(display1, text=way_of_transport[i], font=("Times New Roman", 10), width=10,variable=var, value=i)
        radiobutton.grid(row=3, column=i + 6, padx=5, pady=5, sticky="E")

    guide_Label = Label(display1, text="Guide:", font=("Constantia", 12), width=50, height=5)
    guide_Label.grid(row=5, column=0, sticky=E, padx=(20, 5), pady=5, columnspan=2)

    switch = CTkSwitch(display1, text="", width=30)
    switch.grid(row=5, column=2, padx=5, pady=5, columnspan=2)

    date = Label(display1, text="Select a date:", font=("Constantia", 12), width=50, height=5)
    date.grid(row=4, column=4, padx=5, pady=5, columnspan=2)
    date_entry = DateEntry(display1, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=4, column=6, padx=5, pady=5, columnspan=2)

    submit = Button(display1, text="Submit", font=("Constantia", 10, "bold"), width=30, height=2, command=submit_check)
    submit.grid(row=6, column=2, pady=(20, 5), columnspan=50, rowspan=50)
    
    
    
    return