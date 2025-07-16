# """Store and retrive images from postgress."""
# import psycopg2
# from pathlib import Path


# from pdf2image import convert_from_path
# import pytesseract
# from PIL import Image
# import os

# # Convert PDF to images
# pdf_path = r"C:\Education Project Data\Chemistry\Chemistry.pdf"
# images = convert_from_path(pdf_path)

# # Extract text from each page
# for i, image in enumerate(images):
#     # Save image temporarily (optional)
#     image.save(f"C:\\Users\\mysel\\project\\EducationBot\\chemistry\\page_{i}.png", "PNG")
#     # Perform OCR
#     text = pytesseract.image_to_string(Image.open(f"C:\\Users\\mysel\\project\\EducationBot\\chemistry\\page_{i}.png"))
#     print(f"Page {i+1} text:\n{text}\n")
#     # Optionally, save text to a file
#     with open(f"C:\\Users\\mysel\\project\\EducationBot\\chemistry\\page_{i}.txt", "w") as text_file:
#         text_file.write(text)
#     # Clean up temporary image
#     os.remove(f"C:\\Users\\mysel\\project\\EducationBot\\chemistry\\page_{i}.png")














# # from spire.pdf.common import *
# # from spire.pdf import *

# # # Create a PdfDocument object
# # doc = PdfDocument()

# # # Load a PDF document
# # doc.LoadFromFile(r"C:\Users\mysel\project\Physics\Book9\Physics_9_Modified.pdf")

# # # Get a specific page
# # page = doc.Pages[6]

# # # Create a PdfTextExtractor object
# # textExtractor = PdfTextExtractor(page)

# # # Create a PdfTextExtractOptions object
# # extractOptions = PdfTextExtractOptions()

# # # Set IsExtractAllText to Ture
# # extractOptions.IsExtractAllText = True

# # # Extract text from the page keeping white spaces
# # text = textExtractor.ExtractText(extractOptions)

# # # Write text to a txt file 
# # with open('TextOfPageSix.txt', 'w') as file:
# #     lines = text.split("\n")
# #     for line in lines:
# #         if line != '':
# #             file.write(line)
# # doc.Close()
# # from spire.pdf import PdfDocument, PdfImageHelper

# # # Create a PdfDocument instance
# # pdf = PdfDocument()

# # # Load a PDF file
# # pdf.LoadFromFile("C:/Users/mysel/project/Chemistry/Chemistry.pdf")

# # # Create a PdfImageHelper instance
# # imageHelper = PdfImageHelper()

# # # Iterate through the pages in the document
# # for i in range(0, pdf.Pages.Count):
# #     # Get the current page
# #     page = pdf.Pages.get_Item(i)
# #     # Get the image information of the page
# #     imageInfo = imageHelper.GetImagesInfo(page)
# #     # Iterate through the image information items
# #     for j in range(0, len(imageInfo)):
# #         # Save the current image to file
# #         imageInfo[j].Image.Save(f"C:\\Users\\mysel\\project\\EducationBot\\Image{i}_{j}.png")

# # # Release resources
# # pdf.Close()

# # file = 

# # # open the file
# # pdf_file = fitz.open(file)

# # # STEP 3
# # # iterate over PDF pages
# # for page_index in range(len(pdf_file)):

# #     # get the page itself
# #     page = pdf_file.load_page(page_index)  # load the page
# #     image_list = page.get_images(full=True)  # get images on the page

# #     # printing number of images found in this page
# #     if image_list:
# #         print(f"[+] Found a total of {len(image_list)} images on page {page_index}")
# #     else:
# #         print("[!] No images found on page", page_index)
    
# #     for image_index, img in enumerate(image_list, start=1):
# #         # get the XREF of the image
# #         xref = img[0]

# #         # extract the image bytes
# #         base_image = pdf_file.extract_image(xref)
# #         image_bytes = base_image["image"]

# #         # get the image extension
# #         image_ext = base_image["ext"]

# #         # save the image
# #         image_name = f"image{page_index+1}_{image_index}.{image_ext}"
# #         with open(image_name, "wb") as image_file:
# #             image_file.write(image_bytes)
# #             print(f"[+] Image saved as {image_name}")


# def store_images_in_podtgress(path:str)->None:
#     """Store images along in postgress db."""

#     conn = psycopg2.connect(
#         dbname="postgres",
#         user="postgres",
#         password="HelloWorld1!",
#         host="localhost",  # or your server
#         port="5432"
#     )
#     cur = conn.cursor()

#     # Read image as binary
#     folder = Path(path)

#     for file in folder.iterdir():
#         if file.is_file():
#             with file.open("rb",encoding="utf-8") as f:
#                 content = f.read()
#                 cur.execute("INSERT INTO image.img (name, data) VALUES (%s, %s)", (file.name, psycopg2.Binary(content)))
#                 conn.commit()

#     cur.close()
#     conn.close()
#     print("Image inserted successfully.")

# from pathlib import Path
# def image_extraction_regex(text:str):
#         """extract image form the code."""
#         import re
#         image_str = r'C:\Users\mysel\Pictures\Screenshots\Physics\test'
#         image_folder =Path('C:\\Users\\mysel\\Pictures\\Screenshots\\Physics\\test')
#         matches = re.findall(r'\b[Ff]igure\s+\d+(?:\.\d+)?\b', text)
        
#         if len(matches)>0:
#             for image in matches:
#                 for file in image_folder.iterdir():
#                     if file.is_file() :
                       
#                         if file.name.lower().replace(' ','')==image.lower().replace(' ','')+'.png':
#                             image_path = image_str+"\\"+file.name
#                             print(image_path)




# # Example usage
# # store_images_in_podtgress("C:\\Users\\mysel\\Pictures\\Screenshots\\Physics\\Book9_2")
# # image_extraction_regex("""### Working of Screw Gauge

# # A **screw gauge**, also known as a micrometer screw gauge, is a precision instrument used to measure small lengths with greater accuracy than a Vernier caliper. Here’s how it works, along with an illustration.

# # #### Components of a Screw Gauge
# # 1. **U-shaped Metal Frame:** Holds the other components.
# # 2. **Stud:** A metal stud is fixed at one end of the frame.
# # 3. **Hollow Cylinder (Sleeve):** It has a millimeter scale marked on it and acts as a nut.
# # 4. **Thimble:** Contains a threaded spindle that moves as the thimble rotates.
# # 5. **Circular Scale:** Divided into 100 parts, for finer measurement.

# # ![Figure 1.9: A micrometer screw gauge](https://example.com/screw_gauge_image.png)

# # - As the thimble completes one full rotation, the spindle moves 1 mm along the index line, and each division on the circular scale corresponds to 0.01 mm.

# # #### Steps to Use a Screw Gauge
# # 1. **Zero Error Determination:**
# #    - Close the gap between the stud and spindle.
# #    - Check if the zero of the circular scale aligns with the index line. If not, calculate the zero error.

# # 2. **Measurement Procedure:**
# #    - Open the gap using the ratchet and place the object (e.g., wire) between the stud and spindle.
# #    - Gently turn the ratchet until the object is firmly held.
# #    - Read the main scale and circular scale to find the diameter of the object.
# #    - Apply any zero error correction to obtain the accurate measurement.

# # #### Example Calculation
# # If the main scale reading is 1 mm and the circular scale reading (85 divisions) is noted:
# # - Circular scale reading = 85 × 0.01 mm = 0.85 mm
# # - Observed diameter = Main scale reading + Circular scale reading = 1 mm + 0.85 mm = 1.85 mm
# # - Apply zero correction if any, to finalize the measurement.

# # ### Conclusion
# # The least count of a screw gauge is 0.01 mm, making it more precise than other measurements tools like the Vernier calipers. Measurements taken with a screw gauge are crucial in experimental physics due to their accuracy.

# # #### Sources
# # - Chapter: Physical Quantities and Measurement, Pages 13-15.""")