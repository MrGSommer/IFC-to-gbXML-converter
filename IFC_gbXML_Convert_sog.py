import tkinter as tk
from tkinter import filedialog, messagebox
import ifcopenshell
from xml.dom import minidom

# Funktion zum Erstellen des gbXML
def generate_gbxml(ifc_path, output_path):
    try:
        # IFC-Datei öffnen
        ifc_file = ifcopenshell.open(ifc_path)

        # XML-Struktur erstellen
        root = minidom.Document()
        gbxml = root.createElement('gbXML')
        root.appendChild(gbxml)

        # gbXML-Attribute hinzufügen
        gbxml.setAttribute('xmlns', 'http://www.gbxml.org/schema')
        gbxml.setAttribute('temperatureUnit', 'C')
        gbxml.setAttribute('lengthUnit', 'Meters')
        gbxml.setAttribute('areaUnit', 'SquareMeters')
        gbxml.setAttribute('volumeUnit', 'CubicMeters')
        gbxml.setAttribute('useSIUnitsForResults', 'true')
        gbxml.setAttribute('version', '0.37')

        # Campus hinzufügen
        campus_elements = ifc_file.by_type('IfcSite')
        for element in campus_elements:
            campus = root.createElement('Campus')
            campus.setAttribute('id', f"campus_{element.GlobalId}")
            gbxml.appendChild(campus)

        # XML speichern
        with open(output_path, "w") as file:
            file.write(root.toprettyxml(indent="  "))
        messagebox.showinfo("Erfolg", f"gbXML-Datei wurde erstellt: {output_path}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler bei der Erstellung: {str(e)}")

# Funktionen für UI-Interaktion
def select_ifc_file():
    file_path = filedialog.askopenfilename(filetypes=[("IFC Dateien", "*.ifc")])
    if file_path:
        ifc_entry.delete(0, tk.END)
        ifc_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML Dateien", "*.xml")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def start_conversion():
    ifc_path = ifc_entry.get()
    output_path = output_entry.get()
    if not ifc_path or not output_path:
        messagebox.showwarning("Warnung", "Bitte beide Pfade angeben.")
        return
    generate_gbxml(ifc_path, output_path)

# Tkinter-UI erstellen
root = tk.Tk()
root.title("IFC zu gbXML Konverter")
root.geometry("400x400")

# IFC-Datei Eingabe
tk.Label(root, text="IFC-Datei:").pack(pady=5)
ifc_entry = tk.Entry(root, width=50)
ifc_entry.pack(pady=5)
tk.Button(root, text="IFC-Datei auswählen", command=select_ifc_file).pack(pady=5)

# Output-Datei Eingabe
tk.Label(root, text="Speicherort der gbXML-Datei:").pack(pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)
tk.Button(root, text="Speicherort auswählen", command=select_output_file).pack(pady=5)

# Konvertierungsbutton in einem separaten Frame
tk.Button(root, text="Konvertieren", command=start_conversion, bg="green", fg="white").pack(pady=10)


# Hauptloop starten
root.mainloop()
