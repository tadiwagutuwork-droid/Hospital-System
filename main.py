"""
main.py — Test script for the Appointments class.
Run from the project root: python main.py
"""

import os
import sys
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
sys.path.insert(0, os.path.dirname(__file__))

from models import Appointments  # adjust path if needed


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def section(title: str):
    print(f"\n{'=' * 55}")
    print(f"  {title}")
    print('=' * 55)

def expect(condition: bool, description: str):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {description}")


# ---------------------------------------------------------------------------
# Setup — ensure data dir and support files exist
# ---------------------------------------------------------------------------

def setup_data_dir():
    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base, "data")
    os.makedirs(data_dir, exist_ok=True)

    # identification.txt — one entry per line, [-2] is the appointment slot
    id_file = os.path.join(data_dir, "identification.txt")
    if not os.path.exists(id_file) or os.path.getsize(id_file) == 0:
        with open(id_file, "w") as f:
            f.write("0\n0\nA0000\n0\n")
        print(f"  Created {id_file}")

    # appointments.csv — header only
    appt_file = os.path.join(data_dir, "appointments.csv")
    if not os.path.exists(appt_file) or os.path.getsize(appt_file) == 0:
        fieldnames = [
            "Appointment ID", "Patient ID", "Doctor ID",
            "Specialisation", "Fee", "Date", "Time",
            "Status", "Notes", "Paid"
        ]
        with open(appt_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        print(f"  Created {appt_file}")
    
    appt_file = os.path.join(data_dir, "appointments.csv")
    fieldnames = ["Appointment ID", "Patient ID", "Doctor ID",
              "Specialisation", "Fee", "Date", "Time",
              "Status", "Notes", "Paid"]
    with open(appt_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    print(f"  Data directory ready: {data_dir}")


# ---------------------------------------------------------------------------
# TEST 1 — Create a new appointment
# ---------------------------------------------------------------------------

def test_create_appointment():
    section("TEST 1: Create Appointment")

    appt = Appointments(
        patient="P001",
        doctor="D001",
        specialisation="General Practitioner",
        fee=500.00,
        date="2025-08-01",
        time="09:00",
        notes="Routine checkup"
    )

    d = appt.to_dict()
    expect(appt is not None,                               "Appointment object created")
    expect(d["Patient ID"] == "P001",                     "Patient ID correct")
    expect(d["Doctor ID"] == "D001",                      "Doctor ID correct")
    expect(d["Specialisation"] == "General Practitioner", "Specialisation correct")
    expect(d["Fee"] == 500.00,                            "Fee correct")
    expect(d["Status"] == "pending",                      "Default status is 'pending'")
    expect(d["Paid"] is False,                            "Default paid is False")
    expect(d["Appointment ID"].startswith("A"),           "Appointment ID starts with 'A'")
    expect(len(d["Appointment ID"]) == 5,                 "Appointment ID is 5 chars (A + 4 digits)")
    print(f"\n  Appointment ID: {d['Appointment ID']}")
    return appt


# ---------------------------------------------------------------------------
# TEST 2 — Sequential IDs increment correctly
# ---------------------------------------------------------------------------

def test_sequential_ids():
    section("TEST 2: Sequential ID Generation")

    appt1 = Appointments("P010", "D010", "GP", 300, "2025-08-10", "10:00", "Test 1")
    appt2 = Appointments("P011", "D011", "GP", 300, "2025-08-11", "11:00", "Test 2")
    appt3 = Appointments("P012", "D012", "GP", 300, "2025-08-12", "12:00", "Test 3")

    id1 = int(appt1.to_dict()["Appointment ID"][1:])
    id2 = int(appt2.to_dict()["Appointment ID"][1:])
    id3 = int(appt3.to_dict()["Appointment ID"][1:])

    expect(id2 == id1 + 1, f"Increments correctly: {appt1.to_dict()['Appointment ID']} -> {appt2.to_dict()['Appointment ID']}")
    expect(id3 == id2 + 1, f"Increments correctly: {appt2.to_dict()['Appointment ID']} -> {appt3.to_dict()['Appointment ID']}")


# ---------------------------------------------------------------------------
# TEST 3 — Status transitions: pending -> confirmed -> completed
# ---------------------------------------------------------------------------

def test_status_transitions(appt: Appointments):
    section("TEST 3: Status Transitions (pending -> confirmed -> completed)")

    appt.confirm()
    expect(appt.to_dict()["Status"] == "confirmed", "pending -> confirmed")

    appt.complete()
    expect(appt.to_dict()["Status"] == "completed", "confirmed -> completed")

    # invalid: confirm after completed
    try:
        appt.confirm()
        expect(False, "Should raise on confirm() after completed")
    except ValueError as e:
        expect(True, f"Correctly raised ValueError: {e}")

    # invalid: cancel after completed
    try:
        appt.cancel()
        expect(False, "Should raise on cancel() after completed")
    except ValueError as e:
        expect(True, f"Correctly raised ValueError: {e}")

    return appt


# ---------------------------------------------------------------------------
# TEST 4 — Cancel from pending
# ---------------------------------------------------------------------------

def test_cancel_from_pending():
    section("TEST 4: Cancel from Pending")

    appt = Appointments("P002", "D002", "Cardiology", 800, "2025-08-05", "14:30", "Follow-up")

    expect(appt.to_dict()["Status"] == "pending", "Starts as pending")
    appt.cancel()
    expect(appt.to_dict()["Status"] == "cancelled", "Cancelled from pending")

    try:
        appt.cancel()
        expect(False, "Should raise on double cancel")
    except ValueError as e:
        expect(True, f"Correctly raised ValueError: {e}")


# ---------------------------------------------------------------------------
# TEST 5 — Cancel from confirmed
# ---------------------------------------------------------------------------

def test_cancel_from_confirmed():
    section("TEST 5: Cancel from Confirmed")

    appt = Appointments("P003", "D003", "Dermatology", 650, "2025-09-10", "11:00", "Skin rash")
    appt.confirm()
    expect(appt.to_dict()["Status"] == "confirmed", "Confirmed successfully")
    appt.cancel()
    expect(appt.to_dict()["Status"] == "cancelled",  "Cancelled from confirmed")


# ---------------------------------------------------------------------------
# TEST 6 — to_dict() has all expected keys
# ---------------------------------------------------------------------------

def test_to_dict():
    section("TEST 6: to_dict() Structure")

    appt = Appointments("P004", "D004", "Neurology", 1200, "2025-10-01", "08:00", "Headaches")
    d = appt.to_dict()

    required_keys = [
        "Appointment ID", "Patient ID", "Doctor ID",
        "Specialisation", "Fee", "Date", "Time",
        "Status", "Notes", "Paid"
    ]
    for key in required_keys:
        expect(key in d, f"Key present: '{key}'")


# ---------------------------------------------------------------------------
# TEST 7 — load_from_csv reads back saved appointments
# ---------------------------------------------------------------------------

def test_load_from_csv():
    section("TEST 7: load_from_csv()")

    records = Appointments.load_from_csv()
    expect(isinstance(records, list), "Returns a list")
    expect(len(records) > 0,          f"{len(records)} appointment(s) loaded from CSV")

    if records:
        d = records[0].to_dict()
        expect("Appointment ID" in d, "Loaded record has Appointment ID")
        expect("Status" in d,         "Loaded record has Status")
        print(f"  First loaded ID: {d['Appointment ID']} | Status: {d['Status']}")


# ---------------------------------------------------------------------------
# TEST 8 — billing_records() writes to billing.csv on complete()
# ---------------------------------------------------------------------------

def test_billing_written():
    section("TEST 8: billing_records() writes to billing.csv")

    base = os.path.dirname(os.path.abspath(__file__))
    billing_path = os.path.join(base, "data", "billing.csv")

    appt = Appointments("P005", "D005", "Oncology", 2000, "2025-11-01", "09:30", "Check-up")
    appt.confirm()
    appt.complete()

    expect(os.path.exists(billing_path), "billing.csv exists after complete()")

    with open(billing_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    match = [r for r in rows if r['Appointment ID'] == appt.to_dict()['Appointment ID']]
    expect(len(match) == 1, f"Billing record written for {appt.to_dict()['Appointment ID']}")
    print(f"  Billing row: {match[0]}")

    return appt


# ---------------------------------------------------------------------------
# TEST 9 — payment() marks Paid as True in billing.csv
# ---------------------------------------------------------------------------

def test_payment(appt: Appointments):
    section("TEST 9: payment()")

    appt.payment()

    base = os.path.dirname(os.path.abspath(__file__))
    billing_path = os.path.join(base, "data", "billing.csv")

    with open(billing_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    match = [r for r in rows if r['Appointment ID'] == appt.to_dict()['Appointment ID']]
    expect(len(match) == 1,            "Record still exists after payment")
    expect(match[0]['Paid'] == 'True', "Paid updated to 'True' in billing.csv")
    print(f"  Paid status in CSV: {match[0]['Paid']}")
    appt.clear_csv_file()

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n*** Appointments Class — Test Suite ***")

    setup_data_dir()

    appt1 = test_create_appointment()
    test_sequential_ids()
    test_status_transitions(appt1)
    test_cancel_from_pending()
    test_cancel_from_confirmed()
    test_to_dict()
    test_load_from_csv()
    billing_appt = test_billing_written()
    test_payment(billing_appt)

    print(f"\n{'=' * 55}")
    print("  All tests complete.")
    print('=' * 55 + '\n')
    appt = Appointments(
        patient="P001",
        doctor="D001",
        specialisation="General Practitioner",
        fee=500.00,
        date="2025-08-01",
        time="09:00",
        notes="Routine checkup"
    )

    appt.clear_csv_file()