# DEPAAD - Device Provisioning and Authentication for Azure Active Directory

[![Python Version](https://img.shields.io/badge/python-3.7.9-blue.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/flask-1.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

DEPAAD enables multi-user support for DEP devices in MobileIron Cloud by automating device assignment through Azure AD authentication via webclip deployment.

## How It Works

1. **Webclip Deployment**: MobileIron pushes a webclip to iOS devices with device serial as URL parameter
2. **User Authentication**: User taps webclip, authenticates with Azure AD
3. **Automatic Assignment**: App assigns device to authenticated user in MobileIron Cloud

## Architecture

```
iOS Device → Webclip (w/ serial) → DEPAAD App → Azure AD Authentication → MobileIron Cloud Assignment
```

## Prerequisites

- Python 3.7.9+
- Azure AD tenant with app registration
- MobileIron Cloud instance with API access

## Quick Start

1. **Clone and setup**
   ```bash
   git clone https://github.com/vcruzcid/DEPAAD.git
   cd DEPAAD
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure and MobileIron credentials
   ```

3. **Run**
   ```bash
   python app/app.py
   ```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLIENT_SECRET` | Azure AD app client secret | ✅ |
| `API_TOKEN` | MobileIron Cloud API token (Base64) | ✅ |

### Azure AD Setup

1. Create app registration in Azure Portal
2. Set redirect URI: `https://your-domain.com/getAADToken`
3. Generate client secret
4. Update `CLIENT_ID` in `app/conf/app_config.py` (currently: `98145980-4a60-455a-9699-eacf4d339ee8`)

### MobileIron Setup

1. Generate API token in MobileIron Cloud Admin Portal
2. Base64 encode the token for `API_TOKEN` environment variable
3. Deploy webclip with URL: `https://your-app.com/?deviceSerial={DEVICE_SERIAL}`

## Security Features

- iOS device restriction via user-agent detection
- Azure AD OAuth2 authentication with state validation
- Secure session management with filesystem storage
- Environment-based secret management

## Deployment

### Heroku
```bash
heroku create your-app-name
heroku config:set CLIENT_SECRET=your_client_secret
heroku config:set API_TOKEN=your_api_token
git push heroku develop:master
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication fails | Verify `CLIENT_SECRET` environment variable |
| Device not found | Check device serial in MobileIron inventory |
| API errors | Regenerate and update `API_TOKEN` |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Version**: 0.2.0  
**Maintainer**: [vcruzcid](https://github.com/vcruzcid)