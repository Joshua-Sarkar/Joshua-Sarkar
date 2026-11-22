<p align="center">
  <img src="https://raw.githubusercontent.com/Joshua-Sarkar/Joshua-Sarkar/media/hero.gif" width="100%" alt="Joshua Sarkar, age 20, B.Tech CSE AI and ML student at Graphic Era University, in a large animated royal-serif title over a cosmic glass background" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Joshua-Sarkar/Joshua-Sarkar/media/tagline.gif" width="96%" alt="Animated project interests" />
</p>

<p align="center">
  <a href="https://github.com/Joshua-Sarkar?tab=repositories"><img src="https://img.shields.io/badge/PROJECTS-BROWSE%20REPOSITORIES-7C3AED?style=for-the-badge&logo=github&logoColor=white" alt="Browse repositories"/></a>
  <img src="https://komarev.com/ghpvc/?username=Joshua-Sarkar&style=for-the-badge&color=0891B2" alt="Profile views"/>
</p>

## **ABOUT ME**

I'm **Joshua Sarkar**, 20, a third-year B.Tech CSE student specialising in AI and Machine Learning at **Graphic Era University, Dehradun**. One of my main projects is **AMS-V1 — Workforce Ledger**: a live attendance and payroll system I built for VentureQuest, my father's company. Around 50 employees use it, so it deals with real shifts, leave balances, salary records and the occasional production problem that refuses to wait until Monday.

I work across full-stack development, computer vision, machine learning and systems programming. Outside coursework, I keep returning to difficult subjects such as neuromorphic computing, computational oncology, prion research and consciousness. Nagel's *What Is It Like to Be a Bat?* is one of the questions I keep turning over.

I also write horror and call my approach **Sarkarian Horror**: Kafka-style bureaucracy mixed with Lovecraftian cosmic indifference. The frightening thing is often the institution, the process or the system itself—not a villain. Away from the screen, I'm usually playing guitar, listening to the Beatles (particularly George Harrison), or writing in my dream journal.

---

## **PROJECTS & EXPERIMENTS** 🧩

<p align="center">
  <img src="https://raw.githubusercontent.com/Joshua-Sarkar/Joshua-Sarkar/media/projects-glass.gif" width="100%" alt="Animated glass project cards" />
</p>

### 🛡️ [Sentinel-Cam Enterprise](https://github.com/Joshua-Sarkar/Sentinel-Cam-Enterprise)
An AI-assisted CCTV monitoring dashboard built with Django, OpenCV and Ultralytics YOLO. It can process video feeds, run object detection, segmentation and pose tasks, filter detections by a human-readable target name, log security events and send email alerts through a background thread. The repository also contains a separate PyTorch CNN training experiment and UCSD anomaly-detection frames. The main monitoring path uses YOLO; the older CNN experiment is not the live inference engine.

### 📋 [AMS-V1 — Workforce Ledger](https://github.com/Joshua-Sarkar/Attendance-Management-System) · <sub>Private</sub>
My live workforce platform for VentureQuest, used by roughly 50 employees. It combines employee and department records, manager hierarchy, role-based access, clock-in/out, late-arrival rules, leave requests and approvals, a double-entry leave ledger, audit trails, bulk attendance overrides, employee dossiers and payroll workflows. It also includes Zimyo spreadsheet imports, encrypted sensitive profile fields, payslip/record management, payroll disputes and exports. Built with Laravel 12, PHP, MySQL, Blade, Tailwind and Pest.

### 🌱 [PlantDoc — Smart Agriculture](https://github.com/Joshua-Sarkar/Smart-Agriculture-Plantdoc)
A plant-disease analysis project built around the 38-class PlantVillage label set. The backend uses TensorFlow Lite for image inference, a separate Keras model for Grad-CAM heatmaps, and simulated ESP32-style humidity, temperature and soil-moisture readings. A Bayesian-style environmental weighting layer adds context to the visual prediction. The React frontend exposes the result, top predictions, sensor readings and model explanations.

### 💊 [PharmaLock](https://github.com/Joshua-Sarkar/PharmaLock-Pharmacy-Drug-Inventory-Engine)
A pharmacy inventory simulator that doubles as an interactive operating-systems and database-systems lab. It ties together a disk manager, an LRU buffer pool, transaction processing, write-ahead logging, strict two-phase locks, wait-for-graph deadlock detection, crash simulation and recovery. The Flask dashboard exposes stock operations and live lock/cache/log state so you can watch concurrency problems happen rather than just read about them.

### 💬 [wacrm-fusion — WhatsApp CRM](https://github.com/Joshua-Sarkar/wacrm-fusion)
A self-hostable CRM built with Next.js, React, TypeScript, PostgreSQL, Prisma and the WhatsApp Business Cloud API. Its modules include a shared team inbox, contacts and custom fields, tags, deals and sales pipelines, broadcasts, message templates, no-code automations, visual conversation flows, team roles, a scoped API-key foundation and optional LiveKit voice-call integration. The public API is still being rolled out endpoint by endpoint; check its API documentation for the endpoints currently available.

### 🧭 [Scout — Lead Intelligence](https://github.com/Joshua-Sarkar/scout-lead-intelligence) · <sub>Private</sub>
A client-aware lead research pipeline. It discovers businesses from OpenStreetMap, resolves city boundaries and filters results against the returned polygon, classifies facilities, flags possible duplicates for human review, inspects public website content with URL and redirect safeguards, and uses an LLM to prepare evidence-based lead assessments. It can sync structured records to Google Sheets and create Gmail drafts for qualified leads; it does **not** send emails automatically.

### 🩺 [EHR De-identification & Blockchain Provenance](https://github.com/Joshua-Sarkar/EHR-Deidentification-Blockchain)
A Flask prototype that uses spaCy named-entity recognition to replace selected medical-text entities, computes SHA-256 fingerprints before and after transformation, and records the hashes and action metadata in a Ganache-hosted smart contract. It includes a basic browser login/de-identification flow and a separate integrity-verification script. This is an academic prototype, not a production medical-data system; its current authentication and secret configuration need hardening before any real data is used.

### 🫀 [Blood Circulation & Blockages Simulation](https://github.com/Joshua-Sarkar/Blood-Circulation-and-Blockages-Simulation)
A small C simulation of a vascular network represented as a graph. Each node holds a queue of simulated blood cells; each tick moves cells into neighbouring vessels subject to capacity, while a blockage timer can temporarily stop movement. A lightweight libmicrohttpd server exposes state, tick and blockage endpoints to a JavaScript visualiser. It is a data-structure simulation, not a medical or physiological model.

### ✈️ [AeroDAA — Airline Pricing & Ticket System](https://github.com/Joshua-Sarkar/Airline-Price-Based-Ticket-System)
A C++ airline reservation and dynamic-pricing coursework project with a web dashboard. It combines linear search for route/date matches, greedy fare adjustments based on seat occupancy and departure date, Quick Sort for price ordering, and memoisation for repeated fare calculations. Flight and booking data are stored in CSV files, while the UI demonstrates the algorithms as they run.

### **AMS client and release variants**
Alongside the main AMS repository, I maintain separate private snapshots/deployments:
- [Golden Frozen Master](https://github.com/Joshua-Sarkar/Attendance-Management-System-Golden-Frozen-Master) — preserved master snapshot.
- [Future Corridor](https://github.com/Joshua-Sarkar/Attendance-Management-System-Client-02-Future-Corridor-) — client-specific edition with its own liquid-glass design constitution.
- [Dwheelz](https://github.com/Joshua-Sarkar/Attendance-Management-System-Client-03-Dwheelz) — a separate client deployment variant.

[Browse every repository →](https://github.com/Joshua-Sarkar?tab=repositories)

<p align="center">
  <img src="https://raw.githubusercontent.com/Joshua-Sarkar/Joshua-Sarkar/media/divider.gif" width="100%" alt="Animated topographic glass divider" />
</p>

---

## **A LITTLE LOVECRAFT. A LITTLE AM.** 🌌

I like Lovecraft most when the universe isn't malicious; it simply doesn't care. *The Colour Out of Space* and *At the Mountains of Madness* make the human scale feel fragile in very different ways. The Great Race of Yith and *The Shadow Out of Time* take the question further: if a mind can be displaced across bodies and centuries, what exactly survives the journey?

AM, from Harlan Ellison's *I Have No Mouth & I Must Scream*, is the opposite nightmare: a mind with immense power over others and no escape from its own consciousness. Its hatred becomes a prison it cannot leave. That tension is one reason I keep coming back to the hard problem of consciousness.

<p align="center">
  <img src="https://raw.githubusercontent.com/Joshua-Sarkar/Joshua-Sarkar/media/lovecraft-am.gif" width="100%" alt="Animated cosmic horror and AM terminal banner" />
</p>

> **“That is not dead which can eternal lie.”**  
> — H. P. Lovecraft, *The Call of Cthulhu*

> **“The office had been empty for thirty years. Your appeal was still being processed, and each new form arrived in your handwriting.”**  
> — A fragment of *Sarkarian Horror*

---

## **WHAT THE COMMITS HAVE BEEN UP TO** 📈

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=Joshua-Sarkar&bg_color=11101B&color=E9D5FF&line=22D3EE&point=FBBF24&area=true&hide_border=true&custom_title=Contribution%20Activity" width="100%" alt="GitHub contribution activity graph" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Joshua-Sarkar/Joshua-Sarkar/output/github-contribution-grid-snake.svg" width="100%" alt="Animated GitHub contribution snake" />
</p>

<p align="center"><sub>Thanks for stopping by. Have a look around, open an issue, or say hello.</sub></p>
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:24104F,28:6D28D9,58:0891B2,82:EC4899,100:F59E0B&height=110&section=footer" width="100%" />
</p>
