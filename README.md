# Poketar 🎯⚡

**Pokémon Emoji Avatar Generator & Scanner**

A Flask web application that generates personalized Pokémon emoji combinations based on your unique characteristics. Create your own Pokémon personality through multiple interactive input methods!

## ✨ Features

- **📸 Face Scanning**: Use your camera to capture facial features for personality analysis
- **🎤 Voice Commands**: Speak your preferences using voice-to-text technology
- **✍️ Text Prompts**: Describe yourself with text for custom Pokémon generation
- **🎨 Emoji Generation**: Get simple, fun emoji combinations representing your Pokémon type
- **🔄 Consistent Results**: Deterministic analysis ensures the same input always gives the same result
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🌙 Cyber Theme**: Clean, modern dark interface with futuristic styling

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Modern web browser with camera/microphone support

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RafalW3bCraft/poketar.git
   cd poketar
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using uv:
   ```bash
   uv sync
   ```

3. **Set environment variables**
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎮 How to Use

### 📸 Face Scanner
1. Click on "Scanner" from the main menu
2. Allow camera permissions when prompted
3. Position your face in the camera frame
4. Click "Scan Face" to capture and analyze
5. Receive your personalized Pokémon emoji combination!

### 🎤 Voice Input
1. Click the microphone button
2. Allow microphone permissions
3. Speak your Pokémon preferences or personality traits
4. The system will process your voice and generate emojis

### ✍️ Text Input
1. Use the text input field on the main page
2. Describe your personality, preferences, or desired Pokémon type
3. Submit to get your custom emoji combination

## 🧬 How It Works

### Pokémon Type Detection
The system analyzes your input using deterministic algorithms to determine:

- **18 Pokémon Types**: Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy
- **Personality Traits**: Friendly, energetic, brave, calm, playful, wise, mysterious
- **Energy Levels**: High, medium, low energy states

### Emoji Generation
Your unique combination includes:
- **Type Emoji**: Represents your primary Pokémon type (⚡🔥💧🌿)
- **Personality Emoji**: Shows your character traits (😊🦁🧘✨)
- **Energy Emoji**: Indicates your energy level (🔥⭐🌙)

Example result: `⚡😊✨` (Electric type, friendly personality, high energy)

## 🛠️ Technical Stack

### Backend
- **Flask**: Python web framework
- **Deterministic Analysis**: Consistent personality detection
- **Unicode Emojis**: Simple, universal emoji combinations
- **RESTful APIs**: Clean endpoint structure

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Jinja2**: Server-side templating
- **WebRTC**: Camera integration
- **Web Speech API**: Voice recognition
- **Custom CSS**: Cyber-themed styling

### Deployment
- **Gunicorn**: Production WSGI server
- **Environment Variables**: Secure configuration
- **Cross-platform**: Works on any system with Python

## 📁 Project Structure

```
poketar/
├── app.py              # Main Flask application
├── main.py             # Application entry point
├── templates/          # HTML templates
│   ├── index.html      # Main page
│   └── scanner.html    # Camera scanner page
├── static/             # Static assets
│   └── images/         # Generated avatars
├── pyproject.toml      # Project configuration
├── LICENSE             # MIT License
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables
- `SESSION_SECRET`: Flask session secret key
- `DATABASE_URL`: PostgreSQL database connection (optional)

### Development Mode
```python
# Enable debug mode for development
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation for API changes
- Use meaningful commit messages

## 🐛 Troubleshooting

### Common Issues

**Camera not working?**
- Ensure browser permissions are granted
- Check if camera is being used by another application
- Try refreshing the page

**Voice input not responding?**
- Verify microphone permissions
- Check browser compatibility (Chrome/Firefox recommended)
- Ensure stable internet connection

**Emoji combinations not generating?**
- Clear browser cache and cookies
- Check JavaScript console for errors
- Verify all dependencies are installed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 RafalW3bCraft

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👨‍💻 Author

**RafalW3bCraft**
- Creative developer passionate about interactive web applications
- Combining modern web technologies with gaming elements
- Focused on user experience and innovative digital solutions

## 🔗 Links

- **Project Repository**: [GitHub](https://github.com/RafalW3bCraft/poketar)
- **Live Demo**: [Replit](https://replit.com)
- **Documentation**: Check `replit.md` for detailed technical documentation

## 🙏 Acknowledgments

- Pokémon franchise for inspiration
- Flask community for excellent documentation
- Bootstrap team for responsive framework
- Web APIs for modern browser capabilities

---

**Made with ❤️ by RafalW3bCraft**

*Generate your Pokémon personality today! 🎯⚡*