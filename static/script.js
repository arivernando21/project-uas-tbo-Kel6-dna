function showPage(page, el){
    document.getElementById("analisis-page").style.display="none";
    document.getElementById("tentang-page").style.display="none";
    document.getElementById("panduan-page").style.display="none";

    document.getElementById(page+"-page").style.display="block";

    document.querySelectorAll(".menu li").forEach(li=>li.classList.remove("active"));
    el.classList.add("active");

    countDNA();
    
}

function countDNA() {
    const dna1 = document.getElementById("dna1");
    const dna2 = document.getElementById("dna2");

    if (dna1) {
        dna1.addEventListener("input", () => {
            let val = dna1.value.replace(/[^ATCG]/gi, "");
            document.getElementById("count1").innerText =
                "Panjang: " + val.length + " nukleotida";
        });

        // 🔥 supaya langsung update kalau ada isi awal
        dna1.dispatchEvent(new Event('input'));
    }

    if (dna2) {
        dna2.addEventListener("input", () => {
            let val = dna2.value.replace(/[^ATCG]/gi, "");
            document.getElementById("count2").innerText =
                "Panjang: " + val.length + " nukleotida";
        });

        dna2.dispatchEvent(new Event('input'));
    }
}

window.onload = countDNA;