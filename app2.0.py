import os
import random

import tkinter as tk
from PIL import Image, ImageTk

WINDOW_TITLE = "My Wardrobe"
WINDOW_HEIGHT = 770
WINDOW_WIDTH = 350
IMG_HEIGHT_BOTTOMS = 350
IMG_HEIGHT_TOPS = 250
IMG_WIDTH = 250
BEIGE_COLOR_HEX = '#E3C396'

# Store all Tops and Bottoms into a file we can access
ALL_TOPS = [str('tops/') + file for file in os.listdir('tops') if not file.startswith('.')]
ALL_PANTS = [str('Pants/') + file for file in os.listdir('Pants') if not file.startswith('.')]
ALL_SKIRTS = [str('Skirts/') + file for file in os.listdir('Skirts') if not file.startswith('.')]

class WardrobeApp:

    def __init__(self, root):
        self.root = root

        # collect all tops and bottoms
        self.top_images = ALL_TOPS
        self.pant_images = ALL_PANTS
        self.skirt_images = ALL_SKIRTS

        # first pictures
        self.top_image_path = self.top_images[0]
        self.bottom_image_path = self.skirt_images[0]


        # creating 2 frames
        self.tops_frame = tk.Frame(self.root, bg=BEIGE_COLOR_HEX)
        self.bottoms_frame = tk.Frame(self.root, bg=BEIGE_COLOR_HEX)

        # add tops
        self.top_image_label = self.create_photo(self.top_image_path, self.tops_frame, IMG_WIDTH, IMG_HEIGHT_TOPS)
        self.top_image_label.pack(side=tk.TOP)

        # add bottoms
        self.bottom_image_label = self.create_photo(self.bottom_image_path, self.bottoms_frame, IMG_WIDTH, IMG_HEIGHT_BOTTOMS)
        self.bottom_image_label.pack(side=tk.TOP)

        # create background
        self.create_background()


    def create_background(self):
        """
        Create background for app:

        Includes: Window, Buttons, Clothing
        """
        # title to window and resize
        self.root.title(WINDOW_TITLE)
        self.root.geometry('{0}x{1}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

        # add buttons
        self.create_buttons()

        # add clothing
        self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.bottoms_frame.pack(fill=tk.BOTH, expand=tk.YES)


    def create_photo(self, image, frame, width, height):
        """

        :param image: image of clothing
        :param frame: app frame
        :param width: width of clothing image
        :param height: height of clothing image
        :return: specific image in frame
        """
        image_file = Image.open(image)
        image_resized = image_file.resize((width, height), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)
        image_label = tk.Label(frame, image=tk_photo, anchor=tk.CENTER)
        image_label.image = tk_photo

        # so we can add later
        return image_label


    def create_buttons(self):
        # next and prev buttons for tops
        top_prev_button = tk.Button(self.tops_frame, text="Previous", command=self.get_prev_top)
        top_prev_button.pack(side=tk.LEFT)

        top_next_button = tk.Button(self.tops_frame, text="Next", command=self.get_next_top)
        top_next_button.pack(side=tk.RIGHT)

        # change to pants/skirts buttons
        change_to_pants = tk.Button(self.bottoms_frame, text="Pants", command=self.bottoms_to_pants)
        change_to_pants.pack(side=tk.LEFT)

        change_to_skirts = tk.Button(self.bottoms_frame, text="Skirts", command=self.bottoms_to_skirts)
        change_to_skirts.pack(side=tk.RIGHT)

        # next and prev buttons for bottoms
        bottom_prev_button = tk.Button(self.bottoms_frame, text="Previous", command=self.get_prev_bottom)
        bottom_prev_button.pack(side=tk.LEFT)

        bottom_next_button = tk.Button(self.bottoms_frame, text="Next", command=self.get_next_bottom)
        bottom_next_button.pack(side=tk.RIGHT)


    def bottoms_to_pants(self):
        self.bottom_image_path = self.pant_images[1]
        self.update_image(self.pant_images[1], self.bottom_image_label, IMG_WIDTH, IMG_HEIGHT_BOTTOMS)
        self.rand_outfit()

    def bottoms_to_skirts(self):
        self.bottom_image_path = self.skirt_images[0]
        self.update_image(self.skirt_images[1], self.bottom_image_label, IMG_WIDTH, IMG_HEIGHT_BOTTOMS)
        self.rand_outfit()

    def _get_next_item(self, current_item, category, increment=True):
        """ Gets the Next Item In a Category depending on if you hit next or prev
        Args:
            current_item, str
            category, list
            increment, boolean
        """
        item_index = category.index(current_item)
        final_index = len(category) - 1
        next_index = 0

        if increment and item_index == final_index:
            next_index = 0  # cycle back to the beginning
        elif not increment and item_index == 0:
            next_index = final_index  # cycle back to the end
        else:
            incrementor = 1 if increment else -1
            next_index = item_index + incrementor

        next_image = category[next_index]

        # reset the image object
        if current_item in self.top_images:
            image_label = self.top_image_label
            self.top_image_path = next_image
            height = IMG_HEIGHT_TOPS
        else:
            image_label = self.bottom_image_label
            self.bottom_image_path = next_image
            height = IMG_HEIGHT_BOTTOMS

        # update the photo
        self.update_image(next_image, image_label, IMG_WIDTH, height)

    def get_next_top(self):
        self._get_next_item(self.top_image_path, self.top_images, increment=True)

    def get_prev_top(self):
        self._get_next_item(self.top_image_path, self.top_images, increment=False)

    def get_next_bottom(self):
        if self.bottom_image_path in self.pant_images:
            self._get_next_item(self.bottom_image_path, self.pant_images, increment=False)
        else:
            self._get_next_item(self.bottom_image_path, self.skirt_images, increment=True)

    def get_prev_bottom(self):
        if self.bottom_image_path in self.pant_images:
            self._get_next_item(self.bottom_image_path, self.pant_images, increment=True)
        else:
            self._get_next_item(self.bottom_image_path, self.skirt_images, increment=False)


        # reset and update image
    def update_image(self, new_image, image_label, width, height):
        # collect and change image into tk photo obj
        new_image_file = Image.open(new_image)
        image = new_image_file.resize((width, height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo

    def rand_outfit(self):
        # randomly select an outfit
        new_top_index = random.randint(0, len(self.top_images)-1)
        if self.bottom_image_path in self.pant_images:
            new_bottom_index = random.randint(0, len(self.pant_images)-1)
        else:
            new_bottom_index = random.randint(0, len(self.skirt_images)-1)

        # add the clothes onto the screen
        self.update_image(self.top_images[new_top_index], self.top_image_label, IMG_WIDTH, IMG_HEIGHT_TOPS)
        if self.bottom_image_path in self.pant_images:
            self.update_image(self.pant_images[new_bottom_index], self.bottom_image_label,IMG_WIDTH, IMG_HEIGHT_BOTTOMS)
        else:
            self.update_image(self.skirt_images[new_bottom_index], self.bottom_image_label,IMG_WIDTH, IMG_HEIGHT_BOTTOMS)




if __name__ == '__main__':
    root = tk.Tk()
    app = WardrobeApp(root)

    root.mainloop()
