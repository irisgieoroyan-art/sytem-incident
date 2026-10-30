import re
from datetime import datetime

import mysql.connector

try:
    import ir_db
except Exception:
    import ir_db


def draw_field_box(msg):
    while True:
        v = input(msg).strip()
        if v == "":
            print("  * Kinakailangan ito.")
            continue
        return v


def ask_report_date():
    print("  Petsa ng pangyayari (YYYY-MM-DD)")
    while True:
        v = input("    >> ").strip()
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            print("  * Mali ang petsa. Halimbawa: 2026-10-28")


def ask_report_time():
    print("  Oras ng pangyayari (HH:MM, 24-oras)")
    while True:
        v = input("    >> ").strip()
        if re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", v):
            return v
        print("  * Mali ang oras. Halimbawa: 14:30")


def show_report_detail(r):
    print("\n" + "-" * 44)
    print(f"  INCIDENT REPORT # : {r['ir_no']}")
    print("-" * 44)
    print(f"  Nireport Ni        : {r['reported_by']}")
    print(f"  Petsa/Oras         : {r['incident_date']} {r['incident_time']}")
    print(f"  Lugar              : {r['location']}")
    print(f"  Uri                : {r['incident_type']}")
    print(f"  Mga Sangkot        : {r['persons_involved']}")
    print("\n  SALAYSAY NG PANGYAYARI:")
    print(f"  {r['narrative']}")
    print("\n  AKSYON NA GINAWA:")
    print(f"  {r['action_taken'] or '--- WALA PA ---'}")
    print(f"  Iniulat Kay        : {r['reported_to'] or '---'}")
    print(f"  Kalagayan          : {r['status']}")
    print("-" * 44)


def file_new_report():
    print("\n--- PAGSUSUMITE NG BAGONG INCIDENT REPORT ---")
    irno = ir_db.next_ir()
    print(f"  Incident Report #: {irno}")
    repby = draw_field_box("  Nireport ni (Buong Pangalan): ")
    d = ask_report_date()
    tm = ask_report_time()
    loc = draw_field_box("  Lugar kung saan nangyari: ")
    print("  Uri ng Insidente: [1] Aksidente [2] Away/Unrest [3] Pagkasira [4] Iba pa")
    c = input("    Pumili: ").strip()
    if c == "1":
        itype = "Aksidente"
    elif c == "2":
        itype = "Away/Unrest"
    elif c == "3":
        itype = "Pagkasira"
    elif c == "4":
        itype = draw_field_box("    Tukuyin ang uri: ")
    else:
        itype = draw_field_box("    Uri ng insidente: ")
    pinv = draw_field_box("  Mga sangkot (Buong pangalan o detalye): ")
    print("  Salaysay ng pangyayari (detalyado): ")
    narr = input("    >> ").strip()
    while narr == "":
        print("  * Kailangan ng salaysay.")
        narr = input("    >> ").strip()
    rec = {
        "ir_no": irno,
        "reported_by": repby,
        "incident_date": d,
        "incident_time": tm,
        "location": loc,
        "incident_type": itype,
        "persons_involved": pinv,
        "narrative": narr,
        "action_taken": None,
        "reported_to": None,
        "status": "Kasalukuyang Binabantayan",
    }
    try:
        ir_db.save_report(rec)
        print("\n  [NAIREKORD] Matagumpay na naisumite ang incident report.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def show_all_reports():
    try:
        case_rows = ir_db.all_reports()
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not case_rows:
        print("\n  Wala pang naitalang incident report.")
        return
    print("\n--- LISTAHAN NG MGA INCIDENT REPORT ---")
    for r in case_rows:
        print(f"  [{r['ir_no']}] {r['incident_date']} {r['incident_time']} | {r['incident_type']} @ {r['location']} | {r['status']}")


def find_reports():
    irno = draw_field_box("  Ilagay ang Incident Report #: ").upper()
    try:
        r = ir_db.get_report(irno)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not r:
        print("  [WALA] Hindi matagpuan ang report na ito.")
        return
    show_report_detail(r)


def update_followup():
    irno = draw_field_box("  Incident Report # na aaksyunan: ").upper()
    try:
        r = ir_db.get_report(irno)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not r:
        print("  [WALA] Hindi matagpuan.")
        return
    show_report_detail(r)
    print("\n  Aksyon na ginawa (detalyado): ")
    act = input("    >> ").strip()
    while act == "":
        print("  * Kailangan ng detalye ng aksyon.")
        act = input("    >> ").strip()
    rto = draw_field_box("  Iniulat kay (Pangalan/Posisyon): ")
    print("  Kalagayan: [1] Binabantayan [2] Kinasuhan/Pinagtulungan [3] Sarado/Naayos na")
    c = input("    Pumili: ").strip()
    if c == "1":
        st = "Kasalukuyang Binabantayan"
    elif c == "2":
        st = "Kinasuhan/Pinagtulungan"
    elif c == "3":
        st = "Sarado/Naayos na"
    else:
        st = "Kasalukuyang Binabantayan"
    try:
        ir_db.update_status(irno, act, rto, st)
        print("\n  [NA-UPDATE] Na-update na ang estado ng incident report.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def delete_one_report():
    irno = draw_field_box("  Incident Report # na tatanggalin: ").upper()
    try:
        r = ir_db.get_report(irno)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not r:
        print("  [WALA] Hindi matagpuan.")
        return
    show_report_detail(r)
    konf = input("  Sigurado ka bang tanggalin ito? (oo/hindi): ").strip().lower()
    if konf not in ("oo", "o", "yes", "y"):
        print("  Kinansela.")
        return
    try:
        ir_db.delete_report(irno)
        print("  [TINANGGAL] Natanggal na ang rekord.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def purge_old_reports():
    konf = input("  Tanggalin ang LAHAT ng incident reports? (oo/hindi): ").strip().lower()
    if konf not in ("oo", "o", "yes", "y"):
        print("  Kinansela.")
        return
    try:
        c = ir_db.delete_all()
        print(f"  [TINANGGAL] Natanggal ang {c} na rekord.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
