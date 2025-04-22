# Module II Offline Activity: ChEMBL & UniProt API

This repository contains a Python script that:

1. **Fetches** all Phase‑IV (approved) drugs from ChEMBL  
2. **Filters** for those first approved in 2019 or later  
3. **Retrieves** UniProt accessions for each drug’s single‑protein targets  
4. **Downloads** UniProt keywords for each accession  
5. **Outputs** the combined data into a TSV file

---

## Repository Structure
. ├── offline_activity_module_II.py # main script ├── requirements.txt # Python dependencies ├── LICENSE # (optional) license file └── README.md # this file

---

## Prerequisites

- Python 3.12+  
- Internet connection (to reach ChEMBL & UniProt REST APIs)

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/module-ii-offline-activity.git
   cd module-ii-offline-activity
