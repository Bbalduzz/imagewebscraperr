import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from natsort import natsorted

notvalid = True
while notvalid:	# request a url until a valid one is typed
    url = input('>> Enter the url of the site with the images: ')
    for i in url:
        if 'https' in url or 'http' in url:
            notvalid = False
            break
    if notvalid:
        print("Url inserted is not valid! Please insert a correct one")

file_path = input('>> Enter the file path: ')
if os.path.isdir(file_path):
    pass
else:
    os.mkdir(file_path)
    print('>>>',file_path,'does not exsist, created and using it')

common_char = input('>> Enter the common characteristic of the url: ') # a character common in every url of the images you want
choosename = input('>> How do you want to name the images: ')
Pdf_choose = input('>> Do you want to merge all the images in a singular PDF? (Y/n): ')
name = choosename
print('=== Folder chosen ===\n', file_path)

# beginnig webscraping
page = requests.get(url)
print('=== Website ===\n',url)
soup = BeautifulSoup(page.content, 'html.parser')
images = soup.find_all('img')

print('=== Images Found ===')
#trovo le immagini giuste e le scarico nella giusta cartella
a = 1
for img in images:
    if img.has_attr('src'):
        if common_char in img['src']:
            imgUrl = img['src']
            print(imgUrl)
            img_data = requests.get(imgUrl).content
            with open(f'{file_path}{name}%s.jpg' %a, 'wb') as handler:
                handler.write(img_data)
                print('page saved')
            a = a+1

#creo il pdf con le immagini
if Pdf_choose == 'y' or Pdf_choose == '':

    pdf_name = input('>> How do you want to name the pdf: ')
    file_names = os.listdir(file_path)
    file_names = natsorted(file_names) #Python doesn't have a built-in way to have natural sorting so I needed to import a specific library to do it


    pdfimages = [
        Image.open(file_path + f)
        for f in file_names
    ]
    print('=== Images used to create the PDF ===\n' +'>>> '+str(file_names))

    pdf_path = file_path + pdf_name + '.pdf'

    pdfimages[0].save(
        pdf_path, "PDF" , resolution=100.0, save_all=True, append_images=pdfimages[1:]
    )
    print('=== PDF created and saved! ===')
    print('=== Check ===\n' +'>>> '+str(file_path))
    
    #elimino le immagini se l'utente lo desidera
    Delete_img = input('>> Do you want to delete all images after the pdf is created? (Y/n): ')
    if Delete_img == 'y' or Delete_img == '':
        for i in range(len(file_names)):
            if '.jpg' in file_names[i] or '.png' in file_names[i]:
                deleted_img = os.path.join(file_path, file_names[i])
                os.remove(deleted_img)
                print(file_names[i]+' deleted')
        print('=== images deleted ===')
    else:
        print("=== images not deleted ===")
else:
    print('=== PDF not created ===')

