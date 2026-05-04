from unittest import result

from flask import Flask, render_template, request
import re
from difflib import SequenceMatcher

app = Flask(__name__)

def clean_dna(dna):
    #regular language/bahasa formal Σ = {A, T, C, G} hanya menerima input {A, T, C, G} selain itu karakternya dihapus
    return re.sub(r'[^ATCG]', '', dna.upper())

#memvalidas sekuens DNA merupakan gen valid
def detect_gene(dna):
    #regex, language operators, finite automata, tunjukkan epsilon NFA
    match = re.fullmatch(r'ATG(?:[ATCG]{3})+(TAA|TAG|TGA)', dna)

    if match:
        return {
            "status": "TERDETEKSI",
            "start": match.start() + 1,
            "end": match.end(),
            "pos": f"{match.start()+1} - {match.end()}",
            "message": "Sekuens merupakan gen valid karena memiliki start codon (ATG), stop codon (TAA/TAG/TGA), dan panjangnya merupakan kelipatan 3."
        }

    return {
        "status": "TIDAK TERDETEKSI",
        "start": None,
        "end": None,
        "pos": "-",
        "message": "Sekuens bukan gen valid karena tidak memenuhi salah satu syarat: harus diawali ATG, diakhiri stop codon, dan memiliki panjang kelipatan 3."
    }

def find_motif(dna, motif):
    if not motif:
        return None
                #
    positions = [i+1 for i in range(len(dna)-len(motif)+1) 
                 if dna[i:i+len(motif)] == motif]

    return {
        "motif": motif,
        "positions": positions,
        "count": len(positions)
    }

def similarity(dna1, dna2):
    return round(SequenceMatcher(None, dna1, dna2).ratio() * 100, 2)

def similarity_info(score):
    if score >= 80:
        return {
            "label": "KEMIRIPAN TINGGI",
            "desc": "Sekuens DNA menunjukkan tingkat kemiripan yang tinggi.",
            "class": "high"
        }
    elif score >= 50:
        return {
            "label": "KEMIRIPAN SEDANG",
            "desc": "Sekuens DNA memiliki beberapa kesamaan, namun terdapat perbedaan signifikan.",
            "class": "medium"
        }
    else:
        return {
            "label": "KEMIRIPAN RENDAH",
            "desc": "Sekuens DNA memiliki banyak perbedaan.",
            "class": "low"
        }

def detect_mutation(dna1, dna2):

    result = []
    for i in range(min(len(dna1), len(dna2))):
        if dna1[i] != dna2[i]:
            result.append({
                "pos": i+1,
                "d1": dna1[i],
                "d2": dna2[i]
            })
    return result

def generate_conclusion(result, motif_input):
        gene = result.get("gene", {})
        motif_result = result.get("motif", [])
        sim = result.get("similarity", 0)
        mut = result.get("mutation", [])

        # GEN
        if gene.get("status") == "TERDETEKSI":
            gen_text = "terdeteksi pola gen yang valid"
        else:
            gen_text = "tidak ditemukan pola gen yang valid"

        # MOTIF
        if motif_input:
            if motif_result:
                motif_text = f"motif '{motif_input}' ditemukan dalam sekuens"
            else:
                motif_text = f"motif '{motif_input}' tidak ditemukan"
        else:
            motif_text = "tidak dilakukan pencarian motif"

        # SIMILARITY
        if sim >= 80:
            sim_text = "tingkat kemiripan antar sekuens tergolong tinggi"
        elif sim >= 50:
            sim_text = "tingkat kemiripan antar sekuens tergolong sedang"
        else:
            sim_text = "tingkat kemiripan antar sekuens tergolong rendah"

        # MUTASI
        if len(mut) > 0:
            mut_text = "terdapat perbedaan nukleotida yang mengindikasikan adanya mutasi"
        else:
            mut_text = "tidak ditemukan perbedaan nukleotida (tidak ada mutasi)"

        return f"Berdasarkan hasil analisis, {gen_text}, {motif_text}, {sim_text}, serta {mut_text}."

def mutation_info(mutations):
    if len(mutations) > 0:
        return {
            "status": "TERDETEKSI",
            "count": len(mutations),
            "desc": f"Terdapat {len(mutations)} perbedaan nukleotida antara kedua sekuens.",
            "class": "detected"
        }
    else:
        return {
            "status": "TIDAK TERDETEKSI",
            "count": 0,
            "desc": "Tidak ditemukan perbedaan antara kedua sekuens DNA.",
            "class": "not-detected"
        }
    
@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    dna1 = dna2 = motif = ""

    if request.method == "POST":
        dna1 = clean_dna(request.form.get("dna1", ""))
        dna2 = clean_dna(request.form.get("dna2", ""))
        motif = request.form.get("motif", "").upper()

        if not dna1:
            result["error"] = "DNA hanya boleh mengandung A, T, C, G"
            return render_template("index.html", result=result, dna1=dna1, dna2=dna2, motif=motif)

        gene = detect_gene(dna1)
        result["gene"] = gene

        if motif:
          result["motif"] = find_motif(dna1, motif)
        else:
            result["motif"] = None

        if dna2:
            sim = similarity(dna1, dna2)
            result["similarity"] = sim
            result["similarity_info"] = similarity_info(sim)

            mut = detect_mutation(dna1, dna2)
            result["mutation"] = mut
            result["mutation_info"] = mutation_info(mut)
            result["conclusion"] = generate_conclusion(result, motif)

    return render_template("index.html", result=result, dna1=dna1, dna2=dna2, motif=motif)

if __name__ == "__main__":
    app.run(debug=True)