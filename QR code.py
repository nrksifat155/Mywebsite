import qrcode  # Importing the qrcode library to generate QR codes
from PIL import Image, ImageDraw, ImageFont  # Importing necessary modules from PIL (Pillow) for image handling and text drawing

# =================== CONFIGURATION SECTION ===================
QR_CONFIG = {  # Configuration dictionary for the QR code properties
    "version": 5,  # Defines the version (size) of the QR code, where higher version = larger QR
    "box_size": 18,  # Defines the size of each individual box in the QR code
    "border_size_ratio": 0.03,  # Defines the ratio of the border size relative to the QR code
    "fill_color": "black",  # The color of the filled boxes in the QR code
    "bg_color": "white",  # Background color of the QR code
    "border_color": "green"  # Border color of the QR code
}

TEXT_BOX_CONFIG = {  # Configuration dictionary for the text box that will be placed below the QR code
    "width_ratio": 0.15,  # Width of the text box relative to the QR code size
    "height_ratio": 0.05,  # Height of the text box relative to the QR code size
    "color": "white",  # Background color of the text box
    "content": "NRKS",  # Text content that will be displayed in the text box
    "text_color": "black",  # Color of the text inside the text box
    "font_path": "BebasNeue-Regular.ttf",  # Path to the font file for the text
    "font_scaling": 0.7,  # Scaling factor for font size relative to the text box height
    "padding": 5,  # Padding inside the text box
    "border_color": "black",  # Border color of the text box
    "border_width": 0  # Border width around the text box
}

# =================== QR CODE GENERATION ===================
def generate_qr_code(data):  # Function to generate a QR code with the provided data
    qr = qrcode.QRCode(  # Create a new QRCode object
        version=QR_CONFIG["version"],  # Set the QR version
        box_size=QR_CONFIG["box_size"],  # Set the size of each box
        border=1  # Set the border size to 1 box
    )
    qr.add_data(data)  # Add the data to the QR code
    qr.make(fit=True)  # Optimize the QR code to fit the data
    # Generate the image with specified fill and background colors, then convert to 'RGB'
    return qr.make_image(fill_color=QR_CONFIG["fill_color"], back_color=QR_CONFIG["bg_color"]).convert('RGB')

# =================== CREATE QR WITH BORDER AND TEXT ===================
def create_qr_with_border(qr_image):  # Function to add border and text box around the QR code image
    border_size = int(qr_image.size[0] * QR_CONFIG["border_size_ratio"])  # Calculate border size based on the image size
    
    # Create a new image for the bordered QR code
    bordered_image = Image.new('RGB', 
                               (qr_image.size[0] + 2 * border_size, qr_image.size[1] + 2 * border_size),  # Create new image with extra border
                               QR_CONFIG["border_color"])  # Set the background color to the border color
    bordered_image.paste(qr_image, (border_size, border_size))  # Paste the original QR code into the center of the bordered image

    draw = ImageDraw.Draw(bordered_image)  # Create a drawing object to add shapes or text

    # Calculate text box dimensions based on the QR code size and the ratio specified
    box_width = int(qr_image.size[0] * TEXT_BOX_CONFIG["width_ratio"])  
    box_height = int(qr_image.size[1] * TEXT_BOX_CONFIG["height_ratio"])
    # Calculate position of the text box (centered relative to the QR code)
    box_x = (bordered_image.size[0] - box_width) // 2
    box_y = (bordered_image.size[1] - box_height) // 2

    # Draw the rectangle for the text box
    draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill=TEXT_BOX_CONFIG["color"])

    # Load the font with a size based on the text box height
    font_size = int(box_height * TEXT_BOX_CONFIG["font_scaling"])
    font = ImageFont.truetype(TEXT_BOX_CONFIG["font_path"], font_size) if font_size > 0 else ImageFont.load_default()

    # Calculate the bounding box of the text to center it within the text box
    text_bbox = draw.textbbox((0, 0), TEXT_BOX_CONFIG["content"], font=font)
    # Calculate the text's x and y position to be centered within the text box
    text_x = box_x + (box_width - (text_bbox[2] - text_bbox[0])) // 2
    text_y = box_y + (box_height - (text_bbox[3] - text_bbox[1])) // 2

    # Apply padding to the text position
    text_x = max(text_x, box_x + TEXT_BOX_CONFIG["padding"])
    text_y = max(text_y, box_y + TEXT_BOX_CONFIG["padding"])

    # Draw the text inside the text box
    draw.text((text_x, text_y), TEXT_BOX_CONFIG["content"], fill=TEXT_BOX_CONFIG["text_color"], font=font)

    # Draw a border around the text box (optional)
    draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], 
                   outline=TEXT_BOX_CONFIG["border_color"], width=TEXT_BOX_CONFIG["border_width"])

    return bordered_image  # Return the final image with border and text box

# =================== MAIN EXECUTION ===================
if __name__ == "__main__":  # Main execution block
    qr_data = 'I Love You'  # Data to encode in the QR code
    qr_img = generate_qr_code(qr_data)  # Generate the QR code image
    final_img = create_qr_with_border(qr_img)  # Create the final QR code image with border and text

    final_img.save("qr_code_optimized.png")  # Save the generated image as 'qr_code_optimized.png'
 
