from ultralytics import YOLO
import cv2
import math
import requests 

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

model = YOLO("./yolo-Weights/yolov8n-oiv7.pt")

classNames = [
    "Accordion", "Adhesive tape", "Aircraft", "Airplane", "Alarm clock", "Alpaca",
    "Ambulance", "Animal", "Ant", "Antelope", "Apple", "Armadillo", "Artichoke",
    "Auto part", "Axe", "Backpack", "Bagel", "Baked goods", "Balance beam",
    "Ball", "Balloon", "Banana", "Band-aid", "Banjo", "Barge", "Barrel",
    "Baseball bat", "Baseball glove", "Bat (Animal)", "Bathroom accessory",
    "Bathroom cabinet", "Bathtub", "Beaker", "Bear", "Bed", "Bee", "Beehive",
    "Beer", "Beetle", "Bell pepper", "Belt", "Bench", "Bicycle", "Bicycle helmet",
    "Bicycle wheel", "Bidet", "Billboard", "Billiard table", "Binoculars",
    "Bird", "Blender", "Blue jay", "Boat", "Bomb", "Book", "Bookcase", "Boot",
    "Bottle", "Bottle opener", "Bow and arrow", "Bowl", "Bowling equipment",
    "Box", "Boy", "Brassiere", "Bread", "Briefcase", "Broccoli", "Bronze sculpture",
    "Brown bear", "Building", "Bull", "Burrito", "Bus", "Bust", "Butterfly",
    "Cabbage", "Cabinetry", "Cake", "Cake stand", "Calculator", "Camel", "Camera",
    "Can opener", "Canary", "Candle", "Candy", "Cannon", "Canoe", "Cantaloupe",
    "Car", "Carnivore", "Carrot", "Cart", "Cassette deck", "Castle", "Cat",
    "Cat furniture", "Caterpillar", "Cattle", "Ceiling fan", "Cello", "Centipede",
    "Chainsaw", "Chair", "Cheese", "Cheetah", "Chest of drawers", "Chicken",
    "Chime", "Chisel", "Chopsticks", "Christmas tree", "Clock", "Closet",
    "Clothing", "Coat", "Cocktail", "Cocktail shaker", "Coconut", "Coffee",
    "Coffee cup", "Coffee table", "Coffeemaker", "Coin", "Common fig",
    "Common sunflower", "Computer keyboard", "Computer monitor", "Computer mouse",
    "Container", "Convenience store", "Cookie", "Cooking spray", "Corded phone",
    "Cosmetics", "Couch", "Countertop", "Cowboy hat", "Crab", "Cream",
    "Cricket ball", "Crocodile", "Croissant", "Crown", "Crutch", "Cucumber",
    "Cupboard", "Curtain", "Cutting board", "Dagger", "Dairy Product", "Deer",
    "Desk", "Dessert", "Diaper", "Dice", "Digital clock", "Dinosaur", "Dishwasher",
    "Dog", "Dog bed", "Doll", "Dolphin", "Door", "Door handle", "Doughnut",
    "Dragonfly", "Drawer", "Dress", "Drill (Tool)", "Drink", "Drinking straw",
    "Drum", "Duck", "Dumbbell", "Eagle", "Earrings", "Egg (Food)", "Elephant",
    "Envelope", "Eraser", "Face powder", "Facial tissue holder", "Falcon",
    "Fashion accessory", "Fast food", "Fax", "Fedora", "Filing cabinet", 
    "Fire hydrant", "Fireplace", "Fish", "Flag", "Flashlight", "Flower", 
    "Flowerpot", "Flute", "Flying disc", "Food", "Food processor", "Football", 
    "Football helmet", "Footwear", "Fork", "Fountain", "Fox", "French fries", 
    "French horn", "Frog", "Fruit", "Frying pan", "Furniture", "Garden Asparagus", 
    "Gas stove", "Giraffe", "Girl", "Glasses", "Glove", "Goat", "Goggles", 
    "Goldfish", "Golf ball", "Golf cart", "Gondola", "Goose", "Grape", 
    "Grapefruit", "Grinder", "Guacamole", "Guitar", "Hair dryer", "Hair spray", 
    "Hamburger", "Hammer", "Hamster", "Hand dryer", "Handbag", "Handgun", 
    "Harbor seal", "Harmonica", "Harp", "Harpsichord", "Hat", "Headphones", 
    "Heater", "Hedgehog", "Helicopter", "Helmet", "High heels", "Hiking equipment", 
    "Hippopotamus", "Home appliance", "Honeycomb", "Horizontal bar", "Horse", 
    "Hot dog", "House", "Houseplant", "Human arm", "Human beard", "Human body", 
    "Human ear", "Human eye", "Human face", "Human foot", "Human hair", 
    "Human hand", "Human head", "Human leg", "Human mouth", "Human nose", 
    "Humidifier", "Ice cream", "Indoor rower", "Infant bed", "Insect", 
    "Invertebrate", "Ipod", "Isopod", "Jacket", "Jacuzzi", "Jaguar (Animal)", 
    "Jeans", "Jellyfish", "Jet ski", "Jug", "Juice", "Kangaroo", "Kettle", 
    "Kitchen & dining room table", "Kitchen appliance", "Kitchen knife", 
    "Kitchen utensil", "Kitchenware", "Kite", "Knife", "Koala", "Ladder", 
    "Ladle", "Ladybug", "Lamp", "Land vehicle", "Lantern", "Laptop", 
    "Lavender (Plant)", "Lemon", "Leopard", "Light bulb", "Light switch", 
    "Lighthouse", "Lily", "Limousine", "Lion", "Lipstick", "Lizard", 
    "Lobster", "Loveseat", "Luggage and bags", "Lynx", "Magpie", "Mammal", 
    "Man", "Mango", "Maple", "Maracas", "Marine invertebrates", "Marine mammal", 
    "Measuring cup", "Mechanical fan", "Medical equipment", "Microphone", 
    "Microwave oven", "Milk", "Miniskirt", "Mirror", "Missile", "Mixer", 
    "Mixing bowl", "Mobile phone", "Monkey", "Moths and butterflies", "Motorcycle", 
    "Mouse", "Muffin", "Mug", "Mule", "Mushroom", "Musical instrument", 
    "Musical keyboard", "Nail (Construction)", "Necklace", "Nightstand", "Oboe", 
    "Office building", "Office supplies", "Orange", "Organ (Musical Instrument)", 
    "Ostrich", "Otter", "Oven", "Owl", "Oyster", "Paddle", "Palm tree", 
    "Pancake", "Panda", "Paper cutter", "Paper towel", "Parachute", 
    "Parking meter", "Parrot", "Pasta", "Pastry", "Peach", "Pear", "Pen", 
    "Pencil case", "Pencil sharpener", "Penguin", "Perfume", "Person", 
    "Personal care", "Personal flotation device", "Piano", "Picnic basket", 
    "Picture frame", "Pig", "Pillow", "Pineapple", "Pitcher (Container)", 
    "Pizza", "Pizza cutter", "Plant", "Plastic bag", "Plate", "Platter", 
    "Plumbing fixture", "Polar bear", "Pomegranate", "Popcorn", "Porch", 
    "Porcupine", "Poster", "Potato", "Power plugs and sockets", "Pressure cooker", 
    "Pretzel", "Printer", "Pumpkin", "Punching bag", "Rabbit", "Raccoon", 
    "Racket", "Radish", "Ratchet (Device)", "Raven", "Rays and skates", 
    "Red panda", "Refrigerator", "Remote control", "Reptile", "Rhinoceros", 
    "Rifle", "Ring binder", "Rocket", "Roller skates", "Rose", "Rugby ball", 
    "Ruler", "Salad", "Salt and pepper shakers", "Sandal", "Sandwich", 
    "Saucer", "Saxophone", "Scale", "Scarf", "Scissors", "Scoreboard", 
    "Scorpion", "Seafood", "Seagull", "Seal", "Shark", "Shoe", "Shooting game", 
    "Shorts", "Shrimp", "Ski", "Skillet", "Skirt", "Skull", "Slippers", 
    "Socks", "Soda can", "Sofa", "Spoon", "Squash (Fruit)", "Squid", 
    "Staircase", "Steak", "Steering wheel", "Stick", "Stove", "Strawberry", 
    "Suitcase", "Sunglasses", "Superhero", "Table", "Taco", "Teddy bear", 
    "Television", "Tennis racket", "Theater", "Tiger", "Toaster", "Tobacco", 
    "Toilet", "Tomato", "Tongs", "Toothbrush", "Toothpaste", "Tower", 
    "Train", "Tray", "Trolley", "Tulip", "Turtle", "Umbrella", "Unicycle", 
    "Vase", "Vegetable", "Video game console", "Waffle", "Wagon", 
    "Wall clock", "Washing machine", "Watch", "Water", "Watermelon", 
    "Whale", "Whistle", "Wig", "Wine glass", "Wrench", "Yardstick", 
    "Zebra", "Zipper"
]

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)

            cls = int(box.cls[0])

            # Check if cls is a valid index
            if cls < len(classNames):
                class_name = classNames[cls]
            else:
                class_name = "Unknown"
                print("Class index out of range:", cls)

            # If detected object matches target (e.g., a bottle)
            if class_name == "Bottle" and confidence > 0.7:
                print(f"Detected {class_name} with confidence {confidence}")
                
                # Send a request to the Flask server to start the robot
                try:
                    response = requests.get('http://localhost:5000/control?cmd=start')
                    print(response.json())
                except Exception as e:
                    print("Failed to send command to robot:", e)

            org = (x1, y1 - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, f"{class_name} {confidence}", org, font, fontScale, color, thickness)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
