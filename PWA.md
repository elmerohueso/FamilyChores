# Progressive Web App (PWA) Implementation

Family Chores is now a Progressive Web App, enabling installation on mobile and desktop devices for an app-like experience.

## What's New

### PWA Features
- **Install to Home Screen/Desktop** - Add the app to your device like a native app
- **Offline Support** - Access cached pages when internet is unavailable
- **App-like Experience** - Runs in standalone mode without browser chrome
- **Fast Loading** - Aggressive caching for instant subsequent loads
- **App Shortcuts** - Quick access to Record Chore and Dashboard (on supported devices)

### Technical Implementation

**New Files:**
- `static/manifest.json` - Web app manifest defining app metadata and icons
- `static/sw.js` - Service worker handling offline caching and PWA lifecycle
- `static/icons/` - App icons in multiple sizes (72x72 to 512x512)
- `scripts/generate_pwa_icons.py` - Icon generator script
- `scripts/generate_pwa_icons.ps1` - PowerShell wrapper for icon generation

**Modified Files:**
- `templates/_head_includes.html` - Added manifest link, theme-color meta tag, and apple-touch-icon
- `static/js/utils.js` - Added service worker registration and install prompt handling
- `Dockerfile` - Ensures icons directory exists in container

## Installation

### For Users

#### Mobile (iOS/Android)
1. Open Family Chores in Safari (iOS) or Chrome/Edge (Android)
2. Look for "Add to Home Screen" option:
   - **iOS:** Tap share icon → "Add to Home Screen"
   - **Android:** Tap menu (⋮) → "Add to Home Screen" or look for install banner
3. Confirm installation
4. App icon appears on your home screen

#### Desktop (Chrome/Edge/Brave)
1. Open Family Chores in browser
2. Look for install icon in address bar (⊕ or computer icon)
3. Click "Install" when prompted
4. App opens in standalone window
5. Can be launched from Start Menu/Applications folder

### For Developers

#### Generate Icons
Before deploying, generate PWA icons:

```powershell
# Windows PowerShell
.\scripts\generate_pwa_icons.ps1
```

This creates placeholder icons with the purple gradient theme and checkmark symbol. For production, consider creating custom-designed icons.

#### Custom Icons
To replace placeholder icons:
1. Design icons at 1024x1024 (or use a vector source)
2. Export to required sizes: 72, 96, 128, 144, 152, 192, 384, 512 (px)
3. Name as `icon-{size}x{size}.png` (e.g., `icon-192x192.png`)
4. Place in `static/icons/` directory
5. Rebuild Docker container

See `static/icons/README.md` for detailed icon requirements.

## Caching Strategy

The service worker uses a hybrid caching strategy:

### Cache-First (Static Assets)
Files in `/static/*` are served from cache first, with network fallback:
- CSS files
- JavaScript files
- Icons and images
- Manifest

### Network-First (HTML Pages)
Dynamic pages are fetched from network first, with cache fallback:
- All route templates
- Ensures fresh session/auth data
- Offline access to previously visited pages

### Network-Only (API Endpoints)
API routes (`/api/*`) always use network:
- No caching of dynamic data
- Returns 503 error when offline

## Configuration

### Manifest Settings (`static/manifest.json`)

```json
{
  "name": "Family Chores",           // Full app name
  "short_name": "Chores",            // Name shown on home screen
  "theme_color": "#667eea",          // Browser theme color
  "background_color": "#f5f0ff",     // Splash screen background
  "display": "standalone"            // Runs without browser UI
}
```

### Service Worker Cache Version
Update cache version in `static/sw.js` when deploying changes:

```javascript
const CACHE_VERSION = 'v1.2.5';  // Match app version
```

Old caches are automatically cleaned up on activation.

## Testing

### PWA Checklist
1. **HTTPS Required** - PWAs only work over HTTPS (or localhost)
2. **Manifest Valid** - Check DevTools → Application → Manifest
3. **Service Worker Registered** - Check DevTools → Application → Service Workers
4. **Icons Load** - Verify all icon sizes in manifest panel
5. **Installable** - Chrome shows install prompt or address bar icon
6. **Offline Works** - Disconnect network, verify cached pages load

### Browser DevTools
Chrome/Edge DevTools → Application tab:
- **Manifest:** View parsed manifest and icon validation
- **Service Workers:** See registration status, update, unregister
- **Cache Storage:** Inspect cached resources
- **Lighthouse:** Run PWA audit (installable, offline, performance)

### Testing Install Prompt
The app captures the install prompt and provides `showInstallPrompt()` function for custom install buttons:

```javascript
// Add install button to any page
<button onclick="showInstallPrompt()">Install App</button>
```

## Maintenance

### Updating the App
When deploying new versions:
1. Update `__version__` in `app.py`
2. Update `CACHE_VERSION` in `static/sw.js` to match
3. Rebuild and deploy Docker container
4. Service worker auto-updates within 1 hour (or on page refresh)

### Clear Cache
Users can clear cache by:
- Uninstalling and reinstalling the PWA
- Clearing browser data
- Developers: DevTools → Application → Clear Storage

### Debugging Service Worker
```javascript
// Console commands for debugging
navigator.serviceWorker.getRegistration()
  .then(reg => reg.unregister());  // Force unregister

// Clear all caches
caches.keys().then(names => 
  Promise.all(names.map(name => caches.delete(name)))
);
```

## Limitations

### iOS Restrictions
- No install prompt (manual "Add to Home Screen" only)
- Limited background sync
- Service worker quota limits
- No push notifications (as of iOS 16+)

### Offline Limitations
- API calls fail gracefully with 503 error
- Cannot complete/record chores offline
- Cannot modify data offline (read-only cached pages)
- Session authentication requires network

### Browser Support
- **Full Support:** Chrome, Edge, Samsung Internet, Opera
- **Partial Support:** Safari (iOS 11.3+, macOS 11.3+)
- **No Support:** Firefox (service workers supported, install prompt not)

## Future Enhancements

Potential PWA features to add:
- **Background Sync** - Queue chore completions when offline
- **Push Notifications** - Chore reminders and family notifications
- **Periodic Background Sync** - Auto-refresh data when app is closed
- **Share Target** - Share content to Family Chores
- **Shortcuts API** - Dynamic app shortcuts based on user role
- **Badging API** - Show pending chore count on app icon

## Troubleshooting

**Install button doesn't appear:**
- Verify HTTPS is enabled (or using localhost)
- Check manifest is valid in DevTools
- Ensure all required icons exist
- Try hard refresh (Ctrl+Shift+R)

**Service worker not registering:**
- Check browser console for errors
- Verify `/static/sw.js` is accessible
- Ensure no CORS issues
- Try incognito/private mode

**Offline mode not working:**
- Visit pages while online first (to cache them)
- Check cache storage in DevTools
- Verify service worker is activated
- API calls always require network

**Updates not applying:**
- Hard refresh the page
- Unregister old service worker in DevTools
- Update `CACHE_VERSION` in sw.js
- Clear browser cache

## Resources

- [MDN: Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [web.dev: PWA](https://web.dev/progressive-web-apps/)
- [PWA Builder](https://www.pwabuilder.com/) - Test and validate PWA
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - PWA audit tool
