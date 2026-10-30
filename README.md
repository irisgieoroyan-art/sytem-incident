# Incident Report Recording System

Kini nga sistema maoy talaan sa mga panghitabo (incident) sa eskuylahan. Matag
report adunay petsa, oras, lugar, klase sa panghitabo, mga tawo nga nalambigit,
salaysay, aksyon nga gihimo, ug kahimtang. Mahimo kang mangita, motan-aw sa
detalye, mo-update sa aksyon, ug mopapas sa rekord.

## Unsa ang kinahanglan

- **Python 3.8 o mas bag-o**
- **XAMPP** (MySQL/MariaDB)
- **mysql-connector-python**

## 1) I-install ang MySQL connector

```powershell
pip install mysql-connector-python
```

## 2) Sugdi ang XAMPP

1. Ablihi ang **XAMPP Control Panel**.
2. Pindota ang **Start** tapad sa **MySQL**.
3. Siguroha nga **green** ang kolor sa MySQL.
4. Dili kinahanglan ang Apache kung CLI lang ang gamiton, pero ablihi kini kung
   mogamit ka sa phpMyAdmin.

## 3) I-import ang database

1. Ablihi ang browser ug adto sa `http://localhost/phpmyadmin`.
2. Pindota ang **Import** tab.
3. Pilia ang `schema_ir.sql` (naa kini sa sama nga folder).
4. Pindota ang **Go** o **Import**.
5. Siguroha nga makita ang `incident_db` sa lista sa wala nga bahin.

## 4) Koneksyon sa database

Gamit ang mosunod nga default:

| Variable | Default |
| --- | --- |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `3306` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | *(walay password)* |
| `DB_NAME` | `incident_db` |

Kung lahi ang imong setup, i-set kini sa PowerShell sa wala pa padagana:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
$env:DB_NAME = "incident_db"
```

> Sa CMD, gamita ang `set DB_HOST=localhost` ug uban pa.

## 5) Padagana ang sistema

```powershell
cd "C:\Users\suete\Documents\system for sale\irish=incident_report_system"
python main_ir.py
```

> Kung ibalhin ang folder sa lain nga computer, ilisi ang `cd` path sa
> aktwal nga lokasyon sa folder.


Dapat makita nimo ang mensahe nga **"Koneksyon sa Incident Report database ay maayos na."**
Kung ang sistema moingon nga kinahanglan pa i-import ang schema, tan-awa ang
Troubleshooting sa ubos.

## Mga file

| File | Tumong |
| --- | --- |
| `schema_ir.sql` | Naghimo sa `incident_db` ug sa table nga `incident_reports` |
| `ir_db.py` | Tanan nga SQL: insert, select, update, delete |
| `incident_workflow.py` | Flow sa menu: pagsumite, pagpakita, pagpangita, update, papas |
| `main_ir.py` | Ang CLI menu |
| `test_compile.py` | Pagsusi kung walay syntax error |

## Menu

| Numero | Aksyon |
| --- | --- |
| `1` | Pagsumite og bag-ong incident report |
| `2` | Tanan nga incident report |
| `3` | Detalye sa usa ka report (pangitaa pinaagi sa report number) |
| `4` | Dugang aksyon / update sa kahimtang |
| `5` | Papasa sa usa ka rekord |
| `6` | Papasa sa **TANAN** nga rekord |
| `0` | Gula |

> **Pasidaan:** Ang numero `6` mopapas sa tanan nga report. Mangutana kini og
> kumpirmasyon; i-type ang `oo` para modayon. Kung dili `oo`, kanselado.

## Giunsa pagtipig ang datos

Ang tanan nga report naa sa MySQL (`incident_db.incident_reports`). Kung
mopadayon ka sa laing computer, i-export una ang database ug i-import didto.

## Troubleshooting

| Sayop / Mensahe | Solusyon |
| --- | --- |
| `Can't connect to MySQL server on 'localhost:3306'` | Wala nagdagan ang MySQL. Ablihi ang XAMPP ug pindota ang **Start** sa MySQL. |
| `Unknown database 'incident_db'` | Wala pa na-import ang schema. Balika ang Lakang 3. |
| `Table 'incident_db.incident_reports' doesn't exist` | Sayop o kulang ang na-import nga schema. I-import pag-usab ang `schema_ir.sql`. |
| `Access denied for user 'root'@'localhost'` | Naay password ang root. I-set ang `DB_PASSWORD`. |
| `ModuleNotFoundError: No module named 'mysql'` | `pip install mysql-connector-python` |
| `Port 3306 already in use` | Naay lain nga MySQL. Ilisi ang port sa XAMPP o patya ang lain nga serbisyo. |

## Backup sa datos

1. Adto sa phpMyAdmin.
2. Pilia ang `incident_db` sa wala.
3. Pindota ang **Export** → **Go**.
4. Tipigi ang `.sql` file.

## Sulayi ang code

```powershell
python test_compile.py
```

Dapat `OK` ang mogawas.
