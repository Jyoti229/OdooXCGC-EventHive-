# EventHive

EventHive is a web platform for event management that allows organizers to create, publish, and manage events with flexible ticketing and promotions, while attendees can discover, register, pay, and check-in digitally.

---

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Modules](#modules)
- [Installation](#installation)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

---

## Features

### Organizer
- Create and publish events with details: title, description, date, time, location, category.
- Manage multiple ticket types: General, VIP, Student, Early Bird.
- Set ticket attributes: price, sale period, max quantity.
- Save drafts or publish events.
- Receive notifications on ticket sales.

### Attendee
- Browse and search events by category, date, location, price.
- Apply filters: rating, trending, venue type, sport type.
- Book tickets and make secure online payments.
- Receive confirmation via Email & WhatsApp.
- Check-in using QR code at the event.

### Admin
- Manage users, events, tickets, and bookings.
- Monitor platform activities.

---

## Technology Stack

*Frontend:* HTML, CSS, JavaScript  
*Backend:* Django, Django REST Framework  
*Database:* PostgreSQL / MySQL  
*Authentication:* Django Auth (JWT for API)  
*Payment Integration:* Razorpay / Stripe  
*Messaging:* Twilio / WhatsApp Business API / SMTP (Email)  
*Deployment:* Docker + AWS / Heroku  

---

## System Architecture

*Client Layer:*  
- Web: HTML, CSS, JS templates  
- Optional Mobile App (Django REST API integration)

*Application Layer (Django Backend):*  
- User & Authentication Module  
- Event Management Module  
- Ticketing & Booking Module  
- Discovery & Search Module  
- Notification & Reminder Module  
- Check-in & Validation Module  

*Data Layer:*  
- Relational DB (PostgreSQL/MySQL)  
- Tables: Users, Events, Tickets, Bookings, Payments, Notifications  

*Integration Layer:*  
- Payment Gateways  
- Messaging APIs  
- QR Code Generation  

---

## Modules Breakdown

1. *User Module:* Authentication, roles (Organizer / Attendee / Admin)  
2. *Event Module:* CRUD for events, drafts/publishing, categories  
3. *Ticket Module:* Ticket types, pricing, availability  
4. *Booking Module:* Ticket booking, payments, invoice  
5. *Notification Module:* Email/WhatsApp reminders  
6. *Check-in Module:* QR code generation and validation  

---

## Installation

1. *Clone the repository:*
   ```bash
   git clone https://github.com/yourusername/EventHive.git
   cd EventHive