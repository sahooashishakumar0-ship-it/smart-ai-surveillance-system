# Smart AI Surveillance System for Campus Anomaly Detection

An AI-powered smart surveillance system designed to detect suspicious activities in real-time using computer vision and deep learning.

This project was developed during a hackathon to enhance campus security by automatically detecting abnormal behavior from CCTV cameras.

---

## Features

• Person detection using YOLOv8  
• Trespassing detection in restricted zones  
• Loitering detection  
• Dangerous object detection  
• Violence detection  
• Real-time alert generation  
• Evidence snapshot capture  
• Web dashboard for monitoring alerts  

---

## System Architecture

Camera / Video Stream  
↓  
YOLOv8 Detection Model  
↓  
Anomaly Detection Logic  
(Trespassing • Loitering • Violence • Dangerous Objects)  
↓  
Flask Backend API  
↓  
Alert Storage & Evidence Capture  
↓  
Web Dashboard (Frontend)

---

## Technologies Used

- Python  
- YOLOv8 (Ultralytics)  
- OpenCV  
- Flask  
- HTML  
- JavaScript  

---

## Project Structure

smart-ai-surveillance-system  
│  
├── backend  
│   └── app.py  
│  
├── frontend  
│   └── index.html  
│  
├── ai_detection.py  
├── requirements.txt  
├── README.md  
├── LICENSE  
└── .gitignore  

---

## Demo

Example detection outputs from the AI system.

Screenshots of the detection system will be added here.

• Person detection  
• Trespassing detection  
• Violence detection  

---

## Future Improvements

• Multi-camera monitoring  
• Face recognition integration  
• Cloud alert system  
• Mobile notification system  

---

## Hackathon Team

This project was developed as part of a team during a hackathon focused on building innovative solutions for campus safety.

**Team Members**

• Ashisha Kumar Sahoo – AI system development, backend, frontend, and system integration  
• Truptimayee Mohapatra – Presentation preparation and documentation support  
• Simmi Kumari – Presentation support and idea discussion  
• Neha Haldar – Documentation and research support  
• Subham Samantaray – UI concept discussion and team collaboration  

The project was presented as a collaborative team effort during the hackathon. The core technical implementation and system development were carried out by **Ashisha Kumar Sahoo**, with valuable support from the team in discussions, presentation, and documentation.
---

## License

This project is licensed under the MIT License.
