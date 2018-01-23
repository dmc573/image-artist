import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw
import random

def make_collage(original_image):
    return original_image

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

def make_collages(number_of_images=2, border_shape='rectangle', filter_color='random', directory=None):
    """ 
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'framed'
    new_directory = os.path.join(directory, 'collages')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    # Load all the images
    image_list, file_list = get_images(directory)
    
    random.shuffle(image_list)
    
    # Go through the images and save modified versions
    for n in range(len(image_list)/number_of_images):
        
        # Round the corners with default percent of radius
        make_collage(image_list[2*n],image_list[2*n+1],n,new_directory)
            
def make_collage(image1, image2, n, new_directory):
    width1, height1 = image1.size
    width2, height2 = image2.size
    widths = [width1, width2]
    heights = [height1, height2]
    if sum(widths) > sum(heights): #vertical
        width = min(widths)
        if widths[0] == width:
            heights[1] = heights[1]*widths[0]/widths[1]
            widths[1] = widths[0]
        else:
            heights[0] = heights[0]*widths[1]/widths[0]
            widths[0] = widths[1]
        height = sum(heights)
        image1 = image1.resize((widths[0],heights[0]))
        image2 = image2.resize((widths[1],heights[1]))
        canvas = PIL.Image.new('RGB', (width, height), 'white')
        canvas.paste(image1, (0,0))
        canvas.paste(image2, (0, heights[0]))
        new_image_filename = os.path.join(new_directory, 'collage' + str(n+1) + '.png')
        canvas.save(new_image_filename)
        print n
        
    else: #horizontal
        height = min(heights)
        if heights[0] == height:
            widths[1] = widths[1]*heights[0]/heights[1]
            heights[1] = heights[0]
        else:
            widths[0] = widths[0]*heights[1]/heights[0]
            heights[0] = heights[1]
        width = sum(widths)
        image1 = image1.resize((widths[0],heights[0]))
        image2 = image2.resize((widths[1],heights[1]))
        canvas = PIL.Image.new('RGB', (width, height), 'white')
        canvas.paste(image1, (0,0))
        canvas.paste(image2, (widths[0],0))
        new_image_filename = os.path.join(new_directory, 'collage' + str(n+1) + '.png')
        canvas.save(new_image_filename)
        print n
            
        # Save the altered image, suing PNG to retain transparency
        