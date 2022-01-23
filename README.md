
# Chatty
Online Chat Application

- [Chatty](#chatty)
- [Project Structure](#project-structure)


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