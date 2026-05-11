// ottaa nyky ajan
let nyt = new Date();

function LaitaNykyAika() {
    // laittaa automaattisesti nykyajan aikaan
    nyt.setMinutes(nyt.getMinutes() - nyt.getTimezoneOffset());
    document.getElementById('aika').value = nyt.toISOString().slice(0,10);
    document.getElementById("aika").max = nyt.toISOString().slice(0,10);
}
LaitaNykyAika()

// jos input value on muu niin antaa teksti kentän
document.getElementsByName("laji")[0].addEventListener('change', Tee);
document.getElementsByName("viehe")[0].addEventListener('change', Tee);
document.getElementsByName("vapa")[0].addEventListener('change', Tee);

function Tee(){
    // saa arvon
    let arvo_laji = document.getElementById("KalaLaji").value;
    let arvo_viehe = document.getElementById("viehe").value;
    let arvo_vapa = document.getElementById("vapa").value;
    let input_name = document.querySelector("#muu");
    let h2_muu = document.getElementById("h2_muu");

    // tarkistaa on muu
    if (arvo_laji == "muu") {
        document.getElementById("laji_muu_div").style.display = "flex";
        document.getElementById("laji_muu_form").style.display = "flex";
        // asettaa name attribuutin
        input_name.setAttribute("name", "laji");
        h2_muu.innerHTML = "Anna uusi kalalaji:"
        // jos muu valittu laittaa että arvo tarvitaan
        document.getElementById("muu").required = true;
    } if (arvo_viehe == "muu") {
        document.getElementById("laji_muu_div").style.display = "flex";
        document.getElementById("laji_muu_form").style.display = "flex";
        // asettaa name attribuutin
        input_name.setAttribute("name", "viehe");
        h2_muu.innerHTML = "Anna uusi viehe:"
        // jos muu valittu laittaa että arvo tarvitaan
        document.getElementById("muu").required = true;
    } if (arvo_vapa == "muu") {
        document.getElementById("laji_muu_div").style.display = "flex";
        document.getElementById("laji_muu_form").style.display = "flex";
        // asettaa name attribuutin
        input_name.setAttribute("name", "vapa");
        h2_muu.innerHTML = "Anna uusi vapa:"
        // jos muu valittu laittaa että arvo tarvitaan
        document.getElementById("muu").required = true;
    }
}