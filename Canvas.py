PEXELS_ley = "EdAjzUK45cT8SziTJaFENne4wvBSeun4IWzO8OMURuh66HHKBUtrRGIE"
BING_Key = "604ccd5b2f744445ae5b25b6d60f49d1"

import AI_Word_Gen as AI
import tkinter as tk
from tkinter import Entry, Button, messagebox, Canvas
import requests
from PIL import Image, ImageTk
from io import BytesIO
# Function to fetch image from Pexels API
def fetch_from_pexels(query):
    endpoint = "https://api.pexels.com/v1/search"
    api_key = PEXELS_ley

    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": 1}

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    search_results = response.json()
    if search_results["photos"]:
        return search_results["photos"][0]["src"]["large"]
    return None

# Function to fetch image from Bing Image Search API
def fetch_from_bing(query):
    endpoint = "https://api.bing.microsoft.com/v7.0/images/search"
    api_key = BING_Key
    headers = {"Ocp-Apim-Subscription-Key" : api_key}
    params = {"q": query, "count": 1, "mkt": "en-US", "imageType": "photo", "safeSearch": "Off"}

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    search_results = response.json()
    return search_results["value"][0]["contentUrl"]



def add_image_to_canvas(word, image):
    photo = ImageTk.PhotoImage(image)
    img_id = canvas.create_image(10, 10, anchor=tk.NW, image=photo)
    
    # Calculate the center position for the text
    img_width = image.width
    text_x = 10 + (img_width / 2)
    
    text_id = canvas.create_text(text_x, 170, anchor=tk.N, text=word)
    canvas.image_dict[img_id] = photo  # Store reference to avoid garbage collection
    return img_id, text_id

# Function to display image in the window
def display_image(word="blank"):
    if word == "blank":
        word = entry.get()
    
    if not word:
        messagebox.showerror("Error", "Please enter a word!")
        return

    try:
        image_url = fetch_from_pexels(word)
        if not image_url:
            image_url = fetch_from_bing(word)

        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).resize((100, 100))  # Resize for uniformity
        img_id, text_id = add_image_to_canvas(word, image)
        canvas.tag_bind(img_id, '<ButtonPress-1>', lambda event, img_id=img_id, text_id=text_id: on_drag_start(event, img_id, text_id))
        canvas.tag_bind(img_id, '<B1-Motion>', on_drag_motion)
        canvas.tag_bind(text_id, '<ButtonPress-1>', lambda event, img_id=img_id, text_id=text_id: on_drag_start(event, img_id, text_id))
        canvas.tag_bind(text_id, '<B1-Motion>', on_drag_motion)
        canvas.tag_bind(img_id, '<ButtonRelease-1>', on_drag_release)
        canvas.tag_bind(text_id, '<ButtonRelease-1>', on_drag_release)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch image for '{word}'. Error: {e}")

def on_drag_start(event, img_id, text_id):
    # Store the initial position and the IDs of the image and text
    canvas.drag_data = {'x': event.x, 'y': event.y, 'img_id': img_id, 'text_id': text_id}

def on_drag_motion(event):
    # Compute distance moved
    dx = event.x - canvas.drag_data['x']
    dy = event.y - canvas.drag_data['y']
    # Move both the image and the text
    canvas.move(canvas.drag_data['img_id'], dx, dy)
    canvas.move(canvas.drag_data['text_id'], dx, dy)
    # Store new position
    canvas.drag_data['x'] = event.x
    canvas.drag_data['y'] = event.y

def on_drag_release(event):
    # Check for overlapping items
    img_bbox = canvas.bbox(canvas.drag_data['img_id'])
    overlapping_items = canvas.find_overlapping(*img_bbox)
    
    # Filter out the current image and text from overlapping items
    overlapping_items = [item for item in overlapping_items if item not in (canvas.drag_data['img_id'], canvas.drag_data['text_id'])]
    
    # Ensure there are at least two items (an image and its text)
    if len(overlapping_items) >= 2:
        # Assuming that the first overlapping item is an image (and the next one is its associated text)
        overlapping_img_id = overlapping_items[0]
        overlapping_text_id = overlapping_items[1]
        
        # Get the text of the overlapping image
        overlapping_text = canvas.itemcget(overlapping_text_id, "text")
        current_text = canvas.itemcget(canvas.drag_data['text_id'], "text")
        
        print(f"{current_text} + {overlapping_text} = combined!")
        display_image(AI.combine_words(current_text, overlapping_text))


# Create main window
root = tk.Tk()
root.title("Combine words!")

# Entry widget for user input
entry = Entry(root, width=60)
entry.pack(pady=2)

# Button to fetch and display image
button = Button(root, text="Add Image", command=display_image)
button.pack(pady=2)

# Canvas to display and move the images
canvas = Canvas(root, bg="white", width=800, height=600)
canvas.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
canvas.image_dict = {}  # To store image references

starting_words = AI.add_starting_words()
for word in starting_words:
    display_image(word)

root.mainloop()

