# Creating an Icon for Your Unraid Container

Your Unraid container will look more professional with a custom icon. Here's how to add one.

## Icon Requirements

- **Format**: PNG (recommended) or JPG
- **Size**: 200x200 pixels minimum (512x512 recommended)
- **Aspect Ratio**: Square (1:1)
- **File Name**: `icon.png`
- **Location**: Root of your GitHub repository

## Quick Options

### Option 1: Use a Movie/Plex Related Icon

1. **Search for free icons**:
   - https://www.flaticon.com/ (search "movie" or "film reel")
   - https://www.iconfinder.com/ (search "plex" or "cinema")
   - https://icons8.com/ (search "movie")

2. **Download as PNG**
   - Choose 512x512 size
   - Save as `icon.png`

3. **Add to repository**:
   ```bash
   # Place icon.png in project root
   git add icon.png
   git commit -m "Add container icon"
   git push
   ```

### Option 2: Create Custom Icon

**Using Canva (Free)**:
1. Go to https://www.canva.com/
2. Create design → Custom dimensions → 512x512
3. Design your icon (use movie/film elements)
4. Download as PNG
5. Rename to `icon.png`
6. Add to repository

**Using GIMP (Free)**:
1. Download GIMP: https://www.gimp.org/
2. File → New → 512x512
3. Design your icon
4. Export as PNG
5. Save as `icon.png`
6. Add to repository

### Option 3: AI-Generated Icon

**Using DALL-E or similar**:
1. Prompt: "A simple icon for a movie selector app, minimalist design, film reel and randomizer symbol"
2. Generate image
3. Download and resize to 512x512
4. Save as `icon.png`
5. Add to repository

### Option 4: Use Placeholder

A simple colored square with text:

**Python script to create placeholder**:
```python
from PIL import Image, ImageDraw, ImageFont

# Create image
img = Image.new('RGB', (512, 512), color='#e5a00d')
draw = ImageDraw.Draw(img)

# Add text
try:
    font = ImageFont.truetype("arial.ttf", 100)
except:
    font = ImageFont.load_default()

text = "PLEX\nMOVIE"
draw.text((256, 256), text, fill='#1f1f1f', font=font, anchor='mm', align='center')

# Save
img.save('icon.png')
print("Icon created: icon.png")
```

Run this script and it creates a simple icon with text.

## Icon Color Suggestions

To match your app's theme:
- **Primary**: `#e5a00d` (gold/orange)
- **Background**: `#1f1f1f` (dark gray)
- **Accent**: `#282828` (medium gray)

## After Creating Icon

1. **Save as `icon.png`** in project root

2. **Verify size**:
   ```bash
   # Check image dimensions
   file icon.png
   # Should show 512x512 or larger
   ```

3. **Add to Git**:
   ```bash
   git add icon.png
   git commit -m "Add container icon"
   git push
   ```

4. **Verify URL works**:
   ```
   https://raw.githubusercontent.com/YOURUSERNAME/plex-movie-selector/main/icon.png
   ```
   - Should display the icon in your browser

5. **Update in Unraid**:
   - Docker tab → Edit container
   - Icon URL should already be set from template
   - Force Update to refresh

## Troubleshooting

### Icon not showing in Unraid

1. **Clear browser cache**: Ctrl+F5
2. **Check file exists**: View your GitHub repository, see if icon.png is there
3. **Test raw URL**: Access the raw GitHub URL in browser
4. **Verify XML template**: Icon URL should point to raw.githubusercontent.com

### Icon appears but wrong size

- Unraid will scale it, but 512x512 looks best
- Too small = pixelated
- Too large = unnecessary file size

### Icon shows broken image

- File might not be PNG
- File might be corrupted
- URL might be wrong in template
- Repository might be private

## Example Icons

Good examples for a Plex movie selector:
- 🎬 Film reel
- 🎲 Dice (for randomization)
- 🎥 Movie camera
- 📽️ Projector
- 🍿 Popcorn
- 🎞️ Film strip
- Combination of movie icon + shuffle/random symbol

## Icon Generator Tools

Free online tools:
- **Favicon Generator**: https://favicon.io/ (can create simple icons)
- **Icons8**: https://icons8.com/ (tons of free icons)
- **Flaticon**: https://www.flaticon.com/ (free icon collections)
- **App Icon Generator**: https://appicon.co/ (resize to multiple sizes)

## Best Practices

1. **Keep it simple**: Icons should be recognizable at small sizes
2. **Use solid colors**: Avoid gradients for better clarity
3. **Square design**: Center your design in the square
4. **High contrast**: Dark icon on light background or vice versa
5. **PNG format**: Better transparency support than JPG
6. **Reasonable file size**: Under 100KB for fast loading

## Without an Icon

If you don't want to create an icon:
1. Remove or comment out `<Icon>` line in `plex-movie-selector.xml`
2. Unraid will use a default Docker icon
3. Still works perfectly fine!

---

**Recommendation**: Even a simple icon makes your container look more professional. Use Option 1 (find a free icon) for the quickest solution!
