const catchDate = document.getElementById('aika');
const now = new Date();
now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
catchDate.value = now.toISOString().slice(0, 10);
catchDate.max = catchDate.value;

document.getElementById('kuvaBt').addEventListener('click', () => {
    document.getElementById('fileToUpload').click();
});

function showOtherValue() {
    const selected = [
        ['KalaLaji', 'Anna uusi kalalaji:', 'laji'],
        ['viehe', 'Anna uusi viehe:', 'viehe'],
        ['vapa', 'Anna uusi vapa:', 'vapa'],
    ].find(([id]) => document.getElementById(id).value === 'muu');

    if (!selected) {
        return;
    }

    document.getElementById('main-div').style.display = 'none';
    document.getElementById('laji_muu_div').style.display = 'flex';
    document.getElementById('laji_muu_form').style.display = 'flex';
    document.getElementById('muu').name = selected[2];
    document.getElementById('muu').required = true;
    document.getElementById('h2_muu').textContent = selected[1];
}

for (const id of ['KalaLaji', 'viehe', 'vapa']) {
    document.getElementById(id).addEventListener('change', showOtherValue);
}
