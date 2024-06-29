from tkinter import *
from tkinter import ttk
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL import Image, ImageTk

conn = sqlite3.connect("places_details.db")
c = conn.cursor()

connb = sqlite3.connect('booking_details.db')
cu = connb.cursor()

class UI:
    @staticmethod
    def tab6_page(tab6):
        canvas1 = Canvas(tab6, width=1000, height=800)
        canvas1.pack(fill=BOTH, expand=True)
    
        long_text = ('''Established in 1968, TravelEasy is entirely owned and managed by Sangam Group of Hotels. The Sangam Group is recognized as one of the largest hotel chains in Tamil Nadu. Along with the Group, the GT Holidays is striving hard for ultimate success and innovation.
            We are an ISO 9001: 2008 certified company that aim to set clear goals, fix the priorities and organize the resources effectively. TravelEasy enables you to discover a new destination and offer unique ideas to your travel.
    
        Our travel company offers a complete business travel environment for MICE (Meetings, Incentives, Conferences and Events) services at affordable cost. We provide a wide range of holiday tour packages for all the domestic and international destinations across the world.''')
        
        text1 = canvas1.create_text(868, 70, text="Our Story", anchor="nw", font=("Helvetica", 30), fill="black", justify=CENTER)
        text2 = canvas1.create_text(20, 150, text=long_text, anchor="nw", font=("Helvetica", 18), fill="black", width=1790)
        default_bg_color = tab6.cget("background")
        
        # Our Mission
        our_mission = '''TravelEasy is a fully integrated travel company that offers comprehensive solutions for all the business and leisure travelers across the world. This prestigious travel company in Chennai mainly aims to satisfy the client’s requirements with ultimate transparency and cost-effectiveness. We assure to offer round the clock support and assistance at any point of your travel.'''
        mission_label = Label(canvas1, text=our_mission, font=("Helvetica", 18), justify=LEFT, wraplength=800, bg=default_bg_color)
    
        # Our Vision
        our_vision = '''Our TravelEasy Team is striving hard to become the world class travel company and industry leader in the near future. We are planning to focus on customer centric approach and gain recognition among the worldwide clients. The travel company believes in maintaining highest quality standards and craft extraordinary moments especially for you.'''
        vision_label = Label(canvas1, text=our_vision, font=("Helvetica", 18), justify=LEFT, wraplength=800, bg=default_bg_color)
    
        # Create labels for titles
        mission_title_label = Label(canvas1, text="Our Mission", font=("Helvetica", 30), bg=default_bg_color)
        vision_title_label = Label(canvas1, text="Our Vision", font=("Helvetica", 30), bg=default_bg_color)
    
        # Place the labels on the canvas
        canvas1.create_window(20, 460, anchor="nw", window=mission_title_label)
        canvas1.create_window(20, 540, anchor="nw", window=mission_label)
        canvas1.create_window(900, 460, anchor="nw", window=vision_title_label)
        canvas1.create_window(900, 540, anchor="nw", window=vision_label)

    @staticmethod
    def tab5_page(tab5):
        canvas2 = Canvas(tab5, width=1000, height=800)
        canvas2.pack(fill=BOTH, expand=True)
        
        praga_label = '''Pragadeesh
        
        contact : +91 9363130385
        
        mail : 23i246@psgtech.ac.in
        '''
        sanjay_label = '''Sanjay
        
        contact : +91 9952441708
        
        mail : 23i259@psgtech.ac.in
        '''
        valan_label = '''Valan Antony Raj
        
        contact : +91 6374980861
        
        mail : 23i70@psgtech.ac.in
        '''
        default_bg_color = tab5.cget("background")
        contact = Label(canvas2, text="Contact", font=("Helvetica", 30), justify=LEFT, wraplength=500, bg=default_bg_color)
        canvas2.create_window(868, 70, anchor="nw", window=contact)
        praga_label = Label(canvas2, text=praga_label, font=("Helvetica", 20), justify=LEFT, wraplength=500, bg=default_bg_color)
        canvas2.create_window(150, 200, anchor="nw", window=praga_label)
        sanjay_label = Label(canvas2, text=sanjay_label, font=("Helvetica", 20), justify=LEFT, wraplength=500, bg=default_bg_color)
        canvas2.create_window(775, 200, anchor="nw", window=sanjay_label)
        valan_label = Label(canvas2, text=valan_label, font=("Helvetica", 20), justify=LEFT, wraplength=500, bg=default_bg_color)
        canvas2.create_window(1400, 200, anchor="nw", window=valan_label)
    
        stay_connected = Label(canvas2, text="Stay Connected", font=("Helvetica", 30), justify=LEFT, wraplength=500, bg=default_bg_color)
        canvas2.create_window(150, 500, anchor="nw", window=stay_connected)
        sc_contact = '''Phone : +91 9810098100'''
        sc_contact = Label(canvas2, text=sc_contact, font=("Helvetica", 20), justify=LEFT, wraplength=500, bg=default_bg_color)
        canvas2.create_window(775, 650, anchor="nw", window=sc_contact)
        sc_mail = '''Mail : TravelEasy@gmail.com'''
        sc_mail = Label(canvas2, text=sc_mail, font=("Helvetica", 20), justify=LEFT, wraplength=500, bg=default_bg_color)
        canvas2.create_window(1400, 650, anchor="nw", window=sc_mail)
        sc_insta = '''Instagram : TravelEasy_2024'''
        sc_insta = Label(canvas2, text=sc_insta, font=("Helvetica", 20), justify=LEFT, wraplength=500, bg=default_bg_color)
        canvas2.create_window(150, 650, anchor="nw", window=sc_insta)
        
    @staticmethod
    def tab1_page(tab):
        def load_images(image_files):
            images = [Image.open(img) for img in image_files]
            resize = [img.resize((1940, 890)) for img in images]
            images = [ImageTk.PhotoImage(img) for img in resize]
            return images
        
        def slide_image():
            nonlocal current_image_index, current_image_id, next_image_id
            
            current_image_index = (current_image_index + 1) % len(images)
            next_image = images[current_image_index]
            next_image_id = canvas.create_image(root.winfo_screenwidth(), 0, anchor='nw', image=next_image)
            animate_slide()
        
        def animate_slide():
            nonlocal current_image_id, next_image_id
            
            current_coords = canvas.coords(current_image_id)
            next_coords = canvas.coords(next_image_id)
            
            if current_coords[0] <= -root.winfo_screenwidth():
                canvas.delete(current_image_id)
                current_image_id = next_image_id
                next_image_id = None
                canvas.delete("text")
                root.after(delay, slide_image)
            else:
                canvas.move(current_image_id, -slide_speed, 0)
                canvas.move(next_image_id, -slide_speed, 0)
                text_id = canvas.create_text(960, 350, text="Welcome to TravelEasy", font=("Helvetica", 60), fill="white")
                text_id = canvas.create_text(960, 450, text='"Explore The Unravel Mysteries Of The World"', font=("Helvetica", 30), fill="white")
                root.after(30, animate_slide)
        
        image_files = ["Andaman.jpg","man.jpg","Ooty.jpg","Himachal.jpg","Coorg.jpg"]
        delay = 3000
        slide_speed = 60
        images = load_images(image_files)
        
        root = tab.winfo_toplevel()
        canvas = Canvas(tab, width=root.winfo_screenwidth(), height=900)
        canvas.pack(fill=BOTH, expand=True)
        
        current_image_index = 0
        current_image_id = canvas.create_image(0, 0, anchor='nw', image=images[0])
        next_image_id = None
        text_id = canvas.create_text(960, 350, text="Welcome to TravelEasy", font=("Helvetica", 60), fill="white")
        text_id = canvas.create_text(960, 450, text='"Explore The Unravel Mysteries Of The World"', font=("Helvetica", 30), fill="white")
        root.after(delay, slide_image)
    @staticmethod
    def tab2_page(tab2):
        def show_frame_tab2(event):
            selected_index = listbox_tab2.curselection()
            if selected_index:
                selected_index = selected_index[0]
                for frame in frames_tab2:
                    frame.pack_forget()
                frames_tab2[selected_index].pack(fill=BOTH, expand=True)

        listbox_tab2 = Listbox(tab2, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
        listbox_tab2.pack(side=LEFT, fill=BOTH)

        items = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
                    "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
                    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
                    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]

        for item in items:
            listbox_tab2.insert(END, item)

        frames_tab2 = []
        for item in items:
            frame = Frame(tab2, bg="lightgrey", width=1536, height=836)
            if item == "Andhra Pradesh":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", "Kurnool",
                            "Prakasam", "Nellore", "Srikakulam", "Visakhapatnam", "Vizianagaram", "West Godavari",
                            "YSR Kadapa"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_andhra = Canvas(frame, width=1536, height=836)
                canvas_andhra.pack(fill="both", expand=True)
                andhra_text = '''Andhra Pradesh is a state in the southeastern part of India known for its rich cultural heritage and historical significance. The state offers diverse attractions ranging from ancient temples and forts to scenic beaches and hill stations.

                Best time to visit: October to March

                Best places to visit:

                Tirupati: Famous for the Sri Venkateswara Temple, a major pilgrimage site.

                Visakhapatnam: Known for its beaches like RK Beach and Ramakrishna Beach

                Vijayawada: Famous for the Kanaka Durga Temple and Prakasam Barrage.

                Araku Valley: Known for its scenic beauty, coffee plantations, and Borra Caves.'''
                default_bg_color = canvas_andhra.cget("background")
                andhra_text = Label(canvas_andhra, text=andhra_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_andhra.create_window(150, 80, anchor="nw", window=andhra_text)
            elif item == "Arunachal Pradesh":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Anjaw", "Changlang", "Dibang Valley", "East Kameng", "East Siang",
                            "Kamle", "Kra Daadi", "Kurung Kumey", "Lepa Rada", "Lohit", "Longding",
                            "Lower Dibang Valley", "Lower Siang", "Lower Subansiri", "Namsai",
                            "Pakke-Kessang", "Papum Pare", "Shi Yomi", "Siang", "Tawang", "Tirap",
                            "Upper Dibang Valley", "Upper Siang", "Upper Subansiri", "West Kameng", "West Siang"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_aruna = Canvas(frame, width=1536, height=836)
                canvas_aruna.pack(fill="both", expand=True)
                aruna_text = '''Arunachal Pradesh is a northeastern state known for its picturesque landscapes, rich biodiversity, and vibrant tribal culture. It is a paradise for nature lovers and adventure enthusiasts with opportunities for trekking, rafting, and wildlife spotting.

                Best time to visit: October to April

                Best places to visit:

                Tawang: Famous for the Tawang Monastery, Sela Pass, and scenic views of the Eastern Himalayas.

                Ziro Valley: Known for its lush greenery, rice fields, and Apatani tribal culture.

                Namdapha National Park: Largest protected area in the Eastern Himalaya biodiversity hotspot

                Itanagar: State capital known for Itanagar Wildlife Sanctuary and Gompa Temple.'''
                default_bg_color = canvas_aruna.cget("background")
                aruna_text = Label(canvas_aruna, text=aruna_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_aruna.create_window(150, 80, anchor="nw", window=aruna_text)

            elif item == "Assam":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Baksa", "Barpeta", "Biswanath", "Bongaigaon", "Cachar", "Charaideo",
                            "Chirang", "Darrang", "Dhemaji", "Dhubri", "Dibrugarh", "Dima Hasao",
                            "Goalpara", "Golaghat", "Hailakandi", "Hojai", "Jorhat", "Kamrup",
                            "Kamrup Metropolitan", "Karbi Anglong", "Karimganj", "Kokrajhar",
                            "Lakhimpur", "Majuli", "Morigaon", "Nagaon", "Nalbari", "Sivasagar",
                            "Sonitpur", "South Salmara-Mankachar", "Tinsukia", "Udalguri", "West Karbi Anglong"]
                for city in cities:
                    nested_listbox.insert(END, city)
                canvas_assam = Canvas(frame, width=1536, height=836)
                canvas_assam.pack(fill="both", expand=True)
                assam_text = '''Assam is a state in northeastern India known for its tea gardens, wildlife sanctuaries, and cultural diversity. The Brahmaputra River and Kaziranga National Park are notable attractions.

                Best time to visit: October to April

                Best places to visit:

                Guwahati: Gateway to Assam, known for Kamakhya Temple, Umananda Island, and Assam State Museum.

                Kaziranga National Park: Famous for one-horned rhinoceros and diverse wildlife.

                Majuli: World's largest river island famous for Vaishnavite monasteries (satras) and culture.

                Sivasagar: Known for Ahom-era monuments like Rang Ghar, Talatal Ghar, and Sivasagar Tank.'''
                default_bg_color = canvas_assam.cget("background")
                assam_text = Label(canvas_assam, text=assam_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_assam.create_window(150, 80, anchor="nw", window=assam_text)

            elif item == "Bihar":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur",
                            "Bhojpur", "Buxar", "Darbhanga", "East Champaran", "Gaya", "Gopalganj",
                            "Jamui", "Jehanabad", "Kaimur", "Katihar", "Khagaria", "Kishanganj",
                            "Lakhisarai", "Madhepura", "Madhubani", "Munger", "Muzaffarpur",
                            "Nalanda", "Nawada", "Patna", "Purnia", "Rohtas", "Saharsa",
                            "Samastipur", "Saran", "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan",
                            "Supaul", "Vaishali", "West Champaran"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_bihar = Canvas(frame, width=1536, height=836)
                canvas_bihar.pack(fill="both", expand=True)
                bihar_text = '''Bihar is a state in eastern India known for its rich history, ancient universities, and religious significance. Bodh Gaya, where Buddha attained enlightenment, is a major pilgrimage site.

                Best time to visit: October to March

                Best places to visit:

                Bodh Gaya: UNESCO World Heritage Site, known for Mahabodhi Temple, Bodhi Tree, and Great Buddha Statue.

                Nalanda: Ancient center of learning, known for Nalanda University ruins and Nalanda Archaeological

                Rajgir: Historical city known for Vishwa Shanti Stupa, Griddhakuta Hill, and hot springs.

                Patna: Capital city known for Golghar, Patna Museum, and Kumhrar excavation site.
                '''
                default_bg_color = canvas_bihar.cget("background")
                bihar_text = Label(canvas_bihar, text=bihar_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_bihar.create_window(150, 80, anchor="nw", window=bihar_text)
            elif item == "Chhattisgarh":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = [
                    "Balod", "Baloda Bazar", "Balrampur", "Bastar", "Bemetara", "Bijapur",
                    "Bilaspur", "Dantewada", "Dhamtari", "Durg", "Gariaband", "Janjgir-Champa",
                    "Jashpur", "Kabirdham", "Kanker", "Kondagaon", "Korba", "Koriya",
                    "Mahasamund", "Mungeli", "Narayanpur", "Raigarh", "Raipur", "Rajnandgaon",
                    "Sukma", "Surajpur", "Surguja"]
                for city in cities:
                    nested_listbox.insert(END, city)
                canvas_chatti = Canvas(frame, width=1536, height=836)
                canvas_chatti.pack(fill="both", expand=True)
                chatti_text = '''Chhattisgarh is a state in central India known for its tribal culture, ancient temples, and lush green forests. It offers opportunities for wildlife tourism and eco-tourism.

                Best time to visit: October to March

                Best places to visit:

                Raipur: State capital known for Mahant Ghasidas Museum and Nandan Van Zoo.

                Bastar: Tribal heartland known for Bastar Palace, Chitrakote Falls, and Bastar Dussehra.

                Chitrakote Falls: Widest waterfall in India, often called the Niagara Falls of India.

                Sirpur: Archaeological site known for ancient temples and Buddhist ruins.'''
                default_bg_color = canvas_chatti.cget("background")
                chatti_text = Label(canvas_chatti, text=chatti_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_chatti.create_window(150, 80, anchor="nw", window=chatti_text)

            elif item == "Goa":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["North Goa", "South Goa"]
                for city in cities:
                    nested_listbox.insert(END, city)
                    # content
                canvas_goa = Canvas(frame, width=1536, height=836)
                canvas_goa.pack(fill="both", expand=True)
                goa_text = '''Goa
                The unofficial party place of India, Goa is more than that. It has a great legacy, history and culture that are yet to be explored. But if beaches are what you are looking for, then the state has that too. And that's why, India tours to Goa are a great option to explore the place, according to your interests. Goa holiday packages are also popular because Goa is one of the top places in the world when it comes to nightlife. Find several exciting tour packages and other India holiday packages that let you try Goa's melange of watersports and other fun activities.


                Best time to visit: November to February


                Best places to visit:

                Calangute
                Baga
                Anjuna
                Miramar
                Palolem
                Panjim

                You can also include the offbeat Patnem Beach in your holiday tour packages, since it was listed amongst one of Asia’s top 20 beaches.'''
                default_bg_color = canvas_goa.cget("background")
                goa_text = Label(canvas_goa, text=goa_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_goa.create_window(150, 80, anchor="nw", window=goa_text)
            elif item == "Gujarat":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha", "Bharuch",
                            "Bhavnagar", "Botad", "Chhota Udaipur", "Dahod", "Dang", "Devbhoomi Dwarka",
                            "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh", "Kheda",
                            "Kutch", "Mahisagar", "Mehsana", "Morbi", "Narmada", "Navsari",
                            "Panchmahal", "Patan", "Porbandar", "Rajkot", "Sabarkantha",
                            "Surat", "Surendranagar", "Tapi", "Vadodara", "Valsad"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_guj = Canvas(frame, width=1536, height=836)
                canvas_guj.pack(fill="both", expand=True)
                guj_text = '''Gujarat is a state in western India known for its vibrant culture, historic sites, and diverse landscapes ranging from deserts to beaches. It is the birthplace of Mahatma Gandhi.

                Best time to visit: October to March

                Best places to visit:

                Ahmedabad: Known for Sabarmati Ashram, Adalaj Stepwell, and Sidi Saiyyed Mosque.

                Dwarka: Hindu pilgrimage site known for Dwarkadhish Temple and Dwarka Beach.

                Somnath: Famous for the Somnath Temple, one of the twelve Jyotirlinga shrines of Lord Shiva.
                Gir National Park: Only natural habitat of Asiatic lions, known for lion safari and birdwatching.'''
                default_bg_color = canvas_guj.cget("background")
                guj_text = Label(canvas_guj, text=guj_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_guj.create_window(150, 80, anchor="nw", window=guj_text)
            elif item == "Haryana":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad",
                            "Gurugram", "Hisar", "Jhajjar", "Jind", "Kaithal", "Karnal", "Kurukshetra",
                            "Mahendragarh", "Nuh", "Palwal", "Panchkula", "Panipat", "Rewari",
                            "Rohtak", "Sirsa", "Sonipat", "Yamunanagar"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_haryana = Canvas(frame, width=1536, height=836)
                canvas_haryana.pack(fill="both", expand=True)
                haryana_text = '''Haryana is a state in northern India known for its agricultural prosperity, ancient temples, and historical sites. It is also a hub for modern industries and urban development.

                Best time to visit: October to March

                Best places to visit:

                Gurugram (Gurgaon): Millennium City known for Cyber Hub, Kingdom of Dreams, and Sultanpur National Park.

                Panipat: Historical city known for Panipat Museum and the battles of Panipat.

                Kurukshetra: Holy city known for Brahma Sarovar, Jyotisar, and Kurukshetra War Memorial.

                Faridabad: Industrial city known for Surajkund Mela, Raja Nahar Singh Palace, and Badkhal Lake.'''
                default_bg_color = canvas_haryana.cget("background")
                haryana_text = Label(canvas_haryana, text=haryana_text, font=("Helvetica", 18), justify=LEFT,
                                        wraplength=1200, bg=default_bg_color)
                canvas_haryana.create_window(150, 80, anchor="nw", window=haryana_text)

            elif item == "Himachal Pradesh":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur", "Kullu", "Lahaul-Spiti",
                            "Mandi", "Shimla", "Sirmaur", "Solan", "Una"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_hima = Canvas(frame, width=1536, height=836)
                canvas_hima.pack(fill="both", expand=True)
                hima_text = '''Himachal Pradesh is a mountainous state in northern India known for its scenic beauty, hill stations, and adventure sports. It is popular among tourists seeking trekking and skiing experiences.

                Best time to visit: March to June, September to December

                Best places to visit:

                Shimla: Capital city known for the Ridge, Mall Road, and Jakhu Temple.

                Manali: Famous hill station known for Hadimba Temple, Solang Valley, and Rohtang Pass.

                Dharamshala: Home to the Dalai Lama and Tibetan culture, known for Tsuglagkhang Complex and Triund trek.

                Spiti Valley: Cold desert mountain valley known for Key Monastery, Chandratal Lake, and high-altitude villages.'''
                default_bg_color = canvas_hima.cget("background")
                hima_text = Label(canvas_hima, text=hima_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_hima.create_window(150, 80, anchor="nw", window=hima_text)

            elif item == "Jharkhand":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", "East Singhbhum",
                            "Garhwa", "Giridih", "Godda", "Gumla", "Hazaribagh", "Jamtara",
                            "Khunti", "Koderma", "Latehar", "Lohardaga", "Pakur", "Palamu",
                            "Ramgarh", "Ranchi", "Sahebganj", "Seraikela-Kharsawan",
                            "Simdega", "West Singhbhum"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_j = Canvas(frame, width=1536, height=836)
                canvas_j.pack(fill="both", expand=True)
                j_text = '''Jharkhand is a state in eastern India known for its rich mineral resources, waterfalls, and dense forests. It offers opportunities for eco-tourism and cultural exploration.

                Best time to visit: October to March

                Best places to visit:

                Ranchi: Capital city known for Ranchi Lake, Jagannath Temple, and Tagore Hill.

                Jamshedpur: Industrial city known for Jubilee Park, Dimna Lake, and Tata Steel Zoological Park.

                Netarhat: Hill station known for Magnolia Point, Upper Ghaghri Falls, and sunrise views.

                Betla National Park: Wildlife sanctuary known for tigers, elephants, and bison.'''
                default_bg_color = canvas_j.cget("background")
                j_text = Label(canvas_j, text=j_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                bg=default_bg_color)
                canvas_j.create_window(150, 80, anchor="nw", window=j_text)

            elif item == "Karnataka":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban",
                            "Bidar", "Chamarajanagar", "Chikballapur", "Chikkamagaluru", "Chitradurga",
                            "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan", "Haveri",
                            "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya", "Mysuru",
                            "Raichur", "Ramanagara", "Shivamogga", "Tumakuru", "Udupi", "Uttara Kannada",
                            "Vijayapura", "Yadgir"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_karna = Canvas(frame, width=1536, height=836)
                canvas_karna.pack(fill="both", expand=True)
                karna_text = '''Karnataka is a state in southwestern India known for its diverse culture, historic sites, and natural landscapes. It is home to ancient temples, UNESCO World Heritage Sites, and vibrant cities.

                Best time to visit: October to March

                Best places to visit:

                Bengaluru (Bangalore): IT hub known for Lalbagh Botanical Garden, Bangalore Palace, and Vidhana Soudha.

                Mysuru (Mysore): Cultural capital known for Mysore Palace, Chamundi Hill, and Dasara Festival.

                Hampi: UNESCO World Heritage Site known for Hampi ruins, Virupaksha Temple, and Vijaya Vittala Temple.

                Coorg (Kodagu): Hill station known for coffee plantations, Abbey Falls, and Talakaveri Wildlife Sanctuary.'''
                default_bg_color = canvas_karna.cget("background")
                karna_text = Label(canvas_karna, text=karna_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_karna.create_window(150, 80, anchor="nw", window=karna_text)

            elif item == "Kerala":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", "Kollam",
                            "Kottayam", "Kozhikode", "Malappuram", "Palakkad", "Pathanamthitta",
                            "Thiruvananthapuram", "Thrissur", "Wayanad"]
                for city in cities:
                    nested_listbox.insert(END, city)
                canvas_kerala = Canvas(frame, width=1536, height=836)
                canvas_kerala.pack(fill="both", expand=True)
                kerala_text = '''Kerala is a state in southern India known for its palm-lined beaches, backwaters, and network of canals. It is also known for its diverse wildlife, hill stations, and Ayurvedic treatments.

                Best time to visit: October to March

                Best places to visit:

                Kochi (Cochin): Port city known for Fort Kochi, Mattancherry Palace, and Chinese Fishing Nets.

                Alleppey (Alappuzha): Famous for Kerala backwaters, houseboat cruises, and Alappuzha Beach.

                Munnar: Hill station known for tea plantations, Eravikulam National Park, and Anamudi Peak.

                Thiruvananthapuram: State capital known for Padmanabhaswamy Temple, Kovalam Beach, and Napier Museum.'''
                default_bg_color = canvas_kerala.cget("background")
                kerala_text = Label(canvas_kerala, text=kerala_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_kerala.create_window(150, 80, anchor="nw", window=kerala_text)

            elif item == "Madhya Pradesh":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat",
                            "Barwani", "Betul", "Bhind", "Bhopal", "Burhanpur", "Chachaura",
                            "Chhatarpur", "Chhindwara", "Damoh", "Datia", "Dewas", "Dhar",
                            "Dindori", "Guna", "Gwalior", "Harda", "Hoshangabad", "Indore",
                            "Jabalpur", "Jhabua", "Katni", "Khandwa", "Khargone", "Mandla",
                            "Mandsaur", "Morena", "Narmadapuram", "Neemuch", "Niwari", "Panna",
                            "Raisen", "Rajgarh", "Ratlam", "Rewa", "Sagar", "Satna", "Sehore",
                            "Seoni", "Shahdol", "Shajapur", "Sheopur", "Shivpuri", "Sidhi",
                            "Singrauli", "Tikamgarh", "Ujjain", "Umaria", "Vidisha"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_mad = Canvas(frame, width=1536, height=836)
                canvas_mad.pack(fill="both", expand=True)
                mad_text = '''Madhya Pradesh is a state in central India known for its wildlife sanctuaries, ancient temples,and rich cultural heritage. It is often referred to as the "Heart of India" due to its geographical location and historical significance.

                Best time to visit: October to March

                Best places to visit:

                Bhopal: Capital city known for its lakes, Van Vihar National Park, and Bharat Bhavan.

                Khajuraho: UNESCO World Heritage Site famous for its erotic temples and intricate carvings.

                Kanha National Park: Renowned tiger reserve known for its wildlife safaris and diverse fauna.

                Ujjain: Ancient city known for the Mahakaleshwar Temple, one of the twelve Jyotirlingas, and the Kumbh Mela.'''
                default_bg_color = canvas_mad.cget("background")
                mad_text = Label(canvas_mad, text=mad_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_mad.create_window(150, 80, anchor="nw", window=mad_text)

            elif item == "Maharashtra":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Ahmednagar", "Akola", "Amravati", "Aurangabad", "Beed", "Bhandara",
                            "Buldhana", "Chandrapur", "Dhule", "Gadchiroli", "Gondia", "Hingoli",
                            "Jalgaon", "Jalna", "Kolhapur", "Latur", "Mumbai City", "Mumbai Suburban",
                            "Nagpur", "Nanded", "Nandurbar", "Nashik", "Osmanabad", "Palghar",
                            "Parbhani", "Pune", "Raigad", "Ratnagiri", "Sangli", "Satara",
                            "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim", "Yavatmal"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_maha = Canvas(frame, width=1536, height=836)
                canvas_maha.pack(fill="both", expand=True)
                maha_text = '''Maharashtra is a state in western India known for its diverse culture, bustling cities, and scenic landscapes. It offers a mix of modern urban life and historic attractions.

                Best time to visit: October to March

                Best places to visit:

                Mumbai: Financial capital known for the Gateway of India, Marine Drive, and Bollywood.

                Pune: Cultural hub known for Aga Khan Palace, Shaniwar Wada, and vibrant nightlife.

                Aurangabad: Known for the Ajanta and Ellora Caves, both UNESCO World Heritage Sites.

                Lonavala and Khandala: Popular hill stations known for their scenic beauty and monsoon retreats.'''
                default_bg_color = canvas_maha.cget("background")
                maha_text = Label(canvas_maha, text=maha_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_maha.create_window(150, 80, anchor="nw", window=maha_text)

            elif item == "Manipur":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Bishnupur", "Chandel", "Churachandpur", "Imphal East", "Imphal West",
                            "Jiribam", "Kakching", "Kamjong", "Kangpokpi", "Noney", "Pherzawl",
                            "Senapati", "Tamenglong", "Tengnoupal", "Thoubal", "Ukhrul"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_mani = Canvas(frame, width=1536, height=836)
                canvas_mani.pack(fill="both", expand=True)
                mani_text = '''Manipur is a northeastern state known for its natural beauty, diverse culture, and rich heritage. It is often referred to as the "Jewel of India."

                Best time to visit: October to April

                Best places to visit:

                Imphal: Capital city known for Kangla Fort, Loktak Lake, and the War Cemetery.

                Loktak Lake: Largest freshwater lake in northeastern India, famous for its phumdis (floating islands).

                Moreh: Border town known for its vibrant markets and proximity to Myanmar.

                Ukhrul: Known for its scenic landscapes, Shirui Lily, and rich tribal culture.'''
                default_bg_color = canvas_mani.cget("background")
                mani_text = Label(canvas_mani, text=mani_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_mani.create_window(150, 80, anchor="nw", window=mani_text)

            elif item == "Meghalaya":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=15, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["East Garo Hills", "East Jaintia Hills", "East Khasi Hills", "North Garo Hills",
                            "Ri Bhoi", "South Garo Hills", "South West Garo Hills", "South West Khasi Hills",
                            "West Garo Hills", "West Jaintia Hills", "West Khasi Hills"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_meg = Canvas(frame, width=1536, height=836)
                canvas_meg.pack(fill="both", expand=True)
                meg_text = '''Meghalaya is a state in northeastern India known for its lush green landscapes, waterfalls, and unique living root bridges. It is a paradise for nature lovers and adventure seekers.

                Best time to visit: October to June

                Best places to visit:

                Shillong: Capital city known as the "Scotland of the East," famous for Umiam Lake, Elephant Falls, and Shillong Peak.

                Cherrapunji: Known for its living root bridges, Nohkalikai Falls, and heavy rainfall.

                Mawlynnong: Voted the cleanest village in Asia, known for its cleanliness and living root bridges.

                Dawki: Known for the crystal-clear waters of the Umngot River and scenic boat rides.'''
                default_bg_color = canvas_meg.cget("background")
                meg_text = Label(canvas_meg, text=meg_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_meg.create_window(150, 80, anchor="nw", window=meg_text)

            elif item == "Mizoram":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Aizawl", "Champhai", "Kolasib", "Lawngtlai", "Lunglei", "Mamit",
                            "Saiha", "Serchhip"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_mizo = Canvas(frame, width=1536, height=836)
                canvas_mizo.pack(fill="both", expand=True)
                mizo_text = '''Mizoram is a state in northeastern India known for its scenic beauty, rolling hills, and rich tribal culture. It offers a tranquil environment and opportunities for eco-tourism.

                Best time to visit: October to March

                Best places to visit:

                Aizawl: Capital city known for its picturesque location, Solomon's Temple, and Durtlang Hills.

                Lunglei: Known for its scenic landscapes, Khawnglung Wildlife Sanctuary, and adventure activities.

                Champhai: Border town known for its vineyards, Rih Dil Lake, and Phawngpui National Park.

                Reiek: Famous for its hilltop views, traditional Mizo village, and Reiek Tlang.'''
                default_bg_color = canvas_mizo.cget("background")
                mizo_text = Label(canvas_mizo, text=mizo_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_mizo.create_window(150, 80, anchor="nw", window=mizo_text)

            elif item == "Nagaland":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Dimapur", "Kiphire", "Kohima", "Longleng", "Mokokchung", "Mon",
                            "Noklak", "Peren", "Phek", "Tuensang", "Wokha", "Zunheboto"]
                for city in cities:
                    nested_listbox.insert(END, city)
                canvas_nag = Canvas(frame, width=1536, height=836)
                canvas_nag.pack(fill="both", expand=True)
                nag_text = '''Nagaland is a northeastern state known for its rich tribal culture, vibrant festivals, and scenic landscapes. It is famous for the Hornbill Festival, which showcases the state's cultural diversity.

                Best time to visit: October to May

                Best places to visit:

                Kohima: Capital city known for the World War II Cemetery, Kohima Museum, and Dzükou Valley trek.

                Dimapur: Gateway to Nagaland, known for the Kachari Ruins and Dimapur Ao Baptist Church.

                Mokokchung: Known for its vibrant Ao Naga culture, Longkhum village, and beautiful landscapes.

                Mon: Famous for the Konyak tribe, traditional tattoos, and the Aoling Festival.'''
                default_bg_color = canvas_nag.cget("background")
                nag_text = Label(canvas_nag, text=nag_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_nag.create_window(150, 80, anchor="nw", window=nag_text)

            elif item == "Odisha":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak", "Boudh",
                            "Cuttack", "Debagarh", "Dhenkanal", "Gajapati", "Ganjam", "Jagatsinghpur",
                            "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara", "Kendujhar",
                            "Khordha", "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur", "Nayagarh",
                            "Nuapada", "Puri", "Rayagada", "Sambalpur", "Subarnapur", "Sundargarh"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_od = Canvas(frame, width=1536, height=836)
                canvas_od.pack(fill="both", expand=True)
                od_text = '''Odisha is a state in eastern India known for its ancient temples, beaches, and rich cultural heritage. It is famous for its classical dance form, Odissi, and vibrant festivals.

                Best time to visit: October to March

                Best places to visit:

                Bhubaneswar: Capital city known for its ancient temples like Lingaraj Temple and Mukteshwar Temple.

                Puri: Famous for Jagannath Temple, Puri Beach, and the annual Rath Yatra festival.

                Konark: Known for the Sun Temple, a UNESCO World Heritage Site, and Chandrabhaga Beach.

                Chilika Lake: Asia's largest brackish water lagoon, known for birdwatching and boating.'''
                default_bg_color = canvas_od.cget("background")
                od_text = Label(canvas_od, text=od_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                bg=default_bg_color)
                canvas_od.create_window(150, 80, anchor="nw", window=od_text)
            elif item == "Punjab":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib",
                            "Fazilka", "Ferozepur", "Gurdaspur", "Hoshiarpur", "Jalandhar",
                            "Kapurthala", "Ludhiana", "Mansa", "Moga", "Mohali", "Muktsar",
                            "Pathankot", "Patiala", "Rupnagar", "Sangrur", "Shaheed Bhagat Singh Nagar", "Tarn Taran"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_pun = Canvas(frame, width=1536, height=836)
                canvas_pun.pack(fill="both", expand=True)
                pun_text = '''Punjab is a state in northern India known for its vibrant culture, historic sites, and delicious cuisine. It is the land of the Sikhs and famous for its festivals and hospitality.

                Best time to visit: October to March

                Best places to visit:

                Amritsar: Known for the Golden Temple, Jallianwala Bagh, and Wagah Border ceremony.

                Chandigarh: Capital city known for Rock Garden, Sukhna Lake, and Capitol Complex.

                Ludhiana: Known for Punjab Agricultural University Museum, Lodhi Fort, and rural tourism.

                Patiala: Known for Qila Mubarak, Sheesh Mahal, and traditional Punjabi culture.'''
                default_bg_color = canvas_pun.cget("background")
                pun_text = Label(canvas_pun, text=pun_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_pun.create_window(150, 80, anchor="nw", window=pun_text)

            elif item == "Rajasthan":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Ajmer", "Alwar", "Banswara", "Baran", "Barmer", "Bharatpur", "Bhilwara",
                            "Bikaner", "Bundi", "Chittorgarh", "Churu", "Dausa", "Dholpur",
                            "Dungarpur", "Hanumangarh", "Jaipur", "Jaisalmer", "Jalore", "Jhalawar",
                            "Jhunjhunu", "Jodhpur", "Karauli", "Kota", "Nagaur", "Pali", "Pratapgarh",
                            "Rajsamand", "Sawai Madhopur", "Sikar", "Sirohi", "Sri Ganganagar",
                            "Tonk", "Udaipur"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_raja = Canvas(frame, width=1536, height=836)
                canvas_raja.pack(fill="both", expand=True)
                raja_text = '''Rajasthan is a state in northern India known for its royal heritage, magnificent palaces, and vast deserts. It is a land of forts, palaces, and vibrant festivals.

                Best time to visit: October to March

                Best places to visit:

                Jaipur: Capital city known as the "Pink City," famous for Amber Fort, City Palace, and Hawa Mahal.

                Udaipur: Known as the "City of Lakes," famous for Lake Pichola, City Palace, and Jag Mandir.

                Jodhpur: Known as the "Blue City," famous for Mehrangarh Fort, Umaid Bhawan Palace, and Jaswant Thada.

                Jaisalmer: Known as the "Golden City," famous for Jaisalmer Fort, Thar Desert, and Sam Sand Dunes.'''
                default_bg_color = canvas_raja.cget("background")
                raja_text = Label(canvas_raja, text=raja_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_raja.create_window(150, 80, anchor="nw", window=raja_text)

            elif item == "Sikkim":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["East Sikkim", "North Sikkim", "South Sikkim", "West Sikkim"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_sikki = Canvas(frame, width=1536, height=836)
                canvas_sikki.pack(fill="both", expand=True)
                sikki_text = '''Sikkim is a small state in northeastern India known for its pristine landscapes, Buddhist monasteries, and vibrant culture. It is home to Kanchenjunga, the third highest mountain in the world.

                Best time to visit: March to June, September to December

                Best places to visit:

                Gangtok: Capital city known for Rumtek Monastery, Tsomgo Lake, and Nathula Pass.

                Pelling: Known for its panoramic views of Kanchenjunga, Pemayangtse Monastery, and Rabdentse Ruins.

                Lachung: Scenic village known for Yumthang Valley, hot springs, and snow-clad peaks.

                Namchi: Known for Char Dham, Namchi Monastery, and panoramic views of Mt. Kanchenjunga.
    '''
                default_bg_color = canvas_sikki.cget("background")
                sikki_text = Label(canvas_sikki, text=sikki_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_sikki.create_window(150, 80, anchor="nw", window=sikki_text)

            elif item == "Tamil Nadu":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore",
                            "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kancheepuram",
                            "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai", "Nagapattinam",
                            "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai", "Ramanathapuram",
                            "Ranipet", "Salem", "Sivaganga", "Tenkasi", "Thanjavur", "Theni",
                            "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tirupattur",
                            "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore",
                            "Viluppuram", "Virudhunagar"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_tn = Canvas(frame, width=1536, height=836)
                canvas_tn.pack(fill="both", expand=True)
                tn_text = '''Tamil Nadu is a state in southern India known for its Dravidian-style temples, classical dance form Bharatanatyam, and rich cultural heritage. It is a blend of tradition and modernity.

                Best time to visit: October to March

                Best places to visit:

                Chennai: Capital city known for Marina Beach, Kapaleeshwarar Temple, and Fort St. George.

                Madurai: Known for the Meenakshi Amman Temple, Thirumalai Nayakkar Palace, and Gandhi Museum.

                Ooty: Popular hill station known for its botanical gardens, Ooty Lake, and Nilgiri Mountain Railway.

                Kanyakumari: Southernmost tip of India, known for Vivekananda Rock Memorial, Thiruvalluvar Statue, and sunrise views.'''
                default_bg_color = canvas_tn.cget("background")
                tn_text = Label(canvas_tn, text=tn_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                bg=default_bg_color)
                canvas_tn.create_window(150, 80, anchor="nw", window=tn_text)

            elif item == "Telangana":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon",
                            "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar",
                            "Khammam", "Komaram Bheem Asifabad", "Mahabubabad", "Mahabubnagar",
                            "Mancherial", "Medak", "Medchal-Malkajgiri", "Mulugu", "Nagarkurnool",
                            "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli",
                            "Rajanna Sircilla", "Ranga Reddy", "Sangareddy", "Siddipet",
                            "Suryapet", "Vikarabad", "Wanaparthy", "Warangal Rural", "Warangal Urban",
                            "Yadadri Bhuvanagiri"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_tele = Canvas(frame, width=1536, height=836)
                canvas_tele.pack(fill="both", expand=True)
                tele_text = '''Telangana is a state in southern India known for its historic landmarks, bustling cities, and rich cultural heritage. It offers a blend of tradition and modernity.

                Best time to visit: October to March

                Best places to visit:

                Hyderabad: Known for its iconic Charminar, Golconda Fort, and vibrant bazaars. The city blends old-world charm with modern IT hubs.

                Warangal: Famous for the Warangal Fort, Thousand Pillar Temple, and intricate stone carvings.

                Nizamabad: Known for its historical significance and architectural marvels like the Nizamabad Fort.

                Karimnagar: Offers scenic spots like Lower Manair Dam and ancient temples like Elgandal Fort.'''
                default_bg_color = canvas_tele.cget("background")
                tele_text = Label(canvas_tele, text=tele_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_tele.create_window(150, 80, anchor="nw", window=tele_text)

            elif item == "Tripura":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Dhalai", "Gomati", "Khowai", "North Tripura", "Sepahijala",
                            "South Tripura", "Unakoti", "West Tripura"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_tri = Canvas(frame, width=1536, height=836)
                canvas_tri.pack(fill="both", expand=True)
                tri_text = '''Tripura is a northeastern state known for its scenic landscapes, diverse tribal cultures, and rich history. It offers a peaceful environment and is known for its unique blend of traditional and modern attractions.

                Best time to visit: October to March

                Best places to visit:

                Agartala: The capital city known for Ujjayanta Palace, Neermahal Palace, and Jagannath Temple.

                Unakoti: Famous for its rock-cut sculptures and ancient temples amidst lush greenery.

                Jampui Hills: Known for its pleasant climate, orange orchards, and panoramic views.

                Sepahijala Wildlife Sanctuary: Home to a variety of flora, fauna, and lakes for boating.'''
                default_bg_color = canvas_tri.cget("background")
                tri_text = Label(canvas_tri, text=tri_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                    bg=default_bg_color)
                canvas_tri.create_window(150, 80, anchor="nw", window=tri_text)

            elif item == "Uttar Pradesh":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Agra", "Aligarh", "Ambedkar Nagar", "Amethi", "Amroha", "Auraiya",
                            "Ayodhya", "Azamgarh", "Badaun", "Baghpat", "Bahraich", "Ballia",
                            "Balrampur", "Banda", "Barabanki", "Bareilly", "Basti", "Bhadohi",
                            "Bijnor", "Budaun", "Bulandshahr", "Chandauli", "Chitrakoot",
                            "Deoria", "Etah", "Etawah", "Farrukhabad", "Fatehpur", "Firozabad",
                            "Gautam Buddha Nagar", "Ghaziabad", "Ghazipur", "Gonda", "Gorakhpur",
                            "Hamirpur", "Hapur", "Hardoi", "Hathras", "Jalaun", "Jaunpur",
                            "Jhansi", "Kannauj", "Kanpur Dehat", "Kanpur Nagar", "Kasganj",
                            "Kaushambi", "Kheri", "Kushinagar", "Lalitpur", "Lucknow", "Maharajganj",
                            "Mahoba", "Mainpuri", "Mathura", "Mau", "Meerut", "Mirzapur",
                            "Moradabad", "Muzaffarnagar", "Pilibhit", "Pratapgarh", "Raebareli",
                            "Rampur", "Saharanpur", "Sambhal", "Sant Kabir Nagar", "Shahjahanpur",
                            "Shamli", "Shravasti", "Siddharthnagar", "Sitapur", "Sonbhadra",
                            "Sultanpur", "Unnao", "Varanasi"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_up = Canvas(frame, width=1536, height=836)
                canvas_up.pack(fill="both", expand=True)
                up_text = '''Uttar Pradesh is a northern state known for its rich cultural heritage, historical monuments, and religious significance. It is home to some of the most iconic landmarks in India.

                Best time to visit: October to March

                Best places to visit:

                Agra: Known for the Taj Mahal, Agra Fort, and Fatehpur Sikri, all UNESCO World Heritage Sites.

                Varanasi: One of the oldest living cities in the world, famous for its ghats, temples, and spiritual ambiance.

                Lucknow: The capital city known for its Nawabi heritage, Bara Imambara, and Rumi Darwaza.

                Mathura: Birthplace of Lord Krishna, known for its temples and vibrant Holi celebrations.'''
                default_bg_color = canvas_up.cget("background")
                up_text = Label(canvas_up, text=up_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                bg=default_bg_color)
                canvas_up.create_window(150, 80, anchor="nw", window=up_text)

            elif item == "Uttarakhand":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", "Haridwar",
                            "Nainital", "Pauri Garhwal", "Pithoragarh", "Rudraprayag",
                            "Tehri Garhwal", "Udham Singh Nagar", "Uttarkashi"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_ut = Canvas(frame, width=1536, height=836)
                canvas_ut.pack(fill="both", expand=True)
                ut_text = '''Uttarakhand is a northern state known for its scenic beauty, pilgrimage sites, and adventure tourism. It is often referred to as the "Land of the Gods" due to its many temples and ashrams.

                Best time to visit: March to June, September to November

                Best places to visit:

                Dehradun: The capital city known for its natural beauty, Robber's Cave, and Sahastradhara.

                Rishikesh: Known as the Yoga Capital of the World, famous for its ashrams, Ganga Aarti, and adventure sports.

                Nainital: Popular hill station known for Naini Lake, Naina Devi Temple, and panoramic views.

                Jim Corbett National Park: India's oldest national park, famous for its Bengal tigers and diverse wildlife.'''
                default_bg_color = canvas_ut.cget("background")
                ut_text = Label(canvas_ut, text=ut_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                bg=default_bg_color)
                canvas_ut.create_window(150, 80, anchor="nw", window=ut_text)

            elif item == "West Bengal":
                nested_listbox = Listbox(frame, bg="white", font=("Constantia", 13), width=20, height=15, borderwidth=0)
                nested_listbox.pack(side=LEFT, fill=BOTH)
                cities = ["Alipurduar", "Bankura", "Birbhum", "Cooch Behar", "Dakshin Dinajpur",
                            "Darjeeling", "Hooghly", "Howrah", "Jalpaiguri", "Jhargram",
                            "Kalimpong", "Kolkata", "Malda", "Murshidabad", "Nadia",
                            "North 24 Parganas", "Paschim Bardhaman", "Paschim Medinipur",
                            "Purba Bardhaman", "Purba Medinipur", "Purulia", "South 24 Parganas",
                            "Uttar Dinajpur"]
                for city in cities:
                    nested_listbox.insert(END, city)

                canvas_wb = Canvas(frame, width=1536, height=836)
                canvas_wb.pack(fill="both", expand=True)
                wb_text = '''West Bengal is an eastern state known for its cultural heritage, historical significance, and natural beauty. It is famous for its literature, music, and delicious cuisine.

                Best time to visit: October to March

                Best places to visit:

                Kolkata: The capital city known for its colonial architecture, Victoria Memorial, and Howrah Bridge.

                Darjeeling: Renowned hill station known for its tea gardens, Darjeeling Himalayan Railway, and scenic views of Kanchenjunga.

                Sundarbans: Largest mangrove forest in the world, home to the Royal Bengal tiger and diverse wildlife.

                Shantiniketan: Founded by Rabindranath Tagore, known for Visva Bharati University and cultural festivals.'''
                default_bg_color = canvas_wb.cget("background")
                wb_text = Label(canvas_wb, text=wb_text, font=("Helvetica", 18), justify=LEFT, wraplength=1200,
                                bg=default_bg_color)
                canvas_wb.create_window(150, 80, anchor="nw", window=wb_text)

            frames_tab2.append(frame)

        listbox_tab2.bind("<<ListboxSelect>>", show_frame_tab2)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook.Tab", padding=(124, 14), font=("Helvetica", 10), background='white', foreground="black",
                        borderwidth=0) 
    @staticmethod
    def booking_details(bid,tab4):

        Label(tab4, text="Itinerary", font=('Helvetica', 25, 'bold'), anchor=CENTER).grid(row=0, column=0, columnspan=2,padx=80, pady=20)

        cu.execute("SELECT * FROM booking_records WHERE bid=?", (bid,))
        data = cu.fetchall()[0]
        
        places=list(data[2].split('|'))
        hotels =list(data[3].split('|'))
        
        cu.execute("SELECT days,people,email FROM booking_details WHERE booking_id=?", (bid,))
        x = cu.fetchall()[0]
        email=x[2]
        days, people = x[0], x[1]
        days, people = int(days), int(people)
        
        hotel_price=0
        transport_price=float(data[7])
        hotel_price_list=list(data[4].split('|'))
        
        for price in hotel_price_list:
            hotel_price+=float(price)
            
        hotel_price*=people
        hotel_price=round(hotel_price,2)
        
        total_price=1000+hotel_price+transport_price
        total_price=round(total_price,2)
        c.execute("SELECT state_id FROM states WHERE state_name=?",(data[1],))
        state_id=c.fetchone()[0]
        print(state_id)
        Label(tab4, text="Destination State:", font=('Helvetica', 15)).grid(row=1, column=0, sticky='e', padx=80, pady=20)
        Label(tab4, text=f"{data[1]}", font=('Helvetica', 15)).grid(row=1, column=1, sticky='w', padx=80, pady=20)

        Label(tab4, text="No of People:", font=('Helvetica', 15)).grid(row=2, column=0, sticky='e', padx=80, pady=20)
        Label(tab4, text=people, font=('Helvetica', 15)).grid(row=2, column=1, sticky='w', padx=80, pady=20)

        Label(tab4, text="Booking ID:", font=('Helvetica', 15)).grid(row=1, column=2, sticky='e', padx=80, pady=20)
        Label(tab4, text=bid, font=('Helvetica', 15)).grid(row=1, column=3, sticky='w', padx=80, pady=20)

        Label(tab4, text="Days:", font=('Helvetica', 15)).grid(row=2, column=2, sticky='e', padx=80, pady=20)
        Label(tab4, text=days, font=('Helvetica', 15)).grid(row=2, column=3, sticky='w', padx=80, pady=20)
        days_list=[]
        print(hotels)
        for i in range(1,int(days)+1):
            c.execute("SELECT district_id FROM districts WHERE district_name=?",(places[i-1],))
            district_id=c.fetchone()[0]
            c.execute("SELECT place_name FROM places WHERE state_id=? AND district_id=?",(state_id,district_id))
            place_name=c.fetchall()
            print(place_name)
            place_name=list(map(lambda x:x[0],place_name))
            text=','.join(place_name)
            days_list.append([f"Day{i}",text,hotels[i-1]])
        print(days_list)


        for i, day in enumerate(days_list):
            Label(tab4, text=day[0], font=('Helvetica', 15), anchor=CENTER).grid(row=3 + i, column=0, sticky='e',padx=80, pady=20)
            Label(tab4, text=places[i], font=('Helvetica', 15)).grid(row=3 + i, column=1, columnspan=2, sticky='w',padx=80, pady=20)
            Label(tab4, text=day[2], font=('Helvetica', 15)).grid(row=3 + i, column=3, sticky='w', padx=80, pady=20)

        Label(tab4, text="Price Details", font=('Helvetica', 25, 'bold'), anchor=CENTER).grid(row=7, column=0, columnspan=4,padx=80, pady=10)

        Label(tab4, text="Hotel Price:", font=('Helvetica', 15)).grid(row=8, column=0, sticky='e', padx=80, pady=20)
        Label(tab4, text=f"₹ {hotel_price}", font=('Helvetica', 15)).grid(row=8, column=1, sticky='w', padx=80, pady=20)

        Label(tab4, text="Transport Price:", font=('Helvetica', 15)).grid(row=9, column=0, sticky='e', padx=80, pady=20)
        Label(tab4, text=f"₹ {transport_price}", font=('Helvetica', 15)).grid(row=9, column=1, sticky='w', padx=80, pady=20)

        Label(tab4, text="Service Charges:", font=('Helvetica', 15)).grid(row=10, column=0, sticky='e', padx=80,
                                                                          pady=20)
        Label(tab4, text="₹ 1000", font=('Helvetica', 15)).grid(row=10, column=1, sticky='w', padx=80, pady=20)

        Label(tab4, text="Total Fare:", font=('Helvetica', 15)).grid(row=11, column=0, sticky='e', padx=80, pady=20)
        Label(tab4, text=f"₹ {total_price}", font=('Helvetica', 15)).grid(row=11, column=1, sticky='w', padx=80, pady=20)

        #mail sender -----------------------------------
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                }}
                .container {{
                    margin: 20px;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
                .header {{
                    font-size: 24px;
                    font-weight: bold;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .details {{
                    margin-bottom: 10px;
                }}
                .day {{
                    margin-left: 20px;
                    margin-bottom: 10px;
                }}
                .price {{
                    font-weight: bold;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">Your Travel Booking Summary</div>
                <div class="details">
                    <div><b>Destination State:</b> {data[1]}</div>
                    <div><b>No of people:</b> {people}</div>
                    <div><b>Booking ID:</b> {bid}</div>
                    <div><b>Days:</b> {days}</div>
                </div>
                <div><b>Itinerary:</b></div>  
        """

        for i, day in enumerate(days_list):
            html_content += f"""
                <div class="day">      
                    <div><b>Day {i + 1}:</b></div>
                    <div>   Place: {places[i]}</div>                    
                    <div>         -{day[1]}</div>
                    <div>   Hotel: {day[2]}</div>
                </div>
            """

        html_content += f"""
                <div class="price">
                    <div><b>Price Details:</b></div>
                    <div>Hotel Price: ₹ {hotel_price}</div>
                    <div>Transport Price: ₹ {transport_price}</div>
                    <div>Service Charges: ₹ 1000</div>
                    <div>Total Fare: ₹ {total_price}</div>
                </div>
            </div>
        </body>
        </html>
        """
        sender_email = 'traveleasypy@gmail.com'
        receiver_email=email
        sender_pwd = 'etjz keuf xudf kodp'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_pwd)

            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = "Booking Receipt"

            message.attach(MIMEText(html_content, 'html'))

            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")

        except Exception as e:
            print(f"Failed to send email. Error: {str(e)}")

        finally:
            server.quit()