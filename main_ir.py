import ir_db
import incident_workflow


def ir_menu():
    print("\n" + "="*46)
    print("   INCIDENT REPORT - PAG-REKORD NG PANGYAYARI")
    print("="*46)
    print("  [1] Mag-submit ng Bagong Incident Report")
    print("  [2] Buong Listahan ng mga Incident Report")
    print("  [3] Tingnan ang Detalye ng isang Report")
    print("  [4] Idagdag ang Aksyon / I-update ang Kalagayan")
    print("  [5] Tanggalin ang isang Rekord")
    print("  [6] Tanggalin ang LAHAT ng Rekord")
    print("  [0] Lumabas")
    print("="*46)


def ir_cli():
    ok, msg = ir_db.test_connection()
    print(f"\n  {msg}")
    if not ok:
        print("  Paki-import muna ang 'schema_ir.sql' sa XAMPP/MySQL.")
        return
    while True:
        ir_menu()
        ch = input("\n  Piliin ang nais mong gawin : ").strip()
        if ch == "1":
            incident_workflow.file_new_report()
        elif ch == "2":
            incident_workflow.show_all_reports()
        elif ch == "3":
            incident_workflow.find_reports()
        elif ch == "4":
            incident_workflow.update_followup()
        elif ch == "5":
            incident_workflow.delete_one_report()
        elif ch == "6":
            incident_workflow.purge_old_reports()
        elif ch == "0":
            print("\n  Salamat. Ingat lagi!")
            break
        else:
            print("\n  * Hindi wasto ang pagpili.")


if __name__ == "__main__":
    ir_cli()
