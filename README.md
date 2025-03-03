# **Sign Language Dataset Generator**

This program extracts **hand images from videos** and converts them into a **picture dataset**. It processes video files, detects hands, and saves cropped hand images as **PNG files** (or other formats).  

## **Features**  
✅ Extracts hands from **videos or live webcam feeds**  
✅ Supports multiple video formats: **MP4, AVI, MOV, MKV, WMV**  
✅ Allows **custom padding, flipping, and extraction timing**  
✅ Saves images in a structured dataset format  

## **Demo**  

![Demo GIF](demo.gif)  

## **Sample Output Images**  

Here are some extracted hand images from the processed videos:  

<table align="center">
  <tr>
    <td><img src="output_images/test1/0.png" width="100"></td>
    <td><img src="output_images/test1/3.png" width="100"></td>
    <td><img src="output_images/test1/5.png" width="100"></td>
    <td><img src="output_images/test1/7.png" width="100"></td>
    <td><img src="output_images/test1/8.png" width="100"></td>
  </tr>
  <tr>
    <td><img src="output_images/test1/10.png" width="100"></td>
    <td><img src="output_images/test1/15.png" width="100"></td>
    <td><img src="output_images/test1/20.png" width="100"></td>
    <td><img src="output_images/test1/23.png" width="100"></td>
    <td><img src="output_images/test1/30.png" width="100"></td>
  </tr>
</table>

## **Settings**  

Modify these parameters in the script to adjust extraction behavior:  

```python
height_width = 100        # Output image size (square format)
output_format = "png"     # File format of extracted images
buffer = 5                # Padding (%) around the hand
flipped = True            # Flip video horizontally
start_extraction = 1.5    # Seconds before extraction begins
num_sec = 2.5             # Duration of extraction in seconds
```

## **How to Use**  

### **Processing Videos**  
1. Place the videos you want to process inside the **`input_videos`** folder.  
2. The output images will be saved in **`output_images`**, inside a folder named after the input video filename (without the extension).  

For example:  
- Input video: `input_videos/example.mp4`  
- Extracted images will be stored in: `output_images/example/`  

### **Run the Extraction**  

- **Process a specific video:**  
  ```python
  process("example.mp4")
  ```
- **Process all videos in the `input_videos` folder:**  
  ```python
  process_all()
  ```
- **Use a webcam instead of a video file:**  
  ```python
  process()
  ```

## **Installation & Dependencies**  

1. Clone the repository:  
   ```sh
   git clone https://github.com/UPD-IM-FSL-Project/Sign-Language-Dataset-Generator
   cd Sign-Language-Dataset-Generator
   ```
2. Install required dependencies:  
   ```sh
   pip install -r requirements.txt
   ```
3. Run the program:  
   ```sh
   python extract.py
   ```
## **Credits**  
The following videos were used for testing:  
- **test1.mp4**: [YouTube Link](https://www.youtube.com/watch?v=xmMKH_R2HAE)  
- **test2.mp4**: [YouTube Link](https://www.youtube.com/watch?v=wihY-cSsoRg)  
- **test3.mp4**: [YouTube Link](https://www.youtube.com/watch?v=8OqOMV-f6hA)  
