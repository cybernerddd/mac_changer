# 🕵️‍♂️ MAC Changer Utility

A Python-based **MAC Address Changer** for penetration testers, red teamers, students and privacy enthusiasts.  
Supports **randomization**, **manual MAC setting**, and **restoring original MACs** with ease.  

---

##  Features

-  Change MAC address to a **specific value**
-  Set a **completely random MAC**
-  **Restore** original MAC after spoofing
-  Validates MAC format before applying
-  Works with **any network interface**
-  Dry-run option (see changes before applying)

---

##  Installation

Clone the repository and install requirements:

```bash
git clone https://github.com/cybernerddd/mac-changer.git
cd mac-changer
pip install -r requirements.txt
```
## Usage
View Help
```bash
python mac_changer.py --help
```
- Change to a randome MAC Address
```bash
sudo python mac_changer.py --interface eth0 --random
```
- Restore Original MAC
```bash
sudo python mac_changer.py --interface eth0 --restore
```
- Dry run(Preview Changes)
```bash
python mac_changer.py --interface eth0 --random --dry-run
```

### Example Output
```less
[+] Current MAC for eth0: 08:00:27:91:2c:34
[+] Changing MAC address for eth0 to 52:11:92:ae:f3:b9
[+] MAC address successfully changed!
```
## ⚠️ Disclaimer

This tool is created for educational and ethical penetration testing purposes only.
Unauthorized use of MAC spoofing may violate laws or network policies.
Use responsibly ⚡.

👨‍💻 Author

Cybernerddd

GitHub: [cybernerddd](https://github.com/cybernerddd)

LinkedIn: [Emmanuel Agyarko Ampah](https://www.linkedin.com/in/emmanuel-a-284803370/)
