# PWA Icons

This directory contains icons for the Progressive Web App.

## Required Icon Sizes

The manifest.json references the following icon sizes:
- 72x72
- 96x96
- 128x128
- 144x144
- 152x152
- 192x192 (required for PWA)
- 384x384
- 512x512 (required for PWA)

## Creating Icons

1. **Design Requirements:**
   - Use the Family Chores branding (purple gradient theme: #667eea to #f093fb)
   - Include a simple, recognizable symbol (e.g., checkmark, star, or chore-related icon)
   - Ensure readability at small sizes
   - Use transparent background for PNG files

2. **Recommended Tools:**
   - [PWA Asset Generator](https://github.com/onderceylan/pwa-asset-generator) - Automated icon generation
   - [RealFaviconGenerator](https://realfavicongenerator.net/) - Online tool
   - Adobe Illustrator, Figma, or similar design tools

3. **Quick Generation Command (if you have pwa-asset-generator installed):**
   ```bash
   npx pwa-asset-generator logo.svg static/icons --icon-only --background "#667eea"
   ```

4. **Manual Creation:**
   - Create a master icon at 1024x1024
   - Export to each required size
   - Name files as: `icon-{size}.png` (e.g., `icon-192x192.png`)

## Temporary Placeholder

Until custom icons are created, you can use a simple solid color placeholder or generate icons from a text-based design tool.

**Example using ImageMagick to create basic placeholders:**
```powershell
# Create purple gradient icons (requires ImageMagick)
foreach ($size in @(72, 96, 128, 144, 152, 192, 384, 512)) {
    magick -size ${size}x${size} gradient:"#667eea-#f093fb" "icon-${size}x${size}.png"
}
```

## Testing

After adding icons, test the PWA:
1. Open the app in Chrome/Edge
2. Check browser DevTools > Application > Manifest
3. Verify all icon sizes load correctly
4. Test "Add to Home Screen" functionality
