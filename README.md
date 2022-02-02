
# Chatty <!-- omit in toc -->
Online Chat Application

- [Project Structure](#project-structure)
- [TODO](#todo)
  - [Messaging](#messaging)
  - [WebRTC](#webrtc)


# Project Structure
```
.
├── app                         # Flask source files
│   ├── api                         # API specific views
│   ├── auth                        # Authentication specific views and forms
│   ├── main                        # Top level views/forms/errors
│   ├── sockets                     # Websocket specific views
│   ├── static                      # Front-end outputs and other static files
│   └── templates                   # Flask templates
│                                      
├── assets                      # Front End and React source
│   └── components                  # Compontents source
│  
└── migrations                  # Database migration files 
    └── versions                    # Migration scripts
```

# TODO
## Messaging
- [ ] Markdown/Rich text support for messages
- [x] Save messages to DB
- [x] Display past messages in channel
- [ ] Direct messages between users
- [ ] Channel Visibility
- [ ] User Permissions

## WebRTC
- [ ] Add Audio Channels
- [ ] Add Video Channels