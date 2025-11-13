# droplet
Software to analyze high speed video of droplets using python. This is related for senior design project 2025-6. Created by someone else, modified by Colton and Wade  

## Capabilities
The software can take an `.MOV` file, convert it to images, and give information on the sizes and speeds of particles detected in the image.  
TODO: more software capabilities go here  

## Usage
Dependencies: `numpy`, `scikit-image`, `matplotlib`, `imageio.v3`  
0. take high speed video of your droplets. include 1cm physical scalebar. pixel measure it by hand. put the length value into the `PixelLength` variable so you get accurate droplet sizing
1. Convert your video to a bunch of still images. the code to convert the `.MOV` files out of the camera to `.TIFF` stills will be uploaded later  
2. Put them in a folder named `Test6_frames_tif_8bit` They should be `.TIFF` images (the folder name can be changed in code)  
3. Run either format.py or plot.py depending on what you want. plot.py is just format with plotting built onto it

## Files
TODO: Overview of what files do what will go here
