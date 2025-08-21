# xblock-image v1.0.0 - OpenEDX Compatible

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/openedx/xblock-image)

> Course component (Open edX XBlock) that provides an easy way to embed full-width images - **Compatible with modern OpenEDX releases**

## Features

- 📸 **Full-width responsive image display**
- 🏷️ **Customizable display name and alt text**
- ♿ **Accessibility-focused with proper ARIA attributes**
- 📊 **Analytics tracking for image loads and errors**
- 🎨 **Clean, modern styling with hover effects**
- 📱 **Mobile-responsive design**
- ⚡ **Fast loading with error handling**

## What's New in v1.0.0

- ✅ **Modern OpenEDX Compatible**
- ✅ **Python 3.11+ Support**
- ✅ **Updated XBlock Dependencies**
- ✅ **Comprehensive Error Handling**
- ✅ **Modern Development Tools**
- ✅ **Accessibility Features**
- ✅ **Enhanced Studio Integration**
- ✅ **Analytics Integration**

## Install / Update the XBlock

### For Tutor EDX (Recommended)

Add it to config.yml using this parameter:

```bash
nano "$(tutor config printroot)/config.yml"
```

```yml
OPENEDX_EXTRA_PIP_REQUIREMENTS:
  - "git+https://github.com/your-repo/xblock-image.git@v1.0.0#egg=xblock-image"
```

Save your config file and rebuild:

```bash
tutor config save
tutor images build openedx
tutor local start -d
```

### For Native OpenEDX Installation

Add it to the `EDXAPP_EXTRA_REQUIREMENTS` variable:

```yml
EDXAPP_EXTRA_REQUIREMENTS:
  - name: "git+https://github.com/your-repo/xblock-image.git@v1.0.0#egg=xblock-image"
```

Then run your deployment playbooks.

### Restart your Open edX processes

```shell
sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp:
```

Not needed in tutor EDX

## Use the XBlock

### Activate the XBlock in your course

Go to `Settings -> Advanced Settings` and set `advanced_modules` to `["image"]`.

### Use the XBlock in a unit

Select `Advanced -> Image Display` in your unit.

## Configuration Options

### Display Name

The title that appears above the image and in navigation.

### Image URL

The URL of the image to display. Supports:

- JPG/JPEG
- PNG
- GIF
- SVG
- WebP

### Alternative Text (Optional)

Descriptive text for screen readers and when images fail to load. Important for accessibility.

## Development Environment

### Prerequisites

- Python 3.11+
- pip and virtualenv

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-repo/xblock-image.git
   cd xblock-image
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   make dev-install
   ```

### Development Commands

- **Install dependencies:** `make requirements`
- **Run tests:** `make test`
- **Run tests with coverage:** `make coverage`
- **Run linting:** `make quality`
- **Clean build artifacts:** `make clean`
- **Build package:** `make build`

## Analytics Events

The XBlock publishes the following events for analytics:

- `edx.image.displayed` - When an image loads successfully
- `edx.image.load_error` - When an image fails to load

## Accessibility Features

- Proper alt text support
- Title attributes for additional context
- Keyboard navigation support
- Screen reader compatibility
- High contrast support

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

Run the test suite:

```bash
make test
```

Run with coverage:

```bash
make coverage
```

Run quality checks:

```bash
make quality
```

## License

GNU Affero General Public License 3.0 (AGPL 3.0)

## Support

For support, please open an issue in the GitHub repository or contact the OpenEDX community.
