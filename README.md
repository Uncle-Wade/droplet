# Droplet
Software to analyze high speed video of droplets using python. This is related for senior design project 2025-6. Created by someone else, modified by Colton and Wade  

## Capabilities
The software can take an `.MOV` file, convert it to images, and give information on the sizes and speeds of particles detected in the image.  
TODO: more software capabilities go here  as we add them :)

## Usage
Dependencies: `numpy`, `scikit-image`, `matplotlib`, `imageio.v3`  

0. Take high speed video of your droplets. include 1cm physical scalebar. pixel measure it by hand. put the length value into the `PixelLength` variable so you get accurate droplet sizing
1. Convert your video to a bunch of still images using `Video_converter.py` and put them in a folder named `Test6_frames_tif_8bit` (the software does this automatically) (folder name will be changed in the future)  
2. Run either `Process_to_CSV.py` or `Process_and_Plot.py` depending on what you want. plot version is just csv version with plotting built into it (after future update, just use CSV one and plot seperately afterwards)
3. (after standalone plot update, not yet implemented) run `Plot.py` to get a plot

## Files  
`Test6_frames_tif_8bit` is the folder where your video will get split into images.  
`Process_and_Plot.py` is the version of the main runtime that analyzes the data and plots it. This will be split into 2 different files later. one process and one plot.  
`Process_to_CSV.py` is the main runtime and it dumps droplet data to CSV  
`Video_converter.py` dumps `.MOV` files into a sequence of `.TIFF` images in the test frames folder  
`Test6.mov` is the test data we have been using to test so far  

## TODO  
I (wade) need to:  
- [ ] separate plotting into another python program to make software faster and easier  
- [ ] do automatic naming for sucessive runs so that we dont have to rename a bunch of folders. the way the code works allows for one folder of TIFFs to be used at once and I want more and to select from them (think a `11-2-25-run1` folder/video and more from that day all playing nice in the same directory)  
- [ ] integrate framerate into the software so that we can get particle speeds  
- [ ] find a way to account for the sheet  
- [ ] plot droplet distribution  
- [ ] explore frame scaling to see if data can be enhanced with scalers (i think by scalers's nature this may be a fools errand)
- [ ] add white point and black point adjustments so that lighting conditions can be accounted for.  
- [ ] add a cool video/photo to the README so people like it better
- [ ] fix scalebar
- [ ] plane charactateristics
- [ ] try to anticipate the sheet when it's time for that
- [ ] get the better camera in on this.
