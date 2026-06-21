import csv
import json
import re
import os

# Nama fail anda
fail_html = 'ibdal-game.html'
fail_csv = 'data.csv'

def kemaskini_html():
    print(f"Mencari fail {fail_csv}...")
    
    # 1. Pastikan CSV wujud
    if not os.path.exists(fail_csv):
        print(f"RALAT: Fail '{fail_csv}' tidak dijumpai di dalam folder ini.")
        print("Sila buat fail data.csv dengan lajur: Perkataan, Asal, Petunjuk, Sebab")
        return

    # 2. Baca data dari CSV
    data_baru = []
    try:
        # Gunakan 'utf-8-sig' supaya Python abaikan cop tersembunyi (BOM) dari Excel
        with open(fail_csv, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            # Buang ruang kosong (space) pada tajuk (jika ustaz tertekan space)
            headers = [h.strip() for h in reader.fieldnames if h]
            
            if not headers or 'Perkataan' not in headers or 'Asal' not in headers:
                print(f"RALAT: Format CSV salah! Tajuk yang dibaca: {headers}")
                print("Pastikan tajuk baris pertama ialah: Perkataan, Asal, Petunjuk, Sebab")
                return
                
            for row in reader:
                # Ambil data dan bersihkan space yang tidak sengaja ditaip di Excel
                perkataan = row.get('Perkataan', '').strip() if row.get('Perkataan') else ''
                asal = row.get('Asal', '').strip() if row.get('Asal') else ''
                petunjuk = row.get('Petunjuk', '').strip() if row.get('Petunjuk') else ''
                sebab = row.get('Sebab', '').strip() if row.get('Sebab') else ''
                
                if perkataan and asal:
                    data_baru.append({
                        "Perkataan": perkataan,
                        "Asal": asal,
                        "Petunjuk": petunjuk,
                        "Sebab": sebab
                    })
        
        print(f"Berjaya membaca {len(data_baru)} soalan dari CSV.")
    except Exception as e:
        print(f"RALAT semasa membaca CSV: {e}")
        return

    # Format data menjadi string Array JavaScript
    # ensure_ascii=False membenarkan tulisan Arab dikekalkan
    js_array_str = "let ibdalData = " + json.dumps(data_baru, ensure_ascii=False, indent=12) + ";"

    # 3. Baca kandungan fail HTML
    if not os.path.exists(fail_html):
        print(f"RALAT: Fail '{fail_html}' tidak dijumpai di dalam folder ini.")
        return

    try:
        with open(fail_html, mode='r', encoding='utf-8') as f:
            kandungan_html = f.read()

        # 4. Ganti blok data menggunakan Regex
        pattern = re.compile(r'(// --- BEGIN IBDAL DATA ---).*?(// --- END IBDAL DATA ---)', re.DOTALL)
        
        if pattern.search(kandungan_html):
            # Suntik data baru
            html_dikemaskini = pattern.sub(r'\1\n        ' + js_array_str + r'\n        \2', kandungan_html)
            
            # Tulis semula ke fail HTML
            with open(fail_html, mode='w', encoding='utf-8') as f:
                f.write(html_dikemaskini)
            print(f"\n✅ BERJAYA! Fail '{fail_html}' telah dikemas kini dengan soalan baharu.")
            print("Anda kini boleh hantar fail HTML ini kepada pelajar.")
        else:
            print(f"\nRALAT: Penanda '// --- BEGIN IBDAL DATA ---' tidak dijumpai di dalam '{fail_html}'.")
            
    except Exception as e:
        print(f"RALAT semasa mengubah HTML: {e}")

if __name__ == "__main__":
    kemaskini_html()
    input("\nTekan Enter untuk keluar...")