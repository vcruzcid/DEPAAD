# Changelog

All notable changes to DEPAAD will be documented in this file.

## [0.2.0] - 2024-01-15

### Added
- Heroku deployment configuration and Procfile
- Production logging with rotation
- Comprehensive project documentation
- Environment configuration template (.env.example)

### Changed
- Enhanced error handling and user experience
- Updated templates and UI components
- Improved session management for production

### Fixed
- Session storage issues in production environment
- Device assignment workflow improvements
- Logging configuration for Heroku deployment

## [0.1.0] - 2023-12-01

### Added
- Initial release - Multi-user DEP device support for MobileIron Cloud
- Azure AD OAuth2 authentication with MSAL
- MobileIron Cloud API integration for device assignment
- iOS device detection and webclip parameter handling
- Flask web application with session management
- Automated device-to-user assignment workflow

### Features
- **Webclip Integration**: Device serial passed automatically via MobileIron webclip
- **Azure Authentication**: Secure OAuth2 flow with Microsoft Identity Platform  
- **Device Assignment**: Automatic assignment of DEP devices to authenticated users
- **iOS Detection**: Platform validation to restrict access to iOS devices only
- **Session Security**: Filesystem-based session storage with state validation

### Technical Details
- Python 3.7.9 with Flask 1.1.2
- Microsoft Authentication Library (MSAL) for OAuth2
- MobileIron Cloud REST API integration
- CoreUI-based responsive templates
- Environment-based configuration management