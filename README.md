# Logo Placer
Sure you can use an image editing software like Photoshop or GIMP to place a logo on a background image, but when you have a lot of image to process, it can be a pain and take a lot of time to do it manually. 

Logo Placer is a simple tool to help mitigate this pain. Create a logo profile then simply upload all the images you want to process and click generate. It may take a moment but all the images will have the logo applied to them and saved to your desired location. 

## How to Use

### Logo Profile

To create a logo profile, go to the Logos tab and select New Logo from the dropdown. Name your logo profile, upload the logo image, set the position, padding, scale, and final image resolution.

details:
- Logo Name: The name of your logo profile and how it will appear in any dropdowns
- Logo: the image of your logo, this is saved as a path to the image so if you move the image, the logo profile must be updated as well
- Position: this is the base position of the logo on the image, top left, top right, bottom left, or bottom right
- Padding: this is the amount of space between the logo and the closest edges of the image, the default is 0, so the logo will start flush wit the corner position you selected
- Scale: this is the scale of the logo relative to the image. Scaling is done in refernce to the logo and image's height, so setting the scale to 1.0 will make the logo the same height as the image, but maintain it's ascpect ratio.
- Resolution: this is the final resolution of the image you are pasting the logo onto. Uploaded images are scaled and cropped to this resolution to maintain the bulk of the image and not stretch it.

### Placing Logos

1) Once you have created a logo profile, you can upload images to be processed. Go to the Generate tab and click the Upload button to select any images you want to process. You can upload multiple images at once to apply the logo profile to all of them. The application currently supports png, jpg, jpeg, avif, and webp images but will only output jpg.

2) Select the logo profile you want to apply to the images you uploaded.

3) Click the Generate button and select the directory where you want the processed images to be saved.