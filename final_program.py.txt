import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw
import random
import math

def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def make_collage(image1, image2, new_directory):
    '''
    Combines two images side-by-side.
    '''
    # Stores dimensions of images.
    width1, height1 = image1.size
    width2, height2 = image2.size
    widths = [width1, width2]
    heights = [height1, height2]
    if sum(widths) > sum(heights): # If the widths are longer, join the images vertically.
        width = min(widths)
        if widths[0] == width:      # Resize image with larger width to match smaller width.
            heights[1] = heights[1]*widths[0]/widths[1]
            widths[1] = widths[0]
        else:
            heights[0] = heights[0]*widths[1]/widths[0]
            widths[0] = widths[1]
        height = sum(heights)       # New height is sum of old heights.
        image1 = image1.resize((widths[0],heights[0]))
        image2 = image2.resize((widths[1],heights[1]))
        canvas = PIL.Image.new('RGB', (width, height), 'white') # Creates blank canvas to place images on, and places images accordingly.
        canvas.paste(image1, (0,0))
        canvas.paste(image2, (0, heights[0]))
        return canvas
        
    else: # If the heights are longer, join the images horizontally.
        height = min(heights)
        if heights[0] == height:    # Resize image with larger height to match smaller height.
            widths[1] = widths[1]*heights[0]/heights[1]
            heights[1] = heights[0]
        else:
            widths[0] = widths[0]*heights[1]/heights[0]
            heights[0] = heights[1]
        width = sum(widths)     # New width is sum of old widths.
        image1 = image1.resize((widths[0],heights[0]))
        image2 = image2.resize((widths[1],heights[1]))
        canvas = PIL.Image.new('RGB', (width, height), 'white') # Creates blank canvas to place images on, and places images accordingly.
        canvas.paste(image1, (0,0))
        canvas.paste(image2, (widths[0],0))
        return canvas
            
        # Returns the PIL.Image of the combined images.

def make_collages(number_of_images=2, border_shape='rectangle', directory=None):
    """
    Creates multiple collages of any number of images given a directory of images.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'collages'
    new_directory = os.path.join(directory, 'collages')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    # Load all the images
    image_list, file_list = get_images(directory)
    
    random.shuffle(image_list) # Randomize order of images.
    
    j = int(math.log(number_of_images, 2)) # How many times to repeat combining phase.
    k = number_of_images-2**j # How many extra images that must be combined beforehand.
    image_sublist = []
    z=0 # Establishes iterator to track number of collages made.
    for n in range(len(image_list)/number_of_images):
        image_sublist.append(image_list[n*number_of_images:(n+1)*number_of_images]) # Group images to use for each collage.
    for images in image_sublist: # Make a collage for each group of images.
        z+=1
        k_images = images[:2*k] # Establish images to be combined beforehand.
        curr_images = images[2*k:] # Establish images to be combined in combining phase.
        for i in range(k):
            curr_images.append(make_collage(k_images[2*i],k_images[2*i+1],new_directory)) # Combine extra images before combining phase, and add them into the main group of images.
        random.shuffle(curr_images) # Shuffle main group of images before combining phase.
        while len(curr_images)>1: # Combining phase: Combine adjacent pairs of images until only one image is left.
            comb_images = []
            for j in range(len(curr_images)/2):
                comb_images.append(make_collage(curr_images[2*j],curr_images[2*j+1],new_directory))
            curr_images = comb_images
        print z
        collage = curr_images[0]
        width, height = collage.size
        mask = PIL.Image.new('RGBA', (width, height), (127,0,127,0))
        drawing_layer = PIL.ImageDraw.Draw(mask)
        if border_shape in ['oval','ellipse','circle']: # Draws oval mask.
            drawing_layer.ellipse((0,0, width, height), fill=(0,127,127,255))
        elif border_shape in ['diamond', 'rhombus']: # Draws diamond mask.
            drawing_layer.polygon([(width/2, 0), (0,height/2), (width/2, height), (width, height/2)], fill=(127,0,127,255))
        else: # Keeps original border shape (rectangle).
            drawing_layer.polygon([(0,0),(width,0),(width,height),(0,height)], fill=(127,0,127,255))
        result = PIL.Image.new('RGBA', collage.size, (0,0,0,0))
        result.paste(collage, (0,0), mask)
        new_image_filename = os.path.join(new_directory, 'collage' + str(z) + '.png') # Save final collage.
        result.save(new_image_filename)